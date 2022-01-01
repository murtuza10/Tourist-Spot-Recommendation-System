import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask import render_template,redirect,request,url_for,Flask
from flask_dance.contrib.google import make_google_blueprint,google
from flask_dance.contrib.twitter import make_twitter_blueprint,twitter
from flask_dance.contrib.facebook import make_facebook_blueprint,facebook


app= Flask(__name__)
Bootstrap(app)

login_manager = LoginManager()
app.config['SECRET_KEY'] = 'mysecretkey'

#SQL DATABASE SECTION

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'users.user'

from Project.users.views import users_blueprint
from Project.admins.views import admins_blueprint

app.register_blueprint(users_blueprint,url_prefix='/users')
app.register_blueprint(admins_blueprint,url_prefix='/admins')

google_blueprint = make_google_blueprint(client_id='156026091265-u5tlf5srj1ron927kkpbs46913gtifsp.apps.googleusercontent.com',client_secret='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',offline=True,scope=['profile','email'],redirect_to = 'users.login_google')
app.register_blueprint(google_blueprint,url_prefix='/login')
twitter_blueprint = make_twitter_blueprint(api_key='yp8b1rMHabc4EMdGiALTxbwvR',api_secret='NeqHfrxBQkV4p6ai7SltAnlVmNz2UfG8IkiYFAv4t0tX9F5zGi',redirect_to = 'users.login_twitter')
app.register_blueprint(twitter_blueprint,url_prefix='/login')
facebook_blueprint = make_facebook_blueprint(client_id='7082073501810301',client_secret='125a5f2f09a64533c15fe3dec4e51395',scope='email',redirect_to = 'users.login_facebook')
app.register_blueprint(facebook_blueprint,url_prefix='/login')

#secret 125a5f2f09a64533c15fe3dec4e51395
#id 7082073501810301

# google_blueprint = make_google_blueprint(client_id='156026091265-u5tlf5srj1ron927kkpbs46913gtifsp.apps.googleusercontent.com',client_secret='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',offline=True,scope=['profile','email'])
# users_blueprint.register_blueprint(google_blueprint,url_prefix='/login')
# twitter_blueprint = make_twitter_blueprint(api_key='yp8b1rMHabc4EMdGiALTxbwvR',api_secret='NeqHfrxBQkV4p6ai7SltAnlVmNz2UfG8IkiYFAv4t0tX9F5zGi')
# users_blueprint.register_blueprint(twitter_blueprint,url_prefix='/login')
