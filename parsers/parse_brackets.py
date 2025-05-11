def parse_brackets(a: str) -> str:
    return "".join("".join(a.split("(")).split(")"))
