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
    nombre_p = db.Column(db.String(200))
    placa = db.Column(db.varchar(7))
    año = db.Column(db.datetime)
    costo_m = db.Column(db.Float(10), nullable = False)  # este atributo no puede ser nulo


    def __repr__(self):
        return "Matricula: nombre_p=%s placa=%s año=%s costo_m=%s" % (
                          self.nombre_p,
                          self.placa,
                          self.año,
                          self.costo_m)

# vista

@app.route('/')
def index():
    matriculas = Matricula.query.all()
    return render_template('index.html', matriculas=matriculas)


@app.route('/<int:docente_id>/')
def docente(matricula_id):
    matriculas = Matricula.query.get_or_404(matricula_id)
    return render_template('matricula.html', matriculas=matriculas)


@app.route('/add/matricula/', methods=('GET', 'POST'))
def crear():
    if request.method == 'POST':
        nombre_p= request.form['nombre_p']
        placa = request.form['placa']
        año = request.form['año']
        costo_m = request.form['costo_m']
        matricula = Matricula(nombre_p=nombre_p,
                          placa=placa,
                          año=año,
                          costo_m=costo_m
                          )
        db.session.add(matricula)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear.html')


@app.route('/editar/matricula/<int:matricula_id>/', methods=('GET', 'POST'))

def editar(matricula_id):
    matriculas = Matricula.query.get_or_404(matricula_id)

    if request.method == 'POST':
        nombre_p= request.form['nombre_p']
        placa = request.form['placa']
        año = request.form['año']
        costo_m = request.form['costo_m']

        matriculas.nombre_p = nombre_p
        matriculas.placa = placa
        matriculas.año = año
        matriculas.costo_m = costo_m
        db.session.add(matriculas)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('editar.html', matriculas=matriculas)
