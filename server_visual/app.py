from flask import Flask, render_template, jsonify
from queue import Queue
from flask_sqlalchemy import SQLAlchemy

from read_data import read
import time
from threading import Thread

COUNT_STEP = 10

# Метки оси x для отображения данных
x = [i for i in range(0, COUNT_STEP)]

# Интервал получения данных с датчиков
SLEEP_TIME = 3

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Модель записи БД
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False, nullable=True)
    count_controllers = db.Column(db.Integer, unique=False, nullable=False)
    timestamp = db.Column(db.Integer, unique=False, nullable=False)  # Unix

    def __repr__(self):
        return f'<Record {self.temperature}>'


# Получение температуры с последующей записью в БД
def get_temp():
    with app.app_context():
        while True:
            temperature, count_controllers = read()
            db.session.add(Record(temperature=temperature, count_controllers=count_controllers, timestamp=time.time()))
            db.session.commit()
            time.sleep(SLEEP_TIME)


# Инициализация и запуск потока получения данных с датчиков
thread = Thread(target=get_temp)
thread.start()

# Инициализация таблиц БД
with app.app_context():
    db.create_all()


# Главная страница
@app.route('/')
def main_page():
    read()
    return render_template('index.html', context={'data': list(data_queue.queue)})


# Обновление данных
@app.route('/update', methods=['GET', 'POST'])
def update_data():
    with app.app_context():
        # Извлечение данных из БД
        data = Record.query.order_by(Record.timestamp.desc()).all()
        time_arr = [record.timestamp for record in data]
        temp_arr = [record.temperature for record in data]
        connected_mk_arr = [record.count_controllers for record in data]
        y = [record.temperature for record in Record.query.order_by(Record.timestamp.desc()).limit(COUNT_STEP
    ).all()[::-1]]
        # connected_mk = Record.query.order_by(Record.timestamp.desc()).first().count_controllers

        # Преобразование чисел в формат Python-friendly для сериализации в JSON
        data = {'x': x, 'y': y, 'cmk': connected_mk_arr, 'time': time_arr, 'temp': temp_arr}

        return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000)
