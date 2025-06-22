import numpy as np


def calculate_relative_powers(z=0, y=0, dx=1, dz=1, a=[1, 1, 1, 1]):
    """
    Расчета относительных мощностей Изл.МИ

    Args:
        z (int): <Название параметра>
        y (int): <Название параметра>
        dx (int): <Название параметра>
        dz (int): <Название параметра>
        a (List[int]): <Название параметра>

    Returns:
        List[float]: Относительная мошность
    """

    try:
        # Определяем необходимые массивы
        Mi_Z = np.array([50, -50, 0, 0])  # Значения Z
        Mi_Y = np.array([0, 0, 50, -50])  # Значения Y

        # Вычисляем временные значения
        tmpa = np.abs(Mi_Z + Mi_Y - z - y) / np.sqrt(2)
        tmpd = np.sqrt((Mi_Z - z) ** 2 + (Mi_Y - y) ** 2)

        # Расчет относительных мощностей
        Pi = a * tmpa * np.sqrt(tmpd**2 - tmpa**2) / 50

        print("Относительные мощности Изл.МИ:", Pi)
        return Pi

    except Exception as e:
        # Если возникла ошибка, установить значения по умолчанию
        print(f"Error occurred: {e}. Setting default values.")
        z = 0
        y = 0
        a = np.array([1, 1, 1, 1])
        Pi = np.array([1, 1, 1, 1])
        return Pi
