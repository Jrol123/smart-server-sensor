from flask import Flask, render_template, Response, jsonify
from queue import Queue
from flask_sqlalchemy import SQLAlchemy

from read_data import read
import time
from threading import Thread

import numpy as np

x = np.arange(0, 10, 0.1)

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

# подключение базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False, nullable=True)
    count_controllers = db.Column(db.Integer, unique=False, nullable=False)
    timestamp = db.Column(db.Integer, unique=False, nullable=False)  # Unix

    def __repr__(self):
        return f'<Record {self.temperature}>'


def get_temp():
    with app.app_context():
        while True:
            temperature, count_controllers = read()
            db.session.add(Record(temperature=temperature, count_controllers=count_controllers, timestamp=time.time()))
            # print(temperature, count_controllers)
            db.session.commit()
            time.sleep(SLEEP_TIME)


thread = Thread(target=get_temp)
thread.start()

with app.app_context():
    db.create_all()


# Главная страница
@app.route('/')
def main_page():
    read()
    return render_template('index.html', context={'data': list(data_queue.queue)})


@app.route('/update', methods=['GET', 'POST'])
def update_data():
    with app.app_context():
        # Извлечение данных из БД
        data = Record.query.order_by(Record.timestamp.desc()).all()
        time_arr = [record.timestamp for record in data]
        temp_arr = [record.temperature for record in data]
        y = [record.temperature for record in Record.query.order_by(Record.timestamp.desc()).limit(100).all()[::-1]]
        connected_mk = Record.query.order_by(Record.timestamp.desc()).first().count_controllers

        # Преобразование чисел в формат Python-friendly для сериализации в JSON
        data = {'x': x.tolist(), 'y': y, 'cmk': connected_mk, 'time': time_arr, 'temp': temp_arr}

        return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000)
