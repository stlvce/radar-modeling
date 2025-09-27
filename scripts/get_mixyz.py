import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (подключение 3D проекции)
from PIL import Image
import os


def get_mixyz(
    Nmax: int = 0,
    Rs: float = 1.0,
    Rz: float = 1.0,
    Ry: float = 1.0,
    Zmax: float = 4.0,
    Ymax: float = 4.0,
    figext: int = 1,
    result_path: str = "resultFig1.bmp",
    Rs_x: list | None = None,
    Rs_z: list | None = None,
):
    """
    Параметры:
      Nmax: int
        количество элементов (если 0 => будет вычислено как len(sx)*4)
      Rs, Rz, Ry: float
        геометрические параметры (аналог Mi.Rs, Mi.Rz, Mi.Ry)
      Zmax, Ymax: float
        пороги для фильтрации (аналог Mi.Zmax, Mi.Ymax)
      figext: int
        уровень отрисовки (>=0 — рисовать основные точки; >0 — дополнительные линии)
      result_path: str
        куда сохранить BMP (по умолчанию 'resultFig1.bmp' в cwd)
      Rs_x, Rs_z: optional lists
        массивы отсчётов для Rs.x и Rs.z (если хотите визуализировать исходные точки).
    Возвращает:
      dict с полями Mi (numpy-массивы и параметры)
    """
    sx = [
        0,
        1,
        1,
        2,
        -1,
        0,
        -1,
        0,
        -2,
        2,
        3,
        1,
        -2,
        -1,
        -3,
        0,
        2,
        3,
        1,
        4,
        -2,
        -1,
        -3,
        0,
        -4,
        3,
        4,
        2,
        5,
        1,
        -3,
        -2,
        -4,
        -1,
        -5,
        0,
        3,
        4,
        2,
        5,
        1,
        6,
        -3,
        -2,
        -4,
        -1,
        -5,
        0,
        -6,
        4,
        5,
        3,
        6,
        2,
        7,
        1,
        0,
        -4,
        -3,
        -5,
        -2,
        -6,
        -1,
        -7,
        4,
        5,
        3,
        6,
        2,
        7,
        1,
        8,
        -4,
        -3,
        -5,
        -2,
        -6,
        -1,
        -7,
        -8,
        0,
        5,
        6,
        4,
        7,
        3,
        8,
        2,
        1,
        -5,
        -4,
        -6,
        -3,
        -7,
        -2,
        -8,
        -1,
        0,
        -9,
        5,
        6,
        4,
        7,
        3,
        8,
        2,
        9,
        -1,
        -10,
        -5,
        -4,
        -6,
        -3,
        -7,
        -2,
        -8,
        -9,
        1,
        9,
        10,
        0,
    ]

    sz = [
        0,
        1,
        -1,
        0,
        1,
        2,
        -1,
        -2,
        0,
        2,
        1,
        3,
        2,
        3,
        1,
        4,
        -2,
        -1,
        -3,
        0,
        -2,
        -3,
        -1,
        -4,
        0,
        3,
        2,
        4,
        1,
        5,
        3,
        4,
        2,
        5,
        1,
        6,
        -3,
        -2,
        -4,
        -1,
        -5,
        0,
        -3,
        -4,
        -2,
        -5,
        -1,
        -6,
        0,
        4,
        3,
        5,
        2,
        6,
        1,
        7,
        8,
        4,
        5,
        3,
        6,
        2,
        7,
        1,
        -4,
        -3,
        -5,
        -2,
        -6,
        -1,
        -7,
        0,
        -4,
        -5,
        -3,
        -6,
        -2,
        -7,
        -1,
        0,
        -8,
        5,
        4,
        6,
        3,
        7,
        2,
        8,
        9,
        5,
        6,
        4,
        7,
        3,
        8,
        2,
        9,
        10,
        1,
        -5,
        -4,
        -6,
        -3,
        -7,
        -2,
        -8,
        1,
        -9,
        0,
        -5,
        -6,
        -4,
        -7,
        -3,
        -8,
        -2,
        -1,
        -9,
        -1,
        0,
        -10,
    ]

    # Если Nmax == 0 => numel(sx)*4
    if Nmax == 0:
        Nmax = len(sx) * 4

    # Массивы Mi.* (нулевые)
    Mi_Ax = np.zeros(Nmax, dtype=float)
    Mi_Az = np.zeros(Nmax, dtype=float)
    Mi_Mx = np.zeros(Nmax, dtype=float)
    Mi_Mz = np.zeros(Nmax, dtype=float)
    Mi_Rt = np.zeros(Nmax, dtype=float)
    Mi_My = np.zeros(Nmax, dtype=float)

    # углы
    AlfaX = math.atan(Rz / 2.0 / Rs)
    AlfaZ = math.atan(Ry / 2.0 / Rs)

    # сколько "блоков" (sn)
    sn = (Nmax + 3) // 4
    # не индексируем за пределы sx/sz
    sn = min(sn, len(sx))

    Ants = 0

    # Настройка рисунка
    # fig = plt.figure(figsize=(10, 7))
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter([0], [0], [0], marker="h", color="magenta", label="origin")
    # удерживаем легенду/секции
    for k in range(sn):
        base = k * 4
        # проверка границ (нужны хотя бы два слота для первой пары)
        if base + 1 >= Nmax:
            break

        # первая пара
        Mi_Ax[base + 0] = AlfaX * (sx[k] + 0.5)
        Mi_Mx[base + 0] = math.tan(Mi_Ax[base + 0]) * Rs * 2.0
        Mi_Az[base + 0] = AlfaZ * sz[k]
        Mi_Mz[base + 0] = math.tan(Mi_Az[base + 0]) * Rs * 2.0

        Mi_Ax[base + 1] = AlfaX * (sx[k] - 0.5)
        Mi_Mx[base + 1] = math.tan(Mi_Ax[base + 1]) * Rs * 2.0
        Mi_Az[base + 1] = AlfaZ * sz[k]
        Mi_Mz[base + 1] = math.tan(Mi_Az[base + 1]) * Rs * 2.0

        # проверить ограничение
        if (
            abs(Mi_Mx[base + 0]) > Zmax
            or abs(Mi_Mx[base + 1]) > Zmax
            or abs(Mi_Mz[base + 0]) > Ymax
            or abs(Mi_Mz[base + 1]) > Ymax
        ):
            Mi_Mx[base + 0] = 0.0
            Mi_Mz[base + 0] = 0.0
            Mi_Mx[base + 1] = 0.0
            Mi_Mz[base + 1] = 0.0
            continue

        Mi_Rt[base + 0] = math.sqrt(Mi_Mx[base + 0] ** 2 + Rs**2 + Mi_Mz[base + 0] ** 2)
        Mi_Rt[base + 1] = math.sqrt(Mi_Mx[base + 1] ** 2 + Rs**2 + Mi_Mz[base + 1] ** 2)
        Ants += 2

        # вторая пара (если есть место)
        if base + 3 < Nmax:
            Mi_Ax[base + 2] = AlfaX * sx[k]
            Mi_Mx[base + 2] = math.tan(Mi_Ax[base + 2]) * Rs * 2.0
            Mi_Az[base + 2] = AlfaZ * (sz[k] + 0.5)
            Mi_Mz[base + 2] = math.tan(Mi_Az[base + 2]) * Rs * 2.0

            Mi_Ax[base + 3] = AlfaX * sx[k]
            Mi_Mx[base + 3] = math.tan(Mi_Ax[base + 3]) * Rs * 2.0
            Mi_Az[base + 3] = AlfaZ * (sz[k] - 0.5)
            Mi_Mz[base + 3] = math.tan(Mi_Az[base + 3]) * Rs * 2.0

            # проверка ограничений для 2-й пары
            if (
                abs(Mi_Mx[base + 2]) > Zmax
                or abs(Mi_Mx[base + 3]) > Zmax
                or abs(Mi_Mz[base + 2]) > Ymax
                or abs(Mi_Mz[base + 3]) > Ymax
            ):
                # зануляем все 4 слота (как в оригинале)
                Mi_Mx[base + 0] = 0.0
                Mi_Mz[base + 0] = 0.0
                Mi_Mx[base + 1] = 0.0
                Mi_Mz[base + 1] = 0.0
                Mi_Mx[base + 2] = 0.0
                Mi_Mz[base + 2] = 0.0
                Mi_Mx[base + 3] = 0.0
                Mi_Mz[base + 3] = 0.0
                continue

            Mi_Rt[base + 2] = math.sqrt(
                Mi_Mx[base + 2] ** 2 + Rs**2 + Mi_Mz[base + 2] ** 2
            )
            Mi_Rt[base + 3] = math.sqrt(
                Mi_Mx[base + 3] ** 2 + Rs**2 + Mi_Mz[base + 3] ** 2
            )
            Ants += 2

        # Отрисовка согласно figext
        if figext > 0:
            # первая линия (между base and base+1)
            ax.plot(
                [Mi_Mx[base + 0], Mi_Mx[base + 1]],
                [Rs, Rs],
                [Mi_Mz[base + 0], Mi_Mz[base + 1]],
                "-ro",
            )
            # вторая линия, если есть
            if base + 3 < Nmax:
                ax.plot(
                    [Mi_Mx[base + 2], Mi_Mx[base + 3]],
                    [Rs, Rs],
                    [Mi_Mz[base + 2], Mi_Mz[base + 3]],
                    "-bo",
                )
            # при первом блоке — показать исходные Rs точки (если переданы)
            if k == 0 and (Rs_x is not None and Rs_z is not None):
                # отрисовать первые 4 опорных точки (если есть)
                for j in range(min(4, len(Rs_x))):
                    ax.scatter([Rs_x[j]], [0], [Rs_z[j]], marker="o")

        # общая точка для этого блока
        ax.scatter([sx[k] * Rz], [Rs], [sz[k] * Ry], marker="D", color="k")

    # После цикла: вычисления расстояний/диффов (Mi.Dists, Mi.Diffs, Mi.dDist)
    Dists = np.sqrt(Mi_Mx**2 + Rs**2 + Mi_Mz**2)
    # исключаем те значения, которые равны Rs
    mask = Dists > Rs
    if np.any(mask):
        min_dist = np.min(Dists[mask])
    else:
        min_dist = Rs
    Diffs = Dists - min_dist

    if np.any(Diffs >= 0):
        dDist = np.max(Diffs[Diffs >= 0])
    else:
        dDist = 0.0

    Mi_My[:] = Rs

    # Настройка внешнего вида графика
    title_text = f"Антенны (Mi.Ants={Ants})"
    ax.set_title(title_text, fontsize=10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(True)

    # Попытка выставить равные масштабы по осям
    try:
        ax.set_box_aspect([1, 1, 1])
    except Exception:
        pass

    # Сохранение рисунка в BMP
    tmp_path = "tmp.png"
    plt.tight_layout()
    # plt.savefig(tmp_path, dpi=300)
    plt.savefig(tmp_path, dpi=100)
    Image.open(tmp_path).save(result_path)
    plt.close(fig)
    os.remove(tmp_path)

    print(
        f"Angles of first elements have AlfaX={AlfaX / math.pi * 180 * 2:.6g}, AlfaZ={AlfaZ / math.pi * 180 * 2:.6g}"
    )

    # Возвращаем словарь Mi (в виде numpy-массивов) и некоторые вычисленные величины
    Mi = {
        "Ax": Mi_Ax,
        "Az": Mi_Az,
        "Mx": Mi_Mx,
        "Mz": Mi_Mz,
        "Rt": Mi_Rt,
        "My": Mi_My,
        "Dists": Dists,
        "Diffs": Diffs,
        "dDist": dDist,
        "Ants": Ants,
        "AlfaX": AlfaX,
        "AlfaZ": AlfaZ,
        "Rs": Rs,
        "Rz": Rz,
        "Ry": Ry,
    }
    return Mi
