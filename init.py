from flask import flask
from config import config
from flask_sqlalchemy import SQLALchemy
from flask_migrate import Migrate

app=flask(__name__)
app.comfig.form_object(config)
db=SQLALchemy(app)
migrate=Migrate(app,db)

from app import routes,models
