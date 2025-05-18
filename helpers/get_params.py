from typing import List
import re

from parsers import parse_brackets, parse_braces, parse_colon


def get_params(init_arr: List[str]) -> List[str]:
    res = []
    for el in init_arr:
        # Если параметра нет, то продожаем цикл
        if el == "":
            continue

        curr_var = el

        # Убираем скобки из названия параметра
        if "(" in el and ")=" in el:
            curr_var = parse_brackets(el)

        # Убираем фигурные скобки из названия параметра
        if "{" in el and "}=" in el:
            curr_var = parse_braces(el)

        # Обработка двоеточия
        if ":" in el:
            curr_var = parse_colon(el)

        # Обработка evs
        if "evs" in el and "'" not in el:
            curr_var = "='".join(el.split("=")) + "'"

        # TODO обработчик
        if "test.Xcr" in el or "test.Zcr" in el:
            curr_var = "='".join(el.split("=")) + "'"

        dh_pattern = r"dH\(\s*(-?\d+(?:\.\d+)?)\s*\)"
        dh_match = re.search(dh_pattern, curr_var)

        if dh_match:
            curr_var = re.sub(dh_pattern, lambda m: f"dH{m.group(1)}", curr_var)

        res.append(curr_var)

    return res
