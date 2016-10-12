import json
from datetime import timezone, datetime
from flask import request
from flask.ext.restless.helpers import url_for
from flask.ext.restless.manager import APIManager
from flask.wrappers import Response
from pytz import UTC

from g import app, db
from g.models import Language, User, Attempt, UserLanguage

from g.translator import main_script

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Language, methods=['GET'], max_results_per_page=-1)
api_manager.create_api(User, methods=['GET', 'POST'])
api_manager.create_api(Attempt, methods=['GET', 'POST'])
api_manager.create_api(UserLanguage, methods=['GET', 'POST'])


@app.route("/")
def test():
    Language.query.filter_by(_id=1)
    return json.dumps({"Hello": "world"})


@app.route("/translation_script")
def translate():
    main_script(db)
    return "It's ok baby it's ok."


def get_last_update(user_id):
    user_language_ts = UserLanguage.query.filter_by(user_id=user_id).order_by(
        "created_timestamp").first().created_timestamp
    if user_language_ts is None:
        return 0

    attempt_ts = Attempt.query.filter_by(user_id=user_id).order_by("timestamp").first().timestamp
    if attempt_ts is None:
        return user_language_ts

    return max(user_language_ts.replace(tzinfo=UTC).timestamp(),
               attempt_ts.replace(tzinfo=UTC).timestamp())


CLIENT_TO_SERVER_SYNC = 'sync_to_server'
SERVER_TO_CLIENT_SYNC = 'sync_to_client'
CLIENT_TO_SERVER_USER_SYNC = 'sync_user_to_server'


@app.route("/polling")
def polling():
    user_google_id = request.args.get("user_google_id")

    existing_user = User.query.filter_by(google_id=user_google_id).first()

    last_update_client = int(request.args.get("last_update_unix"))

    # api_manager.created_apis_for['language']
    if not existing_user:
        # We want the new user and everything the client has got.
        return json.dumps({'action': CLIENT_TO_SERVER_USER_SYNC, 'urls': [url_for(User)]})

    last_update_db = get_last_update(existing_user._id)
    if not existing_user or last_update_client > last_update_db:
        # We want the client to give us everything they got since our last update.
        return json.dumps({'action': CLIENT_TO_SERVER_SYNC, 'last_update_unix': last_update_db})
    else:
        # We need to send updates to the client

        # We should probably be packing all the changes here and send them directly.
        # However I don't know how to call the flask-restless underlying view functions (!!)
        # So I make a list of urls for the client to call.
        attempts_update_url = "{}{}".format(
            url_for(Attempt),
            '?q={"filters":[{"name":"timestamp","op":">","val":"%s"}, '
            '{"name": "user_id", "op": "==", "val": %i}]}'
            % (datetime.fromtimestamp(last_update_client, tz=UTC), existing_user._id))

        user_language_update_url = "{}{}".format(
            url_for(UserLanguage),
            '?q={"filters":[{"name":"created_timestamp","op":">","val":"%s"}, '
            '{"name": "user_id", "op": "==", "val": %i}]}'
            % (datetime.fromtimestamp(last_update_client, tz=UTC), existing_user._id))

        return json.dumps({'action': SERVER_TO_CLIENT_SYNC, 'urls': [attempts_update_url, user_language_update_url]})
