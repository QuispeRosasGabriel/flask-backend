from .. import db, flask_bcrypt
import datetime
import jwt
from ..config import key

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    firstName = db.Column(db.String(255), unique=False, nullable=False)
    lastName = db.Column(db.String(255), unique=False, nullable=False)
    passwordHash = db.Column(db.String(100))
    createDate = db.Column(db.DateTime(timezone=True), unique=False, nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.passwordHash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod  
    def decode_auth_token(auth_token):
            """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
            """
            try:
                payload = jwt.decode(auth_token, key, algorithms=["HS256"])
                return payload['sub']
            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'