def setup_loging(app, login_manager, user_service):
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.config['SECRET_KEY'] = 'thisisasecretkey'

    @login_manager.user_loader
    def load_user(user_id):
        user = user_service.get_user_by_id(int(user_id))
        app.logger.info(f"USER_ID IS {user.id}. NAME IS {user.name}")
        return user
