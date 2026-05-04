import sqlite3 as sql
from flask import Flask, render_template, url_for, redirect, request, flash

def get_db():
    con = sql.connect('banco.db')
    con.row_factory = sql.Row
    return con

app = Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for('cadastrar'))

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    req = request.form
    if request.method == 'POST':
        nome = req.get('nome')
        email = req.get('email')
        senha = req.get('senha')
        con = get_db()
        cur = con.cursor()
        cur.execute('''
                    INSERT INTO usuarios VALUES (?, ?, ?, ?)''', (None, nome, email, senha) )
        con.commit()
        con.close()
        return redirect(url_for('cadastrar'))
    return render_template('cadastro.html')

@app.route('/listar', methods=['POST', 'GET'])
def listar():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM usuarios')
    usuarios = cur.fetchall()
    con.close()
    return render_template('listar.html', usuarios = usuarios)

@app.route('/editar/<email>', methods=['POST', 'GET'])
def editar(email):
    req = request.form
    con = get_db()
    cur = con.cursor()
    
    if request.method =='POST':
        novo_nome = req.get('nome')
        nova_senha = req.get('senha')

        cur.execute('UPDATE usuarios SET nome =?, senha = ? WHERE email = ?', (novo_nome, nova_senha, email))
        con.commit()
        con.close()
        return redirect(url_for('listar'))

    cur.execute('SELECT * FROM usuarios WHERE email = ?',(email,))
    usuario = cur.fetchone()
    con.commit()
    con.close()

    if usuario is None:
        return 'Usuário não encontrado', 404

    return render_template('editar.html', usuario = usuario)

@app.route('/excluir', methods=['POST', 'GET'])
def excluir():
    if request.method == 'POST':
        email = request.form.get('email')
        con = get_db()
        cur = con.cursor()
        cur.execute('DELETE FROM usuarios WHERE email = ?', (email,))
        con.commit()
        con.close()
        flash('Usuário removido!')
        return redirect(url_for('listar'))

    return render_template('excluir.html')

if __name__ == '__main__':
    app.secret_key='adm123'
    app.run(debug=True) 
