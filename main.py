# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, 
# а пароль должен быть зашифрован.

from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = '77cd032d1d513c1c0efeaa6dbb71cf6d5b4b1a9b0139effcb3ed5125f9b0609e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    userfname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    


@app.route('/',methods=['GET', 'POST'])
def root():
    db.create_all()
    return render_template('index.html')

@app.route('/form',methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/print_db',methods=['GET'])
def print():
    users = User.query.all()
    if not users:
        context = {'users': None}
        return render_template('print_db.html', **context)
    context = {'users': users}
    return render_template('print_db.html', **context)



@app.route('/save_user_date/',methods=['POST'])
def save():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя','danger')
            return redirect(url_for('form'))
        if not request.form['mail']:
            flash('Введите почту','danger')
            return redirect(url_for('form'))
        if not request.form['fname']:
            flash('Введите фамилию','danger')
            return redirect(url_for('form'))
        if not request.form['password']:
            flash('Введите пароль','danger')
            return redirect(url_for('form'))
        name = request.form['name']
        fname = request.form['fname']
        mail = request.form['mail']
        users = User.query.all()
        for userN in users:
            if userN.email == mail:
                flash('Пользователь с данным почтовым адресом уже занесен в БД','danger')
                return redirect(url_for('form'))
        password = generate_password_hash(request.form['password'])
        user = User(username=name , userfname=fname , email=mail , password=password)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('root'))


if __name__=='__main__':
    app.run(debug=True)