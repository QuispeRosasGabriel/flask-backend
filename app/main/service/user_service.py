import datetime

from app.main import db
from app.main.model.user import User

from sqlalchemy import or_

def save_new_user(data):
    user = User.query.filter( or_( (User.email == data['email']), (User.username == data['username']) ) ).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            createDate=datetime.datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    else:
        return None


def get_all_users():
    return User.query.all()


def get_a_user(id):
    user = User.query.filter_by(id=int(id)).first()
    return user
