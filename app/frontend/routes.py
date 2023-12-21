from flask import flash, jsonify, make_response, redirect, render_template, url_for
from app.frontend.forms import *

from flask_login import current_user

from flask import request
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.models.car import Car
from app.models.car_mark import CarMark
from app.models.rent_mode import RentMode
from app.models.rent_responses import RentResponse
from app.models.user import User
from app.models.role import Role
from app.models.session_state import SessionState
from app.models.user_responses import UserResponse
from app.models.car_responses import CarResponse
from app.models.car_mark_responses import CarMarkResponse

import json


def setup_routes(app, user_service, car_service, 
                 car_mark_service, use_session_service, telemetry_service):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # region login
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
    # endregion

    
    # region rent
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
        response = use_session_service.finish_active_rent(id)
        if response == RentResponse.OpenDoors:
            flash('Ошибка, не все двери закрыты!', 'error')
            return redirect(url_for('rent'))
        
        flash(response)
        return redirect(url_for('finished', id=session.id))
    
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
        response = use_session_service.pause_active_rent(id)
        if response == RentResponse.OpenDoors:
            flash('Ошибка, не все двери закрыты!', 'error')
        else:
            flash(response)
        return redirect(url_for('rent'))
    

    @app.route('/finished/', methods = ['GET', 'POST'])
    @login_required
    def finished():
        session_id = int(request.args['id'])
        session = use_session_service.get_session_by_id(session_id)
        if session:
            car = car_service.get_car_by_id(session.car_id)
            car_mark = car_mark_service.get_car_mark_by_id(car.mark_id)
            return render_template(
                        'rent_finished.html', 
                        mark=car_mark.mark,
                        model=car_mark.model,
                        number=car.number.upper(),
                        session_id=session.id,
                        start_time=session.start_time,
                        end_time=session.end_time)
        else:
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
        else:
            form = RentForm()
            form.cars.choices = []
            variants = {}

            cars = car_service.get_all_free_cars()
            for car in cars:
                if car.rent_mode != RentMode.Rent and \
                    current_user.role == Role.User:
                    continue
                car_mark = car_mark_service.get_car_mark_by_id(car.mark_id)
                ans = f'{car_mark.mark} {car_mark.model} {car.number.upper()}'
                variants[ans] = car.id
                form.cars.choices.append(ans)

            if form.validate_on_submit():
                car_id = variants[form.cars.data]
                return redirect(
                    url_for('reserve', car_id=car_id, user_id=user_id))

            return render_template('rent.html', form=form)
    #endregion
    # region admin
    @app.route('/admin/')
    @login_required
    def admin():
        if current_user.role != Role.Admin:
            abort(405)
        return render_template('admin_panel.html')   
    
    @app.route('/admin/user_list/')
    @login_required
    def user_list():
        if current_user.role != Role.Admin:
            abort(405)
        users = user_service.get_all_users()
        return render_template('user_list.html', users=users)   
        
    @app.route('/admin/user_list/add_user', methods = ['GET', 'POST'])
    @login_required
    def add_user():
        if current_user.role != Role.Admin:
            abort(405)
        form = AddUserForm()
        form.role.choices = [role.value for role in Role]

        if form.validate_on_submit():
            name = str(form.name.data)
            id=int(form.id.data)
            password = str(form.password.data)
            role = str(form.role.data)
            new_user = User(id, role, name, password)
            result = user_service.register_user(new_user)
            if result == UserResponse.SuccessfullyAdded:
                flash(result.value, 'success')
                return redirect(url_for('user_list'))
            else:
                flash(result.value, 'error')
            
        return render_template('add_user.html', form=form)
    
    @app.route('/admin/user_list/edit_user', methods = ['GET', 'POST'])
    @login_required
    def edit_user():
        if current_user.role != Role.Admin:
            abort(405)
        id = int(request.args['user_id'])
        user = user_service.get_user_by_id(id)
        
        if user:
            choices = [role.value for role in Role]
            if user.role not in choices:
                user.role = choices[0]

            form = EditUserForm(name=user.name,
                                 password=user.password,
                                   role=user.role)
            form.role.choices = choices

            if form.validate_on_submit():
                name = str(form.name.data)
                password = str(form.password.data)
                role = str(form.role.data)
                new_user = User(id, role, name, password)
                result = user_service.update_user(new_user)
                if result == UserResponse.SuccessfullyUpdated:
                    flash(result.value, 'success')
                    return redirect(url_for('user_list'))
                else:
                    flash(result.value, 'error')

            return render_template('edit_user.html', form=form)
        
        return redirect(url_for('user_list'))
        
        
    
    @app.route('/admin/user_list/details_user')
    @login_required
    def details_user():
        if current_user.role != Role.Admin:
            abort(405)
        return '-'
    
    @app.route('/admin/user_list/delete_user', methods = ['DELETE'])
    @login_required
    def delete_user():
        if current_user.role != Role.Admin:
            abort(405)
        user_id = int(request.args['user_id'])
        result = user_service.remove_user_by_id(user_id)
        return make_response(jsonify(result.value), 200)
    
    @app.route('/admin/car_list/')
    @login_required
    def car_list():
        if current_user.role != Role.Admin:
            abort(405)
        cars = car_service.get_all_cars()
        records = []

        for car in cars:
            model = car_mark_service.get_car_mark_by_id(car.mark_id)
            records.append({
                'id' : car.id,
                'number' : car.number,
                'model' : f'{model.mark} {model.model}',
                'color' : model.color,
                'mode' : car.rent_mode,
                'is_free' : car.is_free
            })

        return render_template('car_list.html', cars=records) 
    
    @app.route('/admin/car_list/add_car/', methods = ['GET', 'POST'])
    @login_required
    def add_car():
        if current_user.role != Role.Admin:
            abort(405)
        marks = car_mark_service.get_all_car_marks()
        form=AddCarForm()
        form.mark_id.choices = []
        variants = {}
        for mark in marks:
            value = f'{mark.mark} {mark.model} {mark.color}'
            variants[value] = mark.id
            form.mark_id.choices.append(value)

        if form.validate_on_submit():
            car_id = int(form.id.data)
            mark_id = variants[form.mark_id.data]
            number = form.number.data
            new_car = Car(
                id=car_id, 
                mark_id=mark_id, 
                number=number,
                rent_mode=RentMode.Service.value,
                is_free=True)
            
            result = car_service.add_car(new_car)
            if result == CarResponse.SuccessfullyAdded:
                flash(result.value, 'success')
                return redirect(url_for('car_list'))
            else:
                flash(result.value, 'error')
            
        return render_template('add_car.html', form=form)
    
    
    @app.route('/admin/car_list/edit_car/', methods = ['GET', 'POST'])
    @login_required
    def edit_car():
        if current_user.role != Role.Admin:
            abort(405)
        id = int(request.args['car_id'])
        car = car_service.get_car_by_id(id)
        
        if car:
            marks = car_mark_service.get_all_car_marks()
            mark_id_choices = []
            mark_id_variants = {}
            for mark in marks:
                value = f'{mark.mark} {mark.model} {mark.color}'
                mark_id_variants[value] = mark.id
                mark_id_choices.append(value)
            mode_choices = [mode.value for mode in RentMode]
            if car.rent_mode not in mode_choices:
                car.rent_mode = mode_choices[0]
            mark = car_mark_service.get_car_mark_by_id(car.mark_id)
            form = EditCarForm(mark_id= f'{mark.mark} {mark.model} {mark.color}',
                               number=car.number,
                               mode=car.rent_mode)
            
            form.mode.choices = mode_choices
            form.mark_id.choices = mark_id_choices

            if form.validate_on_submit():
                car.mark_id = mark_id_variants[form.mark_id.data]
                car.number = form.number.data
                car.rent_mode = form.mode.data
                result = car_service.update_car(car)
                if result == CarResponse.SuccessfullyUpdated:
                    flash(result.value, 'success')
                    return redirect(url_for('car_list'))
                else:
                    flash(result.value, 'error')

            return render_template('edit_car.html', form=form)
        
        return redirect(url_for('car_list'))
    

    @app.route('/admin/car_list/details_car/', methods = ['GET'])
    @login_required
    def details_car():
        if current_user.role != Role.Admin:
            abort(405)
        car_id = int(request.args['car_id'])
        car = car_service.get_car_by_id(car_id)
        if car:
            car_telemetry = telemetry_service.get_all_telemetries_by_car_id(car_id)
            return render_template('car_telemetry.html', 
                                   car_number=car.number, 
                                   car_telemetry=car_telemetry)
        else:
            return redirect(url_for('car_list'))
    

    @app.route('/admin/car_list/delete_car/', methods = ['DELETE'])
    @login_required
    def delete_car():
        if current_user.role != Role.Admin:
            abort(405)
        car_id = int(request.args['car_id'])
        result = car_service.remove_car_by_id(car_id)
        return make_response(jsonify(result.value), 200)
    
    @app.route('/admin/car_mark_list/')
    @login_required
    def car_mark_list():
        if current_user.role != Role.Admin:
            abort(405)
        car_marks = car_mark_service.get_all_car_marks()
        return render_template('car_mark_list.html', car_marks=car_marks)   
    

    @app.route('/admin/car_mark_list/add_car_mark/', methods = ['GET', 'POST'])
    @login_required
    def add_car_mark():
        if current_user.role != Role.Admin:
            abort(405)
        form = AddCarMarkForm()
        if form.validate_on_submit():
            mark_id = int(form.id.data)
            model = form.model.data
            mark = form.mark.data
            color = form.color.data
            new_mark = CarMark(mark_id, model, mark, color)
            result = car_mark_service.add_car_mark(new_mark)
            if result == CarMarkResponse.SuccessfullyAdded:
                flash(result.value, 'success')
                return redirect(url_for('car_mark_list'))
            else:
                flash(result.value, 'error')
        return render_template('add_car_mark.html', form=form) 
    

    @app.route('/admin/car_mark_list/edit_car_mark/', methods = ['GET', 'POST'])
    @login_required
    def edit_car_mark():
        if current_user.role != Role.Admin:
            abort(405)
        mark_id = int(request.args['car_mark_id'])
        car_mark = car_mark_service.get_car_mark_by_id(mark_id)

        if car_mark:
            form = EditCarMarkForm(
                mark=car_mark.mark,
                model=car_mark.model,
                color=car_mark.color)
            if form.validate_on_submit():
                model = form.model.data
                mark = form.mark.data
                color = form.color.data
                new_mark = CarMark(mark_id, model, mark, color)
                result = car_mark_service.update_car_mark(new_mark)
                if result == CarMarkResponse.SuccessfullyUpdated:
                    flash(result.value, 'success')
                    return redirect(url_for('car_mark_list'))
                else:
                    flash(result.value, 'error')

            return render_template('edit_car_mark.html', form=form) 
        
        return redirect(url_for('car_mark_list'))

    @app.route('/admin/car_mark_list/details_car_mark/', methods = ['GET'])
    @login_required
    def details_car_mark():
        if current_user.role != Role.Admin:
            abort(405)
        return '-'
    

    @app.route('/admin/car_mark_list/delete_car_mark/', methods = ['DELETE'])
    @login_required
    def delete_car_mark():
        if current_user.role != Role.Admin:
            abort(405)
        mark_id = int(request.args['car_mark_id'])
        result = car_mark_service.remove_car_mark_by_id(mark_id)
        return make_response(jsonify(result.value), 200)

    # endregion
