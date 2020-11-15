from flask import Blueprint, render_template
from flask import current_app as app

user = Blueprint("user", __name__)

@user.route("/")
def index():

    app.logger.debug(app.config.get("ENV"))

    return "Hello world!"