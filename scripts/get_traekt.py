import numpy as np
from typing import Any


def get_traekt(
    globals: dict[str, Any] | None = None,
):
    f0 = globals["f0"]  # TODO в init_variable нет
    Ym = globals["Ym"]
    Rs = globals["Rs"]
    St = globals["St"]
    Tr = globals["Tr"]
    H = globals["H"]
    t = globals["t"]
    # Предполагается, что здесь определены значения c, f0, St, Rs и т. д.
    # Здесь подразумевается, что evs является словарем для доступа к переменным
    # evs = {...}
    # Пример инициализации параметров
    c = 3e8  # скорость света в м/с
    mean_f0 = np.mean(f0)  # замена mean(f0)
    Nimp = int(Rs.Nimp)

    if Ym == 0:
        tauimp = Rs.tauimp
        Timp = Rs.Timp
        dtau = Rs.dtau
        Rs.Tm = Rs.Timp
        Tm = Timp
        Rs.dR = dtau * c  # шаг по дальности
    else:
        Tm = Rs.Tm  # TODO в init_variable нет

    snr = Rs.snr
    Rs.Lambda = c / mean_f0  # средняя длина волны
    test_canceling = False
    perc_mem = -1  # процент выполнения для вывода по UDP
    hwb = {"canceling": 0}  # Используем словарь для хранения статуса

    n = np.arange(1, St.N + 1)  # счетчик для всех целей

    if "Tr" in locals() and len(Tr.Pos) > 0:
        Tr.Pos[0, :] = Tr.Pos[-1, :]  # начальная позиция (x,h,z)
        if St.N > 0:
            St.Pos[0, :, n] = St.Pos[-1, :, n]

    else:
        Tr.H1 = H
        Tr.N = Nimp
        # Подготовка массивов
        Tr.t = np.zeros(Tr.N + 1)
        Tr.Pos = np.zeros((Tr.N + 1, 3))
        Tr.V = np.zeros((Tr.N, 3))
        Tr.Ang = np.zeros((Tr.N, 3))
        Tr.Tm = np.zeros(Tr.N)
        Tr.Ti = np.zeros(Tr.N)
        Tr.Tm_Ni = np.zeros(Tr.N)
        Tr.Tm_i = np.zeros(Tr.N)
        Tr.TiT = np.zeros(Tr.N)
        Tr.TiR = np.zeros(Tr.N)
        Tr.Pz = np.zeros(Tr.N)  # мощность передатчика возможно зависит от высоты

        # Начальные значения
        Tr.Pos[0, :] = [Tr.Xa, Tr.Ya, Tr.Za]
        St.Pos = np.zeros((Tr.N + 1, 3, St.N))
        St.Pos[0, :, n] = [St.Xs, St.Ys, St.Zs]
        Tr.V = np.zeros((Tr.N, 3, St.N))
        Tr.Ang = np.zeros((Tr.N, 3, St.N))

    # Константы
    TrVall = globals["TrVall"]  # TODO в init_variable нет
    StVall = globals["StVall"]  # TODO в init_variable нет
    consts = {
        "TrVall": np.array([Tr.Vx, Tr.Vy, Tr.Vz]),
        "TrVskip": np.array_equal(TrVall, "000"),
        "StVall": np.array([St.Vx, St.Vy, St.Vz]),
        "StVskip": np.array_equal(StVall, "000"),
    }

    # Расчет точек в траектории
    for m in range(Tr.N + 1):
        if hwb["canceling"]:
            test_canceling = True
            break

        perc = round(100 * (m) / (Tr.N + 1))

        if perc > perc_mem:
            perc_mem = perc
            # Здесь может быть добавлен код для обновления прогресса

        Tr.t[m] = t  # текущее время в модели
        if m > 0:
            dT = t - Tr.t[m - 1]  # время от предыдущего положения в модели, мкс
            if consts["TrVskip"]:  # расчет точек траектории РЛС
                Tr.Pos[m, :] = [Tr.Xa, Tr.Ya, Tr.Za]
            else:  # сдвигаем координаты по вектору скорости
                Tr.Pos[m, :] = Tr.Pos[m - 1, :] + Tr.V[m - 1, :] * dT

            if consts["StVskip"] and St.N > 0:
                St.Pos[m, :, n] = [St.Xs, St.Ys, St.Zs]
            elif St.N > 0:
                St.Pos[m, :, n] = St.Pos[m - 1, :, n] + St.V[m - 1, :, n] * dT

            if m > Tr.N:
                break

        H = Tr.Pos[m, 1]  # высота
        Tr.V[m, :] = [Tr.Vx, Tr.Vy, Tr.Vz]
        Tr.Ang[m, :] = np.radians([Tr.tang, Tr.kren, Tr.psi])

        if St.N > 0:  # расчет точек траектории всех целей
            St.V[m, 0, n] = St.Vx
            St.V[m, 1, n] = St.Vy
            St.V[m, 2, n] = St.Vz
            St.Ang[m, 0, n] = np.radians(St.tang)
