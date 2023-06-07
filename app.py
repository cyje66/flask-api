from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import validates
import os
import re

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'test.db')

app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64))

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError(
                "Username is too short. Should be no less than 3 characters."
            )
        if len(username) > 32:
            raise ValueError(
                "Username is too long. Should be no longer than 32 characters."
            )
        return username


@app.route('/account', methods=['GET'])
def get_all_accounts():

    accounts = Account.query.all()

    output = []

    for account in accounts:
        account_data = {}
        account_data['username'] = account.username
        account_data['password'] = account.password
        output.append(account_data)

    return jsonify({'users': output}), 200


@app.route('/register', methods=["POST"])
def create_account():

    response = {
        'success': False,
        'reason': ''
    }

    try:
        data = request.get_json()

        if len(data['password']) < 8:
            raise ValueError(
                "Password is too short. Should be no less than 8 characters."
            )
        if len(data['password']) > 32:
            raise ValueError(
                "Password is too long. Should be no longer than 32 characters."
            )
        if not re.search(r'[A-Z]', data['password']):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r'[a-z]', data['password']):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r'\d', data['password']):
            raise ValueError(
                "Password must contain at least one digit."
            )

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        new_user = Account(username=data['username'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        response['success'] = True
        response['reason'] = 'Account Created.'
        response = make_response(jsonify(response))
        response.status_code = 201

        return response

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])

        if error == 'UNIQUE constraint failed: account.username':
            error = 'Username already exists.'

        response['success'] = False
        response['reason'] = error
        response = make_response(jsonify(response))
        response.status_code = 400

        return response

    except ValueError as e:
        error = str(e)

        response['success'] = False
        response['reason'] = error
        response = make_response(jsonify(response))
        response.status_code = 400

        return response

    except Exception as e:
        error = str(e)
        response['success'] = False
        response['reason'] = error
        response = make_response(jsonify(response))
        response.status_code = 500

        return response


@app.route('/login', methods=['POST'])
def login():
    response = {
        'success': False,
        'reason': ''
    }
    try:
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            response['reason'] = 'Username or password missing.'

            response = make_response(jsonify(response))
            response.status_code = 401

            return response

        account = Account.query.filter_by(username=auth.username).first()

        if not account:
            response['reason'] = 'Account not found. Please register before login.'

            response = make_response(jsonify(response))
            response.status_code = 401

            return response

        if account and check_password_hash(account.password, auth.password):
            response['success'] = True
            response['reason'] = 'Login successful.'

            response = make_response(jsonify(response))
            response.status_code = 200

            return response

        else:
            response['success'] = False
            response['reason'] = 'Invalid password.'

            response = make_response(jsonify(response))
            response.status_code = 401

            return response

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        response['reason'] = 'DB error. Please try again later.'

        response = make_response(jsonify(response))
        response.status_code = 500

        return response

    except Exception as e:
        error = str(e)
        response['reason'] = error
        response = make_response(jsonify(response))

        response.status_code = 500


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
