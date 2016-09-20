import json
from flask.ext.restless.manager import APIManager

from g import app, db
from g.models import Language, User, Attempt

from g.translator import main_script

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Language, methods=['GET'], max_results_per_page=-1)
api_manager.create_api(User, methods=['GET', 'POST'])
api_manager.create_api(Attempt, methods=['GET', 'POST'])


@app.route("/")
def test():
    Language.query.filter_by(_id=1)
    return json.dumps({"Hello": "world"})


@app.route("/translation_script")
def translate():
    main_script(db)
    return "It's ok baby it's ok."

