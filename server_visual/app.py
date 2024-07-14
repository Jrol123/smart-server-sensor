from flask import Flask, render_template, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from queue import Queue
from threading import Thread
import time

from read_port import read

COUNT_STEP = 10
"""Количество меток для отображения данных"""

x = [i for i in range(0, COUNT_STEP)]
"""Метки оси x для отображения данных"""

SLEEP_TIME = 3
"""Интервал получения данных с датчиков"""

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

# TODO: Убрать очередь за ненадобностью.
data_queue = Queue()
"""Очередь с данными"""

# Подключение базы данных.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
"""База данных"""


class Record(db.Model):
    """
    Запись температуры.

    Для вычисления температуры см. `read_port`

    :var id: id записи.
    :var temperature: Вычисленная температура.
    :var count_controllers: Количество контроллеров.
    :var timestamp: Время снятия показаний с контроллеров.

    """
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False, nullable=True)
    count_controllers = db.Column(db.Integer, unique=False, nullable=False)
    timestamp = db.Column(db.Integer, unique=False, nullable=False)  # Unix

    def __repr__(self):
        return f'<Record {self.temperature}>'


def get_temp() -> None:
    """
    Получение температуры с последующей записью в БД.

    :return: Создаёт запись в базе данных.

    """
    # TODO: Вводить базу данных как аргумент функции (?)
    with app.app_context():
        while True:
            temperature, count_controllers = read()
            db.session.add(Record(temperature=temperature, count_controllers=count_controllers, timestamp=time.time()))
            db.session.commit()
            time.sleep(SLEEP_TIME)


# Инициализация таблиц БД.
with app.app_context():
    db.create_all()

# Инициализация и запуск потока получения данных с датчиков.
thread = Thread(target=get_temp)
thread.start()


# TODO: Сделать перехват ошибки thread-а с его последующим возобновлением.


@app.route('/')
def main_page() -> str:
    """
    Главная страница.

    :return: Заполненный template.

    """
    return render_template('index.html', context={'data': list(data_queue.queue)})


# Обновление данных.
@app.route('/update', methods=['GET', 'POST'])
def update_data() -> Response:
    """
    Обновление данных на странице.

    :return: Обновляет данные на `index.html`.

    """
    with app.app_context():
        # Извлечение данных из БД.
        data = Record.query.order_by(Record.timestamp.desc()).all()
        time_arr = [record.timestamp for record in data]
        temp_arr = [record.temperature for record in data]
        connected_mk_arr = [record.count_controllers for record in data]
        y = [record.temperature for record in Record.query.order_by(Record.timestamp.desc()).limit(COUNT_STEP
                                                                                                   ).all()[::-1]]

        # Преобразование чисел в формат Python-friendly для сериализации в JSON.
        data = {'x': x, 'y': y, 'cmk': connected_mk_arr, 'time': time_arr, 'temp': temp_arr}

        return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000)
