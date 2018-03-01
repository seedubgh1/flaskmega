from flask import Flask
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

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

#### EMAIL SERVER PARAMS - CONFIGURE THESE AS ENVIRONMENT VARS ####
mailserver = app.config['MAIL_SERVER']
mailusername = app.config['MAIL_USERNAME']
mailpasswd = app.config['MAIL_PASSWORD']
mailusetls = app.config['MAIL_USE_TLS']
mailport = app.config['MAIL_PORT']
adminemails = app.config['ADMIN_EMAILS']

if not app.debug:
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

from app import routes, models, errors
