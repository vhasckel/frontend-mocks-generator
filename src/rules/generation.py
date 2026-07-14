"""Regras e heurísticas de geração de valores de mock (SPEC §11, RN04–RN06)."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

# Exemplos alinhados à SPEC §11
DEFAULT_STRING = "João Silva"
DEFAULT_EMAIL = "user@email.com"
DEFAULT_PHONE = "(11) 99999-9999"
DEFAULT_CPF = "123.456.789-09"
DEFAULT_CNPJ = "12.345.678/0001-90"
DEFAULT_UUID = "550e8400-e29b-41d4-a716-446655440000"
DEFAULT_CITY = "São Paulo"
DEFAULT_NUMBER = 199.9
DEFAULT_ID_NUMBER = 1
DEFAULT_BOOLEAN = True
ISO_DATE_EXPR = "new Date().toISOString()"

# Arrays: entre 2 e 5 elementos (SPEC §11)
ARRAY_MIN_LEN = 2
ARRAY_MAX_LEN = 5
DEFAULT_ARRAY_LEN = 2


def to_camel_case(name: str) -> str:
    """Converte PascalCase/snake_case em camelCase para nomes de arquivo/const."""
    if not name:
        return name
    parts = re.split(r"[\s_\-]+", name)
    if len(parts) == 1:
        token = parts[0]
        if token.isupper() and len(token) > 1:
            return token.lower()
        return token[0].lower() + token[1:]
    head, *tail = parts
    return head.lower() + "".join(p[:1].upper() + p[1:] for p in tail if p)


def mock_const_name(entity_name: str) -> str:
    """Retorna o identificador da constante exportada (ex.: User → userMock)."""
    return f"{to_camel_case(entity_name)}Mock"


def mock_filename(entity_name: str) -> str:
    """Retorna o nome do arquivo de mock (ex.: User → user.mock.ts)."""
    return f"{to_camel_case(entity_name)}.mock.ts"


def _normalize_prop_name(name: str) -> str:
    return re.sub(r"[\s_\-]+", "", (name or "").lower())


def _strip_wrappers(type_str: str) -> str:
    text = (type_str or "").strip().rstrip("?")
    if "|" in text and not text.startswith("{"):
        parts = [p.strip() for p in text.split("|")]
        parts = [p for p in parts if p not in ("null", "undefined") and p]
        if parts:
            text = parts[0]
    return text.strip()


def _is_array_type(type_str: str) -> bool:
    text = _strip_wrappers(type_str)
    if text.endswith("[]"):
        return True
    return bool(re.match(r"^Array\s*<", text))


def _array_element_type(type_str: str) -> str:
    text = _strip_wrappers(type_str)
    if text.endswith("[]"):
        return text[:-2].strip()
    match = re.match(r"^Array\s*<\s*([\s\S]+)\s*>$", text)
    if match:
        return match.group(1).strip()
    return "string"


def _is_number_type(type_str: str) -> bool:
    return _strip_wrappers(type_str) in {"number", "Number", "bigint", "BigInt"}


def _is_boolean_type(type_str: str) -> bool:
    return _strip_wrappers(type_str) in {"boolean", "Boolean"}


def _is_string_type(type_str: str) -> bool:
    return _strip_wrappers(type_str) in {"string", "String"}


def _is_date_type(type_str: str, prop_name: str) -> bool:
    text = _strip_wrappers(type_str)
    norm = _normalize_prop_name(prop_name)
    if text in {"Date", "DateTime"}:
        return True
    return text == "string" and any(
        key in norm
        for key in ("createdat", "updatedat", "deletedat", "date", "timestamp")
    )


def _looks_like_email(prop_name: str) -> bool:
    return "email" in _normalize_prop_name(prop_name)


def _looks_like_phone(prop_name: str) -> bool:
    norm = _normalize_prop_name(prop_name)
    return any(k in norm for k in ("phone", "telefone", "celular", "mobile"))


def _looks_like_cpf(prop_name: str) -> bool:
    return "cpf" in _normalize_prop_name(prop_name)


def _looks_like_cnpj(prop_name: str) -> bool:
    return "cnpj" in _normalize_prop_name(prop_name)


def _looks_like_uuid(prop_name: str, type_str: str) -> bool:
    norm = _normalize_prop_name(prop_name)
    text = _strip_wrappers(type_str).lower()
    if "uuid" in norm or text in {"uuid", "guid"}:
        return True
    return norm == "id" and _is_string_type(type_str)


def _looks_like_price(prop_name: str) -> bool:
    norm = _normalize_prop_name(prop_name)
    return any(k in norm for k in ("price", "amount", "value", "total", "salary", "preco"))


def _looks_like_city(prop_name: str) -> bool:
    norm = _normalize_prop_name(prop_name)
    return "city" in norm or "cidade" in norm


def _ts_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def build_model_index(parsed_model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Indexa models por nome a partir de ``parsed_model`` (primary + nested + models)."""
    index: dict[str, dict[str, Any]] = {}

    def _add(model: dict[str, Any]) -> None:
        name = model.get("name")
        if isinstance(name, str) and name:
            index[name] = model

    if parsed_model.get("name"):
        _add(parsed_model)

    for key in ("nested", "models"):
        items = parsed_model.get(key) or []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    _add(item)
                    nested = item.get("nested") or []
                    if isinstance(nested, list):
                        for child in nested:
                            if isinstance(child, dict):
                                _add(child)
    return index


