import os

from flask import Flask, render_template
from flask_migrate import Migrate

from models.db import db
from views.library import library_app

app = Flask(__name__)

CONFIG_OBJECT_PATH = "config.{}".format(os.getenv("CONFIG_NAME", "DevelopmentConfig"))
app.config.from_object(CONFIG_OBJECT_PATH)
db.init_app(app=app)
migrate = Migrate(app=app, db=db)

app.register_blueprint(library_app, url_prefix="/library")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
