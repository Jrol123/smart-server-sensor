from flask import Flask, render_template, Response
from queue import Queue
from flask_sqlalchemy import SQLAlchemy
from read_data import start_init, read

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'<Record {self.temperature}>'


# Обработка контекста приложения
with app.app_context():
    # Создание всех таблиц базы данных
    db.create_all()


# Главная страница
@app.route('/')
def main_page():
    temperature, count_controllers = read()
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


if __name__ == '__main__':
    start_init()
    app.run(port=65536)
######################
# !!  ВОСТОРГАЕМСЯ  !!#
######################
