"""
    Tomado de https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
"""

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
basedir = os.path.abspath(os.path.dirname(__file__))
from config import enlace
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = enlace 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Matricula(db.Model):

    __tablename__ = 'matriculas'

    id = db.Column(db.Integer, primary_key=True)
    nombre_propietario = db.Column(db.String(200))
    placa = db.Column(db.String(200))
    anio_matricula = db.Column(db.String(25))
    valor_matricula = db.Column(db.Float(10), nullable=False) # este atributo no puede ser nulo


    def __repr__(self):
        return "Matricula: nombre del propietario=%s placa=%s año matricula=%s valor de matricula=%d" % (
                          self.nombre_propietario,
                          self.placa,
                          self.anio_matricula,
                          self.valor_matricula)

# vista

@app.route('/')
def index():
    matriculas = Matricula.query.all()
    return render_template('index.html', matriculas=matriculas)


@app.route('/<int:matricula_id>/')
def matricula(matricula_id):
    matriculas = Matricula.query.get_or_404(matricula_id)
    return render_template('matricula.html', matriculas=matriculas)


@app.route('/add/matricula/', methods=('GET', 'POST'))
def crear():
    if request.method == 'POST':
        nombre_propietario = request.form['nombre']
        placa = request.form['placa']
        anio_matricula = request.form['anio_ma']
        valor_matricula = request.form['val_ma']
        matriculacion = Matricula(nombre_propietario=nombre_propietario,
                          placa=placa,
                          anio_matricula=anio_matricula,
                          valor_matricula=valor_matricula,
                          )
        db.session.add(matriculacion)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear.html')


@app.route('/editar/matricula/<int:matricula_id>/', methods=('GET', 'POST'))
def editar(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)

    if request.method == 'POST':
        nombre_propietario = request.form['nombre']
        placa = request.form['placa']
        anio_matricula = request.form['anio_ma']
        valor_matricula = request.form['val_ma']

        matricula.nombre_propietario = nombre_propietario
        matricula.placa = placa
        matricula.anio_matricula = anio_matricula
        matricula.valor_matricula = valor_matricula
        db.session.add(matricula)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('editar.html', matricula=matricula)
