from flask import flash, redirect, render_template, url_for
from app.frontend.forms import *

from flask_login import current_user

from flask import request
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.models.car import Car
from app.models.car_mark import CarMark
from app.models.user import User
from app.models.role import Role


def setup_routes(app, user_service):
    @app.route('/')
    def index():
        return render_template('index.html')
    

    @app.route('/login/', methods = ['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            user = user_service.get_user_by_id(form.id.data)
            if user:
                if user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    flash(f'Добро пожаловать, {user.name}', 'success')
                    app.logger.info(f"User loggined: {user.id}")
                    return redirect(url_for('index'))
                else:
                    flash('Неверный пароль', 'error')
            else:
                flash('Пользователь не найден', 'error')

        return render_template('login.html', form=form)
    

    @app.route('/logout/', methods = ['GET', 'POST'])
    @login_required
    def logout():
        app.logger.info(f"User loggouted: {current_user.id}")
        logout_user()
        flash('Вы вышли из системы', 'success')
        return redirect(url_for('index'))

        
    
