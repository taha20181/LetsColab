from flask import Blueprint, render_template
from flask import current_app as app

blog = Blueprint("blog", __name__)

@blog.route("/")
def index():

    app.logger.debug(app.config.get("ENV"))

    return """<h1>BLOGS...!!</h1><hr><a href="http://127.0.0.1:5000/">Profiles</a>"""