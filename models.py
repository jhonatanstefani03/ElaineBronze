from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    tipo = db.Column(db.String(50))  # sessão única, pacote etc.
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50))
