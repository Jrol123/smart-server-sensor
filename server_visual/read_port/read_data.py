import serial
import io

from serial.serialutil import EIGHTBITS

# Константы
PERIPH_ERROR_INIT = "FAILED"
PERIPH_ERROR_READ = "Could not read temperature"
OK = "OK\n"
PERIPH_ERRORS = [PERIPH_ERROR_READ, PERIPH_ERROR_INIT]


class Controller:
    """
    Класс контроллера.

    Содержит id и геолокацию.

    ----------

    Геолокация пока-что не используется.

    :var id: id
    :type id: int
    :var geolocation: Геолокация.
    :type geolocation: str

    """

    def __init__(self, id: int, geolocation: str):
        """
        Класс порта.

        :param id:
        :param geolocation:
        """
        self.id = id
        self.geolocation = geolocation  # Пока не используется


class Port:
    """
    Класс порта.

    Включает в себя инициализацию и чтение данных.

    :var name: Название порта системы
    :type name: str
    :var port: Открытый порт, для ввода/вывода
    :type port: io.TextIOWrapper | None
    :var control: Контроллер, подключенный к данному порту
    :type control: Controller | None

    """

    def __init__(self, port: str):
        """
        Класс порта.

        :param port:
        """
        self.name = port
        self.port = None
        self.control = None

    def try_init(self) -> bool:
        """
        Попытка инициализации порта.

        В текущей версии baudrate и bytesize захардкодены

        :return: Статус инициализации

        """
        try:
            # TODO: Вынести параметры порта в отдельные переменные
            self.port = io.TextIOWrapper(serial.Serial(self.name, baudrate=115200, bytesize=EIGHTBITS, timeout=1),
                                         newline='\n')
            return True
        except:
            return False

    def read(self) -> bool | list[str, str] | bool:
        """
        Чтение данных с контроллера.

        В случае привязывания контроллера к порту происходит поиск первого среди уже созданных в глобальном массиве.

        В противном случае просто считывается температура.

        ----------

        В текущей версии проверка происходит только по длине.

        В случае инициализации происходит проверка на ошибки периферии.

        write не происходит, из-за чего приходится применять костыль с ожиданием,
        поэтому после инициализации должен пройти цикл, прежде чем произойдёт считывание температуры.

        :returns: bool статус или список, в случае вторичного чтения.

        """
        try:
            # ? Формат данных: Геолокация (пробел) id
            result = self.port.readline()

            print(result)

            result = result.replace('\n', '')

            # Обработка ошибки датчика
            if result in PERIPH_ERRORS or result == '':
                return False
            result = result.split(' ')

            # Считывание первой строку RIOT
            if len(result) > 2:
                result = self.port.readline().replace('\n', '').split(' ')

            # TODO: Сделать проверку не по длине, а по спец-символу

            # Если не привязан контроллер
            if self.control is None:
                self.port.write(OK)
                found = False
                # TODO: Вынести список контроллеров в не-глобальную переменную (?)
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
            # Происходит полный сброс из-за необходимости реинициализировать порт.
            self.control = None
            self.port = None
            return False


mass_ports = [Port('COM3'), Port('COM4'), Port('COM5')]
"""Список портов"""
existing_controllers = list[Controller]
"""Список проинициализированных контроллеров"""


def checker(result: list[str, str]) -> list[str, int] | None:
    """
    Проверка полученной информации из порта на корректность.

    Проверяется на то, является ли результат чтения списком,
     и если да, то можно ли переконвертировать температуру в формат int (т. е. целостность переданной информации).

    :param result: Результат чтения информации с порта.
    :return: В случае успеха возвращается полученная с порта информация с переконвертированной в int температурой.

    """
    if isinstance(result, list) and len(result) == 2:
        try:
            result[1] = int(result[1])
            return result
        except:
            return None
    return None


def port_cycle(ports: list[Port]) -> list[list[str, int]]:
    """
    Цикл опроса портов.

    :param ports: Список портов.
    :return: Массив показаний датчиков, содержащих местоположение + температуру.

    """
    output_data = []
    for port in ports:
        if port.port is None:
            state = port.try_init()
            if state:
                result = checker(port.read())
                if isinstance(result, list):
                    # Если прошла проверка
                    output_data.append(result)
        else:
            result = checker(port.read())
            if isinstance(result, list):
                # Если прошла проверка
                output_data.append(result)
    return output_data


def calc_temp(mass_data: list[list[str, int]]) -> float | None:
    """
    Вычисление температуры.

    В данный момент берётся среднее арифметическое.

    :param mass_data: Список данных с датчиков, содержащий их местоположение и температуру.

    :return: Температура.
    В случае отсутствия данных выводится None.

    """
    if len(mass_data) == 0:
        return None
    print(mass_data)
    return sum(int(i[1]) for i in mass_data) / (len(mass_data) * 100)


def read() -> tuple[float | None, int]:
    """
    Чтение температуры с портов.

    Функция-интерфейс.

    :return: Средняя температура (если есть), число задействованных датчиков.

    """
    data_output = port_cycle(mass_ports)

    temperature = calc_temp(data_output)
    return temperature, len(data_output)
