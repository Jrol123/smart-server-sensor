from flask import Flask, render_template, Response
from queue import Queue
from flask_sqlalchemy import SQLAlchemy
import serial
import io
import time
from threading import Thread

from serial.serialutil import EIGHTBITS

#  ______     __  __     ______        ______     ______     ______     __
# /\  __ \   /\ \/\ \   /\  == \      /\  ___\   /\  __ \   /\  __ \   /\ \
# \ \ \/\ \  \ \ \_\ \  \ \  __<      \ \ \____  \ \ \/\ \  \ \ \/\ \  \ \ \____
#  \ \_____\  \ \_____\  \ \_\ \_\     \ \_____\  \ \_____\  \ \_____\  \ \_____\
#   \/_____/   \/_____/   \/_/ /_/      \/_____/   \/_____/   \/_____/   \/_____/

#  ______   ______     ______       __     ______     ______     ______
# /\  == \ /\  == \   /\  __ \     /\ \   /\  ___\   /\  ___\   /\__  _\
# \ \  _-/ \ \  __<   \ \ \/\ \   _\_\ \  \ \  __\   \ \ \____  \/_/\ \/
#  \ \_\    \ \_\ \_\  \ \_____\ /\_____\  \ \_____\  \ \_____\    \ \_\
#   \/_/     \/_/ /_/   \/_____/ \/_____/   \/_____/   \/_____/     \/_/

app = Flask(__name__)

# Очередь с данными
data_queue = Queue()

# Подключение базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'
db = SQLAlchemy(app)

s = serial.Serial('COM3', baudrate=115200, bytesize=EIGHTBITS, timeout=1)
sio = io.TextIOWrapper(s, newline='\n')


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'<Record {self.temperature}>'


# Обработка контекста приложения
with app.app_context():
    # Создание всех таблиц базы данных
    db.create_all()


def something():
    while True:
        print("Здесь выполняй что хош")
        time.sleep(2)


thread = Thread(target=something)
thread.start()


# Главная страница
@app.route('/')
def main_page():
    temperature = sio.readline()
    print(temperature)
    data_queue.put(temperature)
    return render_template('index.html', context={'data': list(data_queue.queue)})


# Маршрут для установки соединения SSE
@app.route('/stream-data')
def stream_data():
    def generate_data():
        # Извлечение данных из очереди
        if not data_queue.empty():
            data = data_queue.get()
            yield f"data: {data}\n\n"

    return Response(generate_data(), content_type='text/event-stream')


# Получение данных из POST запроса и помещение в очередь
@app.route('/postt', methods=['POST'])
def process_post_request():
    print("fafaff")
    data = sio.readline()  # request.get_json()
    temperature = data  # str(data.get('temperature'))
    data_queue.put(temperature)
    if temperature:
        return "Data received"
    else:
        return "None"


if __name__ == '__main__':
    app.run(port=65536)
######################
# !!    СТРАДАЕМ   !!#
######################
