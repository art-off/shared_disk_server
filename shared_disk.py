from app import app, db
from app.models import User, Credentials


@app.shell_context_processors
def make_shell_context():
    return {'db': db, 'User': User, 'Credentials': Credentials}

#
#
# export OAUTHLIB_RELAX_TOKEN_SCOPE=1
# если вдруг будут траблы `вродеwarning scope has changed from "" to ""`
#
# export FLASK_ENV=development
#
#
#