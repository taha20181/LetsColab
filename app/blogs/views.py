from flask import Blueprint, render_template
from flask import current_app as app

blog = Blueprint("blog", __name__)

@blog.route("/")
def index():

    app.logger.debug(app.config.get("ENV"))

    return "Hello world!"