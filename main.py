"""
The main file for running the dashboard server.
"""

import flask_login

from application_logic.dashboard_controller import app
from application_logic.dashboard_controller.authentication.User import User
from config import Config
from data.dashboard_persistency.facade.service import Service as Persistency_service

if __name__ == '__main__':
    persistency_service = Persistency_service('./database.db')

    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    login_manager = flask_login.LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(email):
        if persistency_service.get_user_by_email(email=email) is None:
            return

        user = User()
        user.id = email
        return user


    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('email')
        if persistency_service.get_user_by_email(email=email) is None:
            return

        user = User()
        user.id = email

        # DO NOT ever store passwords in plaintext 
        #  always compare password
        # hashes using constant-time comparison!
        user.is_authenticated = request.form['password'] == persistency_service.get_user_by_email(email)['password']

        return user

    app.run(host='0.0.0.0')
