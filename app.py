from flask import Flask, request, render_template, redirect
from datetime import datetime
app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form.get('task'):
            return render_template('index.html', msg = 'Ingresa una tarea!')
        else:
            fecha = datetime.now()
            fecha_tarea = fecha.date()
            nueva_tarea = Tarea(descripcion = request.form.get('task'), fecha_creacion = datetime.now() )
            db.session.add(nueva_tarea)
            db.session.commit()
            return render_template('index.html', tareas = Tarea.query.all())
    else:
        return render_template('index.html', tareas = Tarea.query.all())

@app.route('/completar/<int:tarea_id>', methods=['POST'])
def completar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    tarea.completada = True
    tarea.fecha_finalizacion = datetime.utcnow()
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Hubo un problema completando tu tarea'
    

@app.route('/eliminar/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    
    try:
            db.session.delete(tarea)
            db.session.commit()
            return redirect('/')
    except:
        
        return 'Hubo un problema eliminando la tarea'
@app.route('/editar/<int:tarea_id>', methods = ['GET','POST'])        
def editar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)

    if request.method == 'POST':
        nueva_descripcion = request.form.get('descripcion')

        if nueva_descripcion:
            tarea.descripcion = nueva_descripcion
            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'Hubo un problema actualizando la tarea'
        else:
            return 'La descripción no puede estar vacía'

    return render_template('editar.html', tarea=tarea)
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
