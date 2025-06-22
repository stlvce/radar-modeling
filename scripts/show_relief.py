import numpy as np
import matplotlib.pyplot as plt
import base64


def show_relief(Relief):
    """
    Построение поверхности

    Args:
        Relief (Relief): <Название параметра>
    """
    # Здесь мы предполагаем наличие тестового словаря. Задайте его, если он не определён.
    test = {"h": [None, None, None], "fstep": [100, 100]}  # Пример значений fstep
    Sf = {
        "x_size": Relief.shape[1],
        "z_size": Relief.shape[0],
        "med_shift": min(Relief.shape) / 2 - 0.5,
        "XZstep": 10,
        "Relief": "Example Relief",
    }

    # Проверяем, есть ли фигура 3, если нет - создаем её
    if test["h"][2] is None:
        test["h"][2] = plt.figure()

    # Устанавливаем название окна
    plt.get_current_fig_manager().set_window_title("Вид поверхности")

    # Получаем размеры окна для бэкенда Tkinter
    try:
        tmp = (
            plt.get_current_fig_manager().window.winfo_width(),
            plt.get_current_fig_manager().window.winfo_height(),
        )
    except AttributeError:
        tmp = (800, 600)  # Ширина и высота по умолчанию, если не поддерживается

    # Устанавливаем новое положение окна
    x_pos = (test["h"][2].number - 1) * test["fstep"][0]
    y_pos = (test["h"][2].number - 1) * test["fstep"][1]

    # Используем значения по умолчанию, если текущее положение не определено
    width = tmp[0] if tmp[0] > 0 else 800  # В случае ошибки использовать 800
    height = tmp[1] if tmp[1] > 0 else 600  # В случае ошибки использовать 600

    # Обновляем геометрию окна
    plt.get_current_fig_manager().window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    # Определяем границы рельефа
    mm = (np.min(Relief), np.max(Relief))

    # Очищаем текущее состояние отображения
    plt.clf()

    # Создаём сетку
    X, Z = np.meshgrid(
        (np.arange(1, Sf["x_size"] + 1) - Sf["med_shift"]),
        (np.arange(1, Sf["z_size"] + 1) - Sf["med_shift"]),
    )

    # Строим контурный график
    plt.contourf(X * Sf["XZstep"], Z * Sf["XZstep"], Relief)
    plt.axis("equal")
    plt.gca().invert_yaxis()  # Инвертируем ось Y
    plt.axis("tight")

    # Назначаем метки осей
    plt.xlabel("x (м)", fontsize=9)
    plt.ylabel("z (м)", fontsize=9)

    # Назначаем заголовок графика
    plt.title(
        f'Вид рельефа "{Sf["Relief"]}"; высоты от {int(mm[0])} до {int(mm[1])} м',
        fontsize=9,
        fontweight="normal",
    )

    # Показываем график
    plt.colorbar()  # Добавляем цветовую шкалу

    # Сохранение графика
    plt.savefig("plots/relief_plot.png")
    with open("plots/relief_plot.png", "rb") as image_file:
        image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    return encoded_image
