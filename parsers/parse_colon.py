from typing import List

def parse_colon(a: str) -> List[int]:
    return "='".join(a.split("="))+"'"