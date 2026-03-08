from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acuario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
base_de_datos = SQLAlchemy(app)


class Pez(base_de_datos.Model):
    id = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
    nombre = base_de_datos.Column(base_de_datos.String(100), nullable=False)
    descripcion = base_de_datos.Column(base_de_datos.String(200), nullable=False)
    imagen = base_de_datos.Column(base_de_datos.String(500), nullable=False)


with app.app_context():
    base_de_datos.create_all()

@app.route('/')
def mostrar_galeria_principal():

    lista_peces = Pez.query.all()
    return render_template('index.html', peces=lista_peces)

@app.route('/registrar', methods=['POST'])
def registrar_pez():

    nombre_form = request.form.get('nombre_del_pez')
    desc_form = request.form.get('descripcion_del_pez')
    img_form = request.form.get('url_de_la_imagen')

    nuevo_pez = Pez(nombre=nombre_form, descripcion=desc_form, imagen=img_form)
    base_de_datos.session.add(nuevo_pez)
    base_de_datos.session.commit()

    return redirect('/')

@app.route('/eliminar/<int:id_del_pez>')
def eliminar_pez(id_del_pez):
    pez_encontrado = Pez.query.get_or_404(id_del_pez)
    base_de_datos.session.delete(pez_encontrado)
    base_de_datos.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)