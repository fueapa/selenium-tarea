from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Datos en memoria (lista simple)
usuarios = []

@app.route('/')
def index():
        return render_template('index.html', usuarios=usuarios, enumerate=enumerate)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        # Guardar nuevo usuario
        usuarios.append({'nombre': nombre, 'email': email})
        return redirect(url_for('index'))
    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if id < 0 or id >= len(usuarios):
        return "Usuario no encontrado", 404
    if request.method == 'POST':
        usuarios[id]['nombre'] = request.form['nombre']
        usuarios[id]['email'] = request.form['email']
        return redirect(url_for('index'))
    return render_template('editar.html', usuario=usuarios[id], id=id)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if id < 0 or id >= len(usuarios):
        return "Usuario no encontrado", 404
    usuarios.pop(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
