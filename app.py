from flask import Flask, render_template, request, redirect, url_for
  # importa o db daqui
from models import db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studio_bronze.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # inicializa o db com o app

from models import  Cliente, Agendamento
# Rotas...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes_page():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        tipo = request.form.get('tipo')
        novo_cliente = Cliente(nome=nome, telefone=telefone, tipo=tipo)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('clientes_page'))
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    clientes = Cliente.query.all()
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        data = request.form.get('data')
        horario = request.form.get('horario')
        tipo = request.form.get('tipo')
        if not cliente_id:
            return "Erro: cliente não selecionado", 400
        cliente_id = int(cliente_id)
        novo_agendamento = Agendamento(cliente_id=cliente_id, data=data, horario=horario, tipo=tipo)
        db.session.add(novo_agendamento)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('agendar.html', clientes=clientes)

@app.route('/Agendadas')
def lista_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template('agendadas.html', clientes=agendamentos)

from flask import request

@app.route('/agendamentos', methods=['GET', 'POST'])
def agendamentos():
    data_filtro = None
    agendamentos = []

    if request.method == 'POST':
        data_filtro = request.form.get('data')  # pega a data do formulário

        if data_filtro:
            agendamentos = Agendamento.query.filter_by(data=data_filtro).all()
        else:
            agendamentos = Agendamento.query.all()
    else:
        agendamentos = Agendamento.query.all()

    return render_template('agendamentos.html', agendamentos=agendamentos, data_filtro=data_filtro)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
