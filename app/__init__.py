from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel(app)

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	migrate.init_app(app)
	login.init_app(app)
	mail.init_app(app)
	boostrap.init_app(app)
	moment.init_app(app)
	babel.init_app(app)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	#### EMAIL SERVER PARAMS - CONFIGURE THESE AS ENVIRONMENT VARS (dotenv) ####
	mailserver = app.config['MAIL_SERVER']
	mailusername = app.config['MAIL_USERNAME']
	mailpasswd = app.config['MAIL_PASSWORD']
	mailusetls = app.config['MAIL_USE_TLS']
	mailport = app.config['MAIL_PORT']
	adminemails = app.config['ADMIN_EMAILS']

	if not app.debug and not app.testing:
		#### CONFIGURE SMTP EMAIL HANDLER TO REPORT ERRORS ####
		if mailserver:
			auth = None
			if mailusername or mailpasswd:
				auth = (mailusername, mailpasswd)
			secure = None
			if mailusetls:
				secure = ()
			mail_handler = SMTPHandler(
				mailhost=(mailserver, mailport),
				fromaddr='no-reply@' + mailserver,
				toaddrs=adminemails,
				credentials=auth,
				secure=secure,
				subject='An error was logged...')
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)

		#### CONFIGURE FILE HANDLER TO LOG ERRORS ####
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler(
			'logs/microblog.log',
			maxBytes=10240,
			backupCount=10)
		file_handler.setFormatter(
			logging.Formatter(
				'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
			)
		)
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info("Microblog startup")

	return app

@babel.localeselector
def get_local():
	return request.accept_languages.best_match(current_app.config['LANGUAGES'])
	# return 'es' # for testing

from app import models#, routes, errors
