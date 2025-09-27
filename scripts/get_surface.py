import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os


def gen_forest(
    N_trees=50,
    area_size=(200, 200),
    h_mean=20,
    h_std=5,
    r_mean=5,
    r_std=2,
    base_height=0,
):
    """
    Генерация леса (Type=4).
    """
    x = (np.random.rand(N_trees) - 0.5) * area_size[0]
    z = (np.random.rand(N_trees) - 0.5) * area_size[1]
    h = np.abs(np.random.normal(h_mean, h_std, N_trees))
    r = np.abs(np.random.normal(r_mean, r_std, N_trees))

    y_base = np.full(N_trees, base_height)
    y_top = base_height + h

    return {
        "x": x,
        "z": z,
        "y_base": y_base,
        "y_top": y_top,
        "h": h,
        "r": r,
    }


def plot_forest(forest, ax):
    """
    Визуализация леса (стволы + вершины).
    """
    for i in range(len(forest["x"])):
        # Ствол
        ax.plot(
            [forest["x"][i], forest["x"][i]],
            [forest["z"][i], forest["z"][i]],
            [forest["y_base"][i], forest["y_top"][i]],
            c="saddlebrown",
            linewidth=2,
        )

        # Крона (верхушка)
        ax.scatter(
            forest["x"][i],
            forest["z"][i],
            forest["y_top"][i],
            c="green",
            s=forest["r"][i] * 20,
            alpha=0.6,
        )


def calc_surface(Sf, Tr, St, params, result_path="surface.bmp"):
    """
    Пересчёт подстилающей поверхности и построение сцены.
    Sf – словарь с параметрами поверхности (например Dspot)
    Tr – словарь с траекторией цели (Pos, Ang, N)
    St – словарь со станциями (Pos, N)
    params – словарь с дополнительными параметрами (Kr, DOR, dH, Type, test, Ncr)
    """
    Kr = params["Kr"]
    DOR = params["DOR"]
    dH = params["dH"]
    test = params["test"]
    Ncr = params.get("Ncr", 0)

    FacetN = max([Ncr + test.get("Nadir", 0), params.get("FacetN", 1), 1])
    cMass = np.zeros((13, FacetN))

    # Пример генерации случайных фаз и типов
    cMass[4, :] = 2 * np.pi * np.random.rand(FacetN)
    cMass[5, :] = params["Type"]
    cMass[6, :] = Kr[min(params["Type"], 7)]
    cMass[8, :] = np.deg2rad(DOR[min(params["Type"], 7)]) / 2

    # Координаты случайных фасетов (простая модель)
    FC = np.arange(Ncr, FacetN)
    cX = np.random.randn(len(FC))
    cZ = np.random.randn(len(FC))
    cMass[0, FC] = Sf["Dspot"] * cX + np.mean(Tr["Pos"][:-1, 0])
    cMass[2, FC] = Sf["Dspot"] * cZ + np.mean(Tr["Pos"][:-1, 2])
    cMass[1, FC] = 0  # пока без рельефа

    # Построение графика
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax: Axes3D = fig.add_subplot(111, projection="3d")

    # Траектория цели
    ax.plot3D(Tr["Pos"][:, 0], Tr["Pos"][:, 2], Tr["Pos"][:, 1], "-xm", label="Цель")

    # Станции
    if St["N"] > 0:
        for n in range(St["N"]):
            ax.plot3D(
                St["Pos"][:, 0, n],
                St["Pos"][:, 2, n],
                St["Pos"][:, 1, n],
                "-dr",
                label=f"Станция {n + 1}",
            )

    # Подстилающая поверхность
    ax.scatter(
        cMass[0, :], cMass[2, :], cMass[1, :], c="g", s=5, alpha=0.6, label="Surface"
    )

    # Лес, если Type == 4
    if params["Type"] == 4:
        forest = gen_forest(N_trees=100, area_size=(400, 400), base_height=0)
        plot_forest(forest, ax)

    ax.set_xlabel("x [м]")
    ax.set_ylabel("z [м]")
    ax.set_zlabel("y [м]")
    ax.set_title("Подстилающая поверхность")
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

    return cMass


if __name__ == "__main__":
    # Тестовый пример
    Tr = {
        "Pos": np.array([[0, 100, 0], [100, 120, 50], [200, 150, 100]]),
        "Ang": np.zeros((3, 3)),
        "N": 3,
    }
    St = {
        "Pos": np.zeros((3, 3, 1)),
        "N": 1,
    }
    Sf = {"Dspot": 50}
    params = {
        "Kr": [1, 1, 1, 1, 1, 1, 1, 1],
        "DOR": [10] * 8,
        "dH": 1,
        "Type": 4,  # Лес
        "test": {"Nadir": 0},
        "Ncr": 0,
    }

    calc_surface(Sf, Tr, St, params, result_path="surface.bmp")
    print("Surface generated -> surface.bmp")
