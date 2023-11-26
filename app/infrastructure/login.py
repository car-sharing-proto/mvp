from app.usecases.user_register import user_register
from app.usecases.user_register import get_user
from app.usecases.user_register import get_user_by_id

def setup_loging(app, login_manager):
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.config['SECRET_KEY'] = 'thisisasecretkey'

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info(f"USER_ID IS {int(user_id)}")
        return get_user_by_id(int(user_id))
