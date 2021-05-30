from app import app

from flask import make_response, request
from .utils import get_files

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
