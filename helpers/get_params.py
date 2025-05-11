from typing import List

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

        if "test.Xcr" in el or "test.Zcr" in el:
            curr_var = "='".join(el.split("=")) + "'"

        res.append(curr_var)

    return res
