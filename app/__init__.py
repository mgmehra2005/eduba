from flask import Flask, app
from config import config

config_name="default"      # default is development
app = Flask(__name__)
app.config.from_object(config[config_name])

from app.routes import main
app.register_blueprint(main)