def _resolve_named_model(
    type_name: str, model_index: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    return model_index.get(_strip_wrappers(type_name))


def _string_value_for_name(prop_name: str, type_str: str) -> str:
    if _looks_like_email(prop_name):
        return _ts_string(DEFAULT_EMAIL)
    if _looks_like_phone(prop_name):
        return _ts_string(DEFAULT_PHONE)
    if _looks_like_cpf(prop_name):
        return _ts_string(DEFAULT_CPF)
    if _looks_like_cnpj(prop_name):
        return _ts_string(DEFAULT_CNPJ)
    if _looks_like_uuid(prop_name, type_str):
        return _ts_string(DEFAULT_UUID)
    if _looks_like_city(prop_name):
        return _ts_string(DEFAULT_CITY)
    norm = _normalize_prop_name(prop_name)
    if norm in {"name", "fullname", "nome"} or norm.endswith("name"):
        return _ts_string(DEFAULT_STRING)
    if "role" in norm:
        return _ts_string("ADMIN")
    return _ts_string(DEFAULT_STRING)


def _value_for_array_element(
    prop_name: str,
    elem_type: str,
    model_index: dict[str, dict[str, Any]],
    *,
    depth: int,
    index: int,
) -> str:
    """Valores de elementos de array; ``roles`` segue o exemplo da SPEC §11/§14."""
    norm = _normalize_prop_name(prop_name)
    if _is_string_type(elem_type) and "role" in norm:
        samples = ["ADMIN", "USER", "GUEST", "EDITOR", "VIEWER"]
        return _ts_string(samples[index % len(samples)])
    if _is_string_type(elem_type):
        samples = [DEFAULT_STRING, "Maria Souza", "Pedro Alves", "Ana Costa", "Lucas Lima"]
        return _ts_string(samples[index % len(samples)])
    if _is_number_type(elem_type):
        return str(index + 1)
    return value_for_type(
        prop_name, elem_type, model_index, depth=depth + 1, array_len=DEFAULT_ARRAY_LEN
    )


def value_for_type(
    prop_name: str,
    type_str: str,
    model_index: dict[str, dict[str, Any]],
    *,
    depth: int = 0,
    array_len: int = DEFAULT_ARRAY_LEN,
    indent: int = 2,
) -> str:
    """Gera expressão TypeScript coerente com tipo e nome da propriedade.

    Nunca inventa propriedades de objetos: só usa as do ``model_index`` (RN04/RN05).
    """
    if depth > 8:
        return "null"

    text = _strip_wrappers(type_str)
    length = max(ARRAY_MIN_LEN, min(ARRAY_MAX_LEN, array_len))

    if _is_array_type(type_str):
        elem = _array_element_type(type_str)
        items = [
            _value_for_array_element(
                prop_name, elem, model_index, depth=depth, index=i
            )
            for i in range(length)
        ]
        return f"[{', '.join(items)}]"

    named = _resolve_named_model(text, model_index)
    if named is not None:
        kind = named.get("kind")
        if kind == "enum":
            values = named.get("enum_values") or []
            if values:
                return f"{named.get('name') or text}.{values[0]}"
            return "null"
        return object_literal_for_model(
            named, model_index, depth=depth + 1, indent=indent
        )

    if _is_date_type(type_str, prop_name):
        return ISO_DATE_EXPR

    if _is_boolean_type(type_str):
        return "true" if DEFAULT_BOOLEAN else "false"

    if _is_number_type(type_str):
        norm = _normalize_prop_name(prop_name)
        if norm == "id" or norm.endswith("id") or "count" in norm or "age" in norm:
            return str(DEFAULT_ID_NUMBER)
        if _looks_like_price(prop_name):
            return str(DEFAULT_NUMBER)
        return str(DEFAULT_ID_NUMBER)

    if _is_string_type(type_str):
        return _string_value_for_name(prop_name, type_str)

    literal = re.match(r"^['\"](.*)['\"]$", text)
    if literal:
        return _ts_string(literal.group(1))

    if re.match(r"^[A-Z]\w*$", text):
        return "{}"

    return _string_value_for_name(prop_name, type_str)


def object_literal_for_model(
    model: dict[str, Any],
    model_index: dict[str, dict[str, Any]],
    *,
    depth: int = 0,
    indent: int = 0,
) -> str:
    """Monta um object literal TS apenas com propriedades do modelo (RN04/RN05)."""
    properties = model.get("properties") or []
    if not isinstance(properties, list) or not properties:
        return "{}"

    inner = " " * (indent + 2)
    closing = " " * indent
    lines = ["{"]
    for prop in properties:
        if not isinstance(prop, dict):
            continue
        name = prop.get("name")
        if not isinstance(name, str) or not name:
            continue
        type_str = str(prop.get("type") or "string")
        value = value_for_type(
            name,
            type_str,
            model_index,
            depth=depth,
            indent=indent + 2,
        )
        lines.append(f"{inner}{name}: {value},")
    lines.append(f"{closing}}}")
    return "\n".join(lines)


def compose_mock_source(
    *,
    entity_name: str,
    kind: str,
    object_body: str,
    import_path: str | None,
) -> str:
    """Compõe o arquivo TypeScript no estilo da SPEC §6."""
    const_name = mock_const_name(entity_name)
    lines: list[str] = []

    if import_path:
        lines.append(f"import {{ {entity_name} }} from '{import_path}';")
        lines.append("")

    type_annot = entity_name if kind in {"interface", "type", "enum"} else entity_name
    lines.append(f"export const {const_name}: {type_annot} = {object_body};")
    lines.append("")
    return "\n".join(lines)


def relative_import_path(output_path: str, input_path: str) -> str:
    """Calcula import relativo do mock até o arquivo de entrada (sem extensão)."""
    out = Path(output_path)
    src = Path(input_path)
    # Preserve relative layout when both paths are relative (common in agent state).
    if not out.is_absolute() and not src.is_absolute():
        rel = Path(os.path.relpath(src.with_suffix(""), start=out.parent))
    else:
        rel = Path(os.path.relpath(src.resolve().with_suffix(""), start=out.resolve().parent))
    text = rel.as_posix()
    if not text.startswith("."):
        text = f"./{text}"
    return text


def resolve_output_path(entity_name: str, mocks_output_dir: str | Path) -> str:
    """Retorna ``MOCKS_OUTPUT_DIR/<entity>.mock.ts`` em camelCase."""
    base = Path(mocks_output_dir)
    return str(base / mock_filename(entity_name))


def generate_mock_code(
    parsed_model: dict[str, Any],
    *,
    input_path: str = "",
    output_path: str = "",
) -> str:
    """Gera o código TypeScript completo do mock a partir de ``parsed_model``."""
    entity_name = str(parsed_model.get("name") or "Entity")
    kind = str(parsed_model.get("kind") or "interface")
    model_index = build_model_index(parsed_model)

    if kind == "enum":
        values = parsed_model.get("enum_values") or []
        first = values[0] if values else None
        body = f"{entity_name}.{first}" if first else "null as never"
    else:
        body = object_literal_for_model(parsed_model, model_index, depth=0, indent=0)

    import_path = None
    if input_path and output_path:
        import_path = relative_import_path(output_path, input_path)

    return compose_mock_source(
        entity_name=entity_name,
        kind=kind,
        object_body=body,
        import_path=import_path,
    )
