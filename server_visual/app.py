import socket
from flask import Flask, request, render_template, Response
from queue import Queue
from flask_sqlalchemy import SQLAlchemy


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

def get_ipv6_address(interface):
    import netifaces
    return netifaces.ifaddresses(interface)[netifaces.AF_INET6][0]['addr']

global_ipv6_address = get_ipv6_address('lo')  # замените 'eth0' на ваш сетевой интерфейс

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind((global_ipv6_address, 65536))


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
    data, addr = sock.recvfrom(1024)
    data_queue.put(data.decode())
    print(addr, list(data_queue.queue))
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
    data = request.data # request.get_json()
    temperature = data # str(data.get('temperature'))
    data_queue.put(temperature)
    if temperature:
        return "Data received"
    else:
        return "None"


if __name__ == '__main__':
    app.run(port=65536)
######################
#!!  ВОСТОРГАЕМСЯ  !!#
######################
