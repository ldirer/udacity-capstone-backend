import json
from datetime import timezone, datetime
from flask import request
from flask_restless.helpers import url_for
from flask_restless.manager import APIManager
from flask.wrappers import Response
from pytz import UTC

from g import app, db
from g.models import Language, User, Attempt, UserLanguage

from g.translator import main_script

"""I tried flask_restless 1.xx (beta). I don't like that the response has so many nested levels (like a top-level "attributes" for the data we usually want!...
So I reverted in spite of some nice new features, like the ability to PATCH relationships directly on an object.
e.g. I can specify I want to add languages to a user by PATCHing on /api/user/5/languages.
"""

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Language, methods=['GET'])
# flask_restless v0.17 (no mo' include_methods afterwards)
api_manager.create_api(User, methods=['GET', 'POST'], include_methods=['attempts.language_id'])

api_manager.create_api(User, methods=['GET', 'POST', 'PUT', 'PATCH'])
api_manager.create_api(Attempt, methods=['GET', 'POST'], include_methods=['language_id'])
api_manager.create_api(UserLanguage, methods=['GET', 'POST'], include_methods=['language_name'])


@app.route("/")
def test():
    Language.query.filter_by(_id=1)
    return json.dumps({"Hello": "world"})


@app.route("/translation_script")
def translate():
    main_script(db)
    return "It's ok baby it's ok."


def get_last_update(user_id):
    """Get the timestamp for the latest data we have about a user. 
    0 if there's no action.
    """
    user_language = UserLanguage.query.filter_by(user_id=user_id).order_by(UserLanguage.created_timestamp.desc()).first()
    if user_language is None:
        return 0

    user_language_ts = user_language.created_timestamp.replace(tzinfo=UTC).timestamp()

    attempt = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.timestamp.desc()).first()
    attempt_ts = 0 if attempt is None else attempt.timestamp.replace(tzinfo=UTC).timestamp()

    return max(user_language_ts, attempt_ts)


CLIENT_TO_SERVER_SYNC = 'sync_to_server'
SERVER_TO_CLIENT_SYNC = 'sync_to_client'
CLIENT_TO_SERVER_USER_SYNC = 'sync_user_to_server'
ALREADY_IN_SYNC = 'already_in_sync'


@app.route("/polling")
def polling():
    user_google_id = request.args.get("user_google_id")

    existing_user = User.query.filter_by(google_id=user_google_id).first()

    last_update_client = int(request.args.get("last_update_unix"))

    # api_manager.created_apis_for['language']
    if not existing_user:
        # We want the new user and everything the client has got.
        return json.dumps({'action': CLIENT_TO_SERVER_USER_SYNC, 'urls': {"user": url_for(User)}})

    last_update_db = get_last_update(existing_user._id)
    if last_update_client > last_update_db:
        # We want the client to give us everything they got since our last update.
        # We send it the url so it can send PATCH requests directly on the right instance.
        return json.dumps({
            'action': CLIENT_TO_SERVER_SYNC, 
            'url': url_for(User, instid=existing_user._id),
            'last_update_unix': last_update_db
            })
    elif last_update_db > last_update_client:
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

        # We could imagine restricting the urls to those that actually have a fresher timestamp.
        return json.dumps({'action': SERVER_TO_CLIENT_SYNC, 
            'urls': {"attempt": attempts_update_url, "user_language": user_language_update_url}})
    else:
        # We have the same timestamp for last update: we're in sync.
        return json.dumps({'action': ALREADY_IN_SYNC, 'urls': {}})

