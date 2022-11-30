from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, usuario, contra_user, nombre, rolle) -> None:
        self.id = id
        self.usuario = usuario
        self.contra_user = contra_user
        self.nombre = nombre
        self.rolle = rolle

    @classmethod
    def check_password(self, hashed_password,password):
        return check_password_hash(hashed_password, password)

#print(generate_password_hash("suscribete"))