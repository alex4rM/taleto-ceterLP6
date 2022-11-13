from werkzeug.security import check_password_hash, generate_password_hash

class User():
    def __init__(self, usuario, contra_user, rolle, id_user) -> None:
        self.usuario = usuario
        self.contra_user = contra_user
        self.rolle = rolle
        self.id_user = id_user

    @classmethod
    def check_password(self, hashed_password,password):
        return check_password_hash(hashed_password, password)
print(generate_password_hash("suscribete"))