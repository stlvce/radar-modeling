import numpy as np

# Функция для расчета относительных мощностей Изл.МИ
def calculate_relative_powers(z=0, y=0, dx=1, dz=1, a=[1, 1, 1, 1]):
    try:
        # Определяем необходимые массивы
        Mi_Z = np.array([50, -50, 0, 0])  # Значения Z
        Mi_Y = np.array([0, 0, 50, -50])   # Значения Y
        
        # Вычисляем временные значения
        tmpa = np.abs(Mi_Z + Mi_Y - z - y) / np.sqrt(2)
        tmpd = np.sqrt((Mi_Z - z) ** 2 + (Mi_Y - y) ** 2)
        
        # Расчет относительных мощностей
        Pi = a * tmpa * np.sqrt(tmpd ** 2 - tmpa ** 2) / 50
        
        return Pi
    
    except Exception as e:
        # Если возникла ошибка, установить значения по умолчанию
        print(f"Error occurred: {e}. Setting default values.")
        z = 0
        y = 0
        a = np.array([1, 1, 1, 1])
        Pi = np.array([1, 1, 1, 1])
        return Pi

# Пример вызова функции
z_val = 21  # пример значения для Mi.z
y_val = 0   # y по умолчанию
dx_val = 1  # dx по умолчанию
dz_val = 1  # dz по умолчанию
a_vals = [1, 1, 1, 1]  # все Изл.МИ включены

# Рассчитываем относительные мощности
relative_powers = calculate_relative_powers(z_val, y_val, dx_val, dz_val, a_vals)
print("Относительные мощности Изл.МИ:", relative_powers)
