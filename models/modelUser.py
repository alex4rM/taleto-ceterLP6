from models.entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor=db.get_db().cursor()
            sql="""Select id, usuario, contra_user, rolle, id_user FROM usuarios
            Where usuario = '{}'""".format(user.usuario)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password), row[3])
                return user
        except Exception as ex:
            raise Exception(ex)