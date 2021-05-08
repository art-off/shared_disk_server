from app import app, db


@app.shell_context_processors
def make_shell_context():
    return {'db': db}

#
#
# export OAUTHLIB_RELAX_TOKEN_SCOPE=1
# если вдруг будут траблы `вродеwarning scope has changed from "" to ""`
#
# export FLASK_ENV=development
#
#
#