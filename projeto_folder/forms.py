from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length, Email,equal_to,ValidationError
from projeto_folder.models import Usuario



class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário:', validators=[DataRequired()])
    email =StringField('Seu email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação de senha:', validators=[DataRequired(), equal_to('senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail em uso, escolha outro por favor.')

class FormLogin(FlaskForm):
    email =StringField('Seu email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar meus dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')

