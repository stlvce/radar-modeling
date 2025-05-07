from datetime import datetime

def print_log(msg: str, from_address: str):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{formatted_datetime}")
    print(f"Сообщение: {msg}")
    print(f"Отправитель: {from_address}")