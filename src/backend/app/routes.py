from flask import Flask, request, jsonify, render_template
from datetime import datetime
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB("banco_de_dados.json")

# Lista para armazenar os logs de acesso
logs = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Rota para o ping
@app.route('/ping', methods=['GET'])
def ping():
    logs.append({'timestamp': datetime.now().isoformat(), 'endpoint': '/ping', 'method': 'GET'})
    return jsonify({'resposta': 'pong'})

@app.route('/echo', methods=['GET','POST']) #Define
def echo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        db.insert({'Dados': nome})  #Salva
    posts = db.all()
    return render_template('echo.html',nome=nome, posts=posts) #Retorna

# # Rota para o echo
# @app.route('/echo', methods=['POST'])
# def echo():
#     data = request.json
#     logs.append({'timestamp': datetime.now().isoformat(), 'endpoint': '/echo', 'method': 'POST', 'data': data})
#     resposta = data.get('dados', '') if data else ''
#     return jsonify({'resposta': resposta})


# Rota para exibir o dashboard
@app.route('/dash')
def dashboard():
    return render_template('dashboard.html', logs=logs)

# Rota para fornecer informações sobre os logs
@app.route('/info')
def info():
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
