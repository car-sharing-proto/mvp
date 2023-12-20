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
from app.models.session_state import SessionState


def setup_routes(app, user_service, car_service, 
                 car_mark_service, use_session_service):
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
    

    @app.route('/service/start_inspection/', methods = ['POST','GET'])
    @login_required
    def start_inspection():
        id = int(request.args['id'])
        session = use_session_service.get_session_by_id(id)
        if not session:
            return 'session not found'
        if current_user.role != Role.Admin and \
            session.user_id != current_user.id:
            return abort(405)
        flash(use_session_service.start_inspection(id))
        return redirect(url_for('rent'))
    

    @app.route('/service/finish_rent/', methods = ['POST', 'GET'])
    @login_required
    def finish_rent():
        id = int(request.args['id'])
        session = use_session_service.get_session_by_id(id)
        if not session:
            return 'session not found'
        if current_user.role != Role.Admin and \
            session.user_id != current_user.id:
            return abort(405)
        flash(use_session_service.finish_active_rent(id))
        return redirect(url_for('rent'))
    
    @app.route('/service/reserve/', methods = ['POST','GET'])
    @login_required
    def reserve():
        user_id = int(request.args['user_id'])
        car_id = int(request.args['car_id'])
        car = car_service.get_car_by_id(car_id)
        user = user_service.get_user_by_id(user_id)
        if not car:
            return 'car not found'
        if not user:
            return 'user not found'
        flash(use_session_service.reserve(user_id, car_id))
        return redirect(url_for('rent'))


    
    @app.route('/service/activate_rent/', methods = ['POST','GET'])
    @login_required
    def activate_rent():
        id = int(request.args['id'])
        session = use_session_service.get_session_by_id(id)
        if not session:
            return 'session not found'
        if current_user.role != Role.Admin and \
            session.user_id != current_user.id:
            return abort(405)
        flash(use_session_service.start_active_rent(id))
        return redirect(url_for('rent'))
    

    @app.route('/service/pause_rent/', methods = ['POST','GET'])
    @login_required
    def pause_rent():
        id = int(request.args['id'])
        session = use_session_service.get_session_by_id(id)
        if not session:
            return 'session not found'
        if current_user.role != Role.Admin and \
            session.user_id != current_user.id:
            return abort(405)
        flash(use_session_service.pause_active_rent(id))
        return redirect(url_for('rent'))
    

    @app.route('/rent/', methods = ['GET', 'POST'])
    @login_required
    def rent():
        user_id = current_user.id
        session = use_session_service.get_user_current_session(user_id)

        if session:
            car = car_service.get_car_by_id(session.car_id)
            car_mark = car_mark_service.get_car_mark_by_id(car.mark_id)
            match session.state:
                case SessionState.Reserved:
                    return render_template(
                        'rent_reserved.html', 
                        mark=car_mark.mark,
                        model=car_mark.model,
                        number=car.number.upper(),
                        session_id=session.id)
                case SessionState.Inspection:
                    return render_template(
                        'rent_inspection.html', 
                        mark=car_mark.mark,
                        model=car_mark.model,
                        number=car.number.upper(),
                        session_id=session.id)
                case SessionState.Active:
                    return render_template(
                        'rent_active.html', 
                        mark=car_mark.mark,
                        model=car_mark.model,
                        number=car.number.upper(),
                        session_id=session.id)
                case SessionState.Paused:
                    return render_template(
                        'rent_paused.html', 
                        mark=car_mark.mark,
                        model=car_mark.model,
                        number=car.number.upper(),
                        session_id=session.id)
                case SessionState.Finished:
                    return 'ABOBA'
        else:
            form = RentForm()
            form.cars.choices = []
            variants = {}

            cars = car_service.get_all_free_cars()
            for car in cars:
                car_mark = car_mark_service.get_car_mark_by_id(car.mark_id)
                ans = f'{car_mark.mark} {car_mark.model} {car.number.upper()}'
                variants[ans] = car.id
                form.cars.choices.append(ans)

            if form.validate_on_submit():
                car_id = variants[form.cars.data]
                return redirect(
                    url_for('reserve', car_id=car_id, user_id=user_id))

            return render_template('rent.html', form=form)
        
        
    
