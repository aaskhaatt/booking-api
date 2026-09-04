from repositories.user_repository import *
from exceptions import *



def hash_password(password):
    return password

def verify_password(password, hashed_password):
    return password == hashed_password





def register_user_service(user_data, db):
    try:
        user = get_user_by_email(user_data.email, db)

    except UserNotFoundError:
        hashed_password = hash_password(user_data.password)
        return create_user(user_data.username, user_data.email, hashed_password, db)

    raise UserAlreadyExistsError()




def authenticate_user_service(email, password, db):
    try:
        user = get_user_by_email(email, db)
        
    except UserNotFoundError:
        raise InvalidCredentialsError()

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    return user

    

    