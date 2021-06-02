from . import app

from flask import request, make_response

from .utils import auth_user
from .auth_utils import token_auth, get_token

from .utils import register_worker, register_manager, register_customer

from .models import Worker, Customer
from .responses.worker import WorkerSchema
from .responses.customer import CustomerSchema


@app.route('/')
@token_auth.login_required
def hello():
    token = get_token(request)
    return token


@app.route('/registration/worker', methods=['POST'])
def registration_worker():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    profession_id = request.json.get('profession_id')

    if name is None \
        or password is None \
        or email is None \
        or profession_id is None:
        return make_response({'error': 'required params does not exist'}, 403)

    error = register_worker(name, email, password, profession_id)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'status': 'worker created'}, 200)


@app.route('/registration/manager', methods=['POST'])
def registration_manager():
    mname = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if mname is None \
        or password is None \
        or email is None:
        return make_response({'error': 'required params does not exist'}, 403)

    error = register_manager(mname, email, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'status': 'manager created'}, 200)


@app.route('/registration/customer', methods=['POST'])
def registration_customer():
    fname = request.json.get('first_name')
    mname = request.json.get('middle_name')
    lname = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')

    if fname is None \
        or mname is None \
        or lname is None \
        or email is None \
        or password is None:
        return make_response({'error': 'required params does not exist'}, 403)

    error = register_customer(fname, mname, lname, email, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'status': 'customer created'}, 200)


@app.route('/workers')
@token_auth.login_required
def workers():
    w = Worker.query.all()
    return make_response({'workers': WorkerSchema(many=True).dump(w)}, 200)


@app.route('/customers')
@token_auth.login_required
def customers():
    w = Customer.query.all()
    return make_response({'workers': CustomerSchema(many=True).dump(w)}, 200)


@app.route('/auth', methods=['POST'])
def auth():
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return make_response({'error': 'required params does not exist'}, 403)

    token, email, name, is_manager, error = auth_user(email, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'token': token,
                          'name': name,
                          'email': email,
                          'is_manager': is_manager}, 200)


@app.route('/auth/customer', methods=['POST'])
def auth_customer():
    email = request.json.get('email')
    password = request.json.get('password')

    cust = Customer.query.filter_by(email=email).first()

    if cust is None or not cust.check_password(password):
        return make_response({'error': 'invalid password or email'}, 403)
    return make_response({'id': cust.id})
