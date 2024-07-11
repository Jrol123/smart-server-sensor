import serial
import io

from serial.serialutil import EIGHTBITS


class Controller:
    def __init__(self, id: int, geolocation: str):
        self.id = id
        self.geolocation = geolocation  # Пока не используется


class Port:
    def __init__(self, port: str):
        self.name = port
        self.port = None
        self.control = None

    def try_init(self) -> bool:
        try:
            self.port = io.TextIOWrapper(serial.Serial(self.name, baudrate=115200, bytesize=EIGHTBITS, timeout=1),
                                         newline='\n')
            return True
        except:
            return False

    def read(self) -> bool | tuple[str, int] | bool:
        try:
            # геолокация (пробел) id
            result = self.port.readline()
            # if len.result
            if self.control is None:
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
                return result[0], result[1]
        except:
            self.control = None
            return False


mass_ports = [Port('COM3'), Port('COM4')]  # Порт - инициализирован ли он - используется ли он

existing_controllers = []

inited_ports = {'COM3': None,
                'COM4': None}  # 'COM' - Port

hash_id = {}  # 'COM' - Controller


def port_cycle(ports: list[Port]):
    output_data = []
    for port in ports:
        if port.port is None:
            state = port.try_init()
            if state:
                output_data.append(port.read())
        else:
            output_data.append(port.read())
    return output_data


def calc_temp(mass_data: list[int]) -> float | None:
    if len(mass_data) == 0:
        return None
    return sum(mass_data) / (len(mass_data) * 100)


def read() -> tuple[float | None, int]:
    """

    :return: Средняя температура (если есть), число задействованны датчиков
    """
    data_output = port_cycle(mass_ports)
    # for port in mass_opened_ports:
    # data_output.append(port.read())

    temperature = calc_temp(data_output)
    return temperature, len(data_output)
