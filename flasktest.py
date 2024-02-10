from flask import Flask, Response, request, send_from_directory, send_file, render_template
from flask_socketio import SocketIO
from logic import ordne_rezensionen_in_json_openai as ordne
from logic import chatbot_openai as bot
from logic.csv_read import read_csv
import csv
import codecs
import json
import time
import ast
import logic.create_graphs as cg

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/graph/<path:path>/<path:subpath>')
def generate_graph(path, subpath):
    liste = json.loads(subpath)
    if liste == None:
        liste = []
    print(liste)
    img_script = cg.generate_plot_and_decode(type=path, categories=liste)
    return img_script

@app.route('/process/comments/csv', methods=['POST'])
def process_csv_comments():
    socketio.emit('processing_started', {'started': True}, namespace='/')
    csv_file = request.files["upload_comments_csv_file"]
    stream = codecs.iterdecode(csv_file.stream, "utf-8")
    comments = read_csv(stream)
    i = 1
    time_per_each = []
    time_avg = 0
    for key in comments:
        start = time.time()
        # time.sleep(8)
        returned_dic = ordne.ordne_in_json(key, comments[key])
        json_string=json.dumps(returned_dic)
        end = time.time()
        time_per_each.append(end - start)
        time_avg = sum(time_per_each) / len(time_per_each)
        socketio.emit('zeit', {'insgesamt' : time_avg*len(comments), 'till_end' : time_avg*(len(comments)-i)}, namespace='/')
        socketio.emit('processing_status_update', {'files': i, 'insgesamt': str(len(comments))}, namespace='/')
        socketio.emit('sortierter_kommentar', {'json_string': json_string}, namespace='/')
        i += 1

    return send_file("html/comment_hochladen_succes.html")
@socketio.on('connect')
def handle_connect():
    socketio.emit('processing_status_update', {'status': 'Connected'})

@app.route("/")
def hello_world():
    return send_file("html/index.html")


@app.route('/logic/data/<path:path>')
def send_datafile(path):
    return send_from_directory("logic/data", path)


@app.route("/html/<path:path>")
def send_report(path):
    return send_from_directory("html", path)


@app.route('/scripts/<path:path>')
def script(path):
    return send_from_directory("scripts", path)


@app.route('/html/styles/<path:path>')
def stylesheet(path):
    return send_from_directory("html/styles", path)

@app.route('/html/styles/chatbot.css')
def bot_init():
    cg.daten_in_json_hochladen()
    return send_from_directory("html/styles", 'chatbot.css')

@app.route('/send/bot/message', methods=['POST'])
def progress_user_message():
    data = request.get_json()
    print(data['prompt'])
    print(data['kontext'])
    answer =bot.answer(data['kontext'], data['prompt'])
    answer_json = json.dumps(answer)
    print(answer)
    if 'statistik' in answer:
        print(answer['statistik'])
    return answer_json

@app.route('/upload/json', methods=['POST'])
def upload_json():
    try:
        data = request.get_json()  # JSON-Daten aus der Anfrage abrufen
        with open('logic/data/data_file.json', 'w') as file:
            json.dump(data, file, indent=4)

        response = {'success': True}
        return response
    except Exception as e:
        return str(e), 400  # Fehlermeldung zurückgeben, falls ein Fehler auftritt


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    socketio.run(app)
