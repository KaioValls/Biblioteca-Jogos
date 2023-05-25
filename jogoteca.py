from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = "KAIOVALLS"

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

    def __str__(self):
        # só para testar toString()
        return self.nome+ ' ,'+ self.categoria + ' ,'+ self.console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Kaio','Valls','sim123')
usuario2 = Usuario('Jorge','Sampaio','nao123')
usuario3 = Usuario('Gabriel','Underline','under')

usuarios = { usuario1.nickname : usuario1 ,
             usuario2.nickname : usuario2 ,
             usuario3.nickname : usuario3 }

jogo1 = Jogo('CSGO', 'FPS', 'Computador')
jogo2 = Jogo('Skyrim', 'Aventura', 'Computador')
jogo3 = Jogo('Valorant', 'FPS', 'Computador')

lista = [ jogo1,jogo2, jogo3]

@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Jogos', jogos = lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        flash('Deve realizar o login primeiramente')
        return redirect('/login')
    return render_template('novo.html', titulo = 'Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    return render_template('login.html', titulo = 'Login')

@app.route('/login/autenticar', methods = ['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com Sucesso!')
            return redirect(url_for('novo'))

    flash('Usuario não logado')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('index'))


app.run(debug = True)
