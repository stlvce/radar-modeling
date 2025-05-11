def parse_braces(a: str) -> str:
    return "".join("".join(a.split("{")).split("}"))
