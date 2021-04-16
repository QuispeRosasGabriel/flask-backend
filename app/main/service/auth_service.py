from app.main.model.user import User

class Auth:

    @staticmethod
    def login_user(data):
        try:
            # Select by email or username
            user = User.query.filter_by(email=data['username']).first()
            if not user:
                user = User.query.filter_by(username=data['username']).first()

            if user and user.check_password(data['password']):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'accessToken': auth_token
                    }
                    return response_object, 200
            else:
                response_object = 'Username or password does not match.'
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = 'Missing or Incorrect Required Information'
            return response_object, 400

    @staticmethod
    def get_logged_in_user(new_request):
            # get the auth token
            auth_token = new_request.headers.get('Authorization')
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    user = User.query.filter_by(id=resp).first()
                    if user:
                        response_object = {
                            'status': 'success',
                            'data':  user
                        }
                        return response_object, 200

            response_object = "Unauthorized"
            return response_object, 401