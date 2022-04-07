from flask import render_template, redirect, url_for, flash, request, abort
from projeto_folder import app, request_API_Sefaz, database, bcrypt
from projeto_folder.forms import FormCriarConta, FormLogin
from projeto_folder.models import Usuario
from flask_login import login_user, current_user,logout_user, login_required

lista_bairros_mcz = request_API_Sefaz.lista_bairros_mcz

@app.route('/')
def home():
    lista_postos = request_API_Sefaz.organizar_request()
    top10_postos = request_API_Sefaz.filtrar(lista_postos)
    return render_template('home.html', top10_postos=top10_postos, lista_bairros_mcz=lista_bairros_mcz)

@app.route('/criar_conta', methods= ['GET','POST'])
def criar_conta():
    form_criar = FormCriarConta()

    if form_criar.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criar.senha.data)
        usuario = Usuario(username=form_criar.username.data, email=form_criar.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash('Usuário criado com sucesso', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criar_conta.html', form_criar=form_criar, lista_bairros_mcz=lista_bairros_mcz)

@app.route('/login', methods=['GET','POST'])
def login():
    form = FormLogin()

    if form.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar_dados.data)
            print('Fez login!')
            flash('Login feito com sucesso', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))


    return render_template('login.html', form= form, lista_bairros_mcz=lista_bairros_mcz)


@app.route('/bairros/<bairro_nome>', methods=['GET', 'POST'])
@login_required
def bairros(bairro_nome):
    lista_bairros_mcz = request_API_Sefaz.lista_bairros_mcz
    lista_postos = request_API_Sefaz.organizar_request()
    top10_postos = request_API_Sefaz.filtrar(lista_postos, bairro_nome)
    return render_template('bairros.html', top10_postos=top10_postos, lista_bairros_mcz=lista_bairros_mcz)

@app.route('/sair')
def logout():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html', lista_bairros_mcz=lista_bairros_mcz)