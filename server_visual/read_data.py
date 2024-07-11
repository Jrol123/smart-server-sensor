import serial
import io

from serial.serialutil import EIGHTBITS

mass_ports = ['COM3', 'COM4']

mass_opened_ports = []


class Controller:
    def __init__(self, id: int, geolocation: str, port: io.TextIOWrapper):
        self.id = id
        self.geolocation = geolocation  # Пока не используется
        self.port = port

    def read(self) -> int | str:
        self.port.readline()

    def set_geo(self, new_geolocation:str) -> int:
        self.geolocation = new_geolocation
        if self.geolocation == new_geolocation:
            return 200


def start_init():
    for port in mass_ports:
        try:
            mass_opened_ports.append(Controller(0,
                                                "Vladivostok",
                                                io.TextIOWrapper(
                                                    serial.Serial(port, baudrate=115200, bytesize=EIGHTBITS, timeout=1),
                                                    newline='\n')))
        finally:
            continue


def read() -> tuple[int | None, int]:
    """

    :return: Температура (если есть), число задействованны датчиков
    """
    data_output = []
    for port in mass_opened_ports:
        data_output.append(port.read())

    temperature = None
    return temperature, len(data_output)
