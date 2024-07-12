import serial
import io

from serial.serialutil import EIGHTBITS

# Константы
PERIPH_ERROR = "Could not read temperature"
OK = "OK\n"


# Класс контроллера
class Controller:
    def __init__(self, id: int, geolocation: str):
        self.id = id
        self.geolocation = geolocation  # Пока не используется


class Port:
    """
    Класс порта
    """

    def __init__(self, port: str):
        self.name = port
        self.port = None
        self.control = None

    def try_init(self) -> bool:
        """
        Попытка инициализации

        """
        try:
            self.port = io.TextIOWrapper(serial.Serial(self.name, baudrate=115200, bytesize=EIGHTBITS, timeout=1),
                                         newline='\n')
            return True
        except:
            return False

    def read(self) -> bool | list[str, str] | bool:
        """
        Чтение данных с МК
        """
        try:
            # ? Формат данных: Геолокация (пробел) id
            result = self.port.readline()

            print(result)

            result = result.replace('\n', '')

            # Обработка ошибки датчика
            if result == PERIPH_ERROR or result == '':
                return False
            result = result.split(' ')

            # Считывание первой строку RIOT
            if len(result) > 2:
                result = self.port.readline().replace('\n', '').split(' ')

            # Если не привязан контроллер
            if self.control is None:
                self.port.write(OK)
                found = False
                for control in existing_controllers:
                    if int(result[1]) == control.id:
                        found = True
                        self.control = control
                        break
                if not found:
                    self.control = Controller(int(result[1]), result[0])
                    existing_controllers.append(self.control)
                return True
            else:
                if len(result) == 1:
                    return [self.control.geolocation, result[0]]
                else:
                    return False
        except:
            self.control = None
            self.port = None
            return False


mass_ports = [Port('COM3'), Port('COM4'), Port('COM5')]  # Порт - инициализирован ли он - используется ли он

existing_controllers = []

inited_ports = {'COM3': None,
                'COM4': None,
                'COM5': None}  # 'COM' - Port

hash_id = {}  # 'COM' - Controller


def checker(result: list[str, str]) -> list[str, int] | None:
    if isinstance(result, list) and len(result) == 2:
        try:
            result[1] = int(result[1])
            return result
        except:
            return None
    return None


def port_cycle(ports: list[Port]):
    output_data = []
    for port in ports:
        if port.port is None:
            state = port.try_init()
            if state:
                result = checker(port.read())
                if isinstance(result, list):
                    output_data.append(result)
        else:
            result = checker(port.read())
            if isinstance(result, list):
                output_data.append(result)
    return output_data


def calc_temp(mass_data: list[str, int]) -> float | None:
    """
    Перевод полученной строки в число
    """
    if len(mass_data) == 0:
        return None
    print(mass_data)
    return sum(int(i[1]) for i in mass_data) / (len(mass_data) * 100)


def read() -> tuple[float | None, int]:
    """

    :return: Средняя температура (если есть), число задействованны датчиков
    """
    data_output = port_cycle(mass_ports)

    temperature = calc_temp(data_output)
    return temperature, len(data_output)
