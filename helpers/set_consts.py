from parsers import parse_colon


def set_consts(msg: str):
    arr = msg[12 : len(msg) - 25].split("; ")

    # Создание массива переменных
    for el in arr:
        # Если переменной нет, то продожаем цикл
        if el == "":
            continue
        curr_var = el
        # Убираем скобки из переменной
        if "(" in el and ")=" in el:
            curr_var = "".join("".join(el.split("(")).split(")"))
        if "{" in el and "}=" in el:
            curr_var = "".join("".join(el.split("{")).split("}"))
        # Убираем двоеточие из переменной
        if ":" in el:
            curr_var = parse_colon(el)
        # Убираем двоеточие из переменной
        if ":" in el or ("evs" in el and "'" not in el):
            curr_var = "='".join(el.split("=")) + "'"
        # Выполняем присваивание
        print("Текущая переменая", curr_var)
        exec(curr_var, globals())
