from app import app

from flask import make_response, request
from .utils import get_files, give_permissions

from .responses.file import FileSchema
from ..auth_utils import token_auth, get_token


@app.route('/files')
@token_auth.login_required
def files():
    token = get_token(request)
    folder = request.args.get('folder') or 'root'
    error, next_page_token, files = get_files(token, folder)

    if error is not None:
        return make_response({'error': 'credentials_is_not_valid'}, 405)

    return make_response({'next_page_token': next_page_token,
                          'files': FileSchema(many=True).dump(files)}, 200)


@app.route('/permission', methods=['POST'])
@token_auth.login_required
def permission():
    token = get_token(request)
    file_id = request.json.get('file_id')
    user_email = request.json.get('user_email')

    error = give_permissions(token, file_id, user_email)
    if error is not None:
        return make_response({'error': 'credentials_is_not_valid'}, 405)

    return make_response({}, 200)