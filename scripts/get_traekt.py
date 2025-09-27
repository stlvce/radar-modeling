import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os

c = 3e8  # скорость света, м/с


def get_traekt(
    Nimp=100,
    Xa=0,
    Ya=1000,
    Za=0,
    Vx=200,
    Vy=0,
    Vz=0,
    St_N=1,
    St_Xs=0,
    St_Ys=0,
    St_Zs=0,
    result_path="resultFig2.bmp",
):
    """
    Генерация траектории цели и (опционально) станций.
    :param Nimp: число импульсов
    :param Xa,Ya,Za: начальные координаты цели (x,h,z)
    :param Vx,Vy,Vz: скорости цели
    :param St_N: число станций
    :param St_Xs, St_Ys, St_Zs: координаты станции
    """

    # структура для цели (Tr)
    Tr = {
        "N": Nimp,
        "Pos": np.zeros((Nimp + 1, 3)),
        "V": np.zeros((Nimp, 3)),
        "Ang": np.zeros((Nimp, 3)),
        "t": np.zeros(Nimp + 1),
    }

    # начальная позиция цели
    Tr["Pos"][0, :] = [Xa, Ya, Za]

    # структура для станции (St)
    St = {
        "N": St_N,
        "Pos": np.zeros((Nimp + 1, 3, St_N)),
        "V": np.zeros((Nimp, 3, St_N)),
        "Ang": np.zeros((Nimp, 3, St_N)),
    }

    # начальная позиция станции
    for n in range(St_N):
        St["Pos"][0, :, n] = [St_Xs, St_Ys, St_Zs]

    # шаг по времени (для примера: 0.1 с)
    dt = 0.1

    # цикл генерации
    for m in range(1, Nimp + 1):
        Tr["t"][m] = Tr["t"][m - 1] + dt
        Tr["V"][m - 1, :] = [Vx, Vy, Vz]
        Tr["Pos"][m, :] = Tr["Pos"][m - 1, :] + Tr["V"][m - 1, :] * dt

        for n in range(St_N):
            St["V"][m - 1, :, n] = [0, 0, 0]  # станции статичны
            St["Pos"][m, :, n] = St["Pos"][m - 1, :, n]

    # построение графика
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax: Axes3D = fig.add_subplot(111, projection="3d")

    # траектория цели
    ax.plot3D(Tr["Pos"][:, 0], Tr["Pos"][:, 2], Tr["Pos"][:, 1], "-xm", label="Цель")

    # траектория станций
    if St_N > 0:
        for n in range(St_N):
            ax.plot3D(
                St["Pos"][:, 0, n],
                St["Pos"][:, 2, n],
                St["Pos"][:, 1, n],
                "-dr",
                label=f"Станция {n + 1}",
            )

    ax.set_xlabel("x (м)")
    ax.set_ylabel("z (м)")
    ax.set_zlabel("y (м)")
    ax.set_title("Траектория цели и станций")
    ax.legend()
    ax.grid(True)
    ax.axis("equal")

    # сохраняем как PNG временно
    tmp_path = "tmp.png"
    plt.tight_layout()
    plt.savefig(tmp_path, dpi=100)
    plt.close(fig)

    # конвертация в BMP
    im = Image.open(tmp_path)
    im.save(result_path)
    os.remove(tmp_path)

    return Tr, St
