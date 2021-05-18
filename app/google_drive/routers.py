from app import app

from flask import make_response, request
import flask

from .auth_utils import (get_authorization_url_ans_store_state,
                         fetch_and_store__credentials)
from .utils import (get_credentials,
                    get_files)

from .responses.file import FileSchema
from ..auth_utils import token_auth, get_token


@app.route('/files')
@token_auth.login_required
def files():
    token = get_token(request)
    folder = request.args.get('folder') or 'root'
    next_page_token, files = get_files(token, folder)
    return make_response({'next_page_token': next_page_token,
                          'files': FileSchema(many=True).dump(files)}, 200)

