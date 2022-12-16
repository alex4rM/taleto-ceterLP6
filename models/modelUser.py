from models.entities.User import User


class ModelUser():

    @classmethod
    def login(self, conn, user):
        try:
            cursor= conn.cursor()
            sql="""SELECT id, usuario, contra_user, nombre, rolle  FROM usuario
            Where usuario = '{}'""".format(user.usuario)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.contra_user), row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, conn, id):
        try:
            cursor= conn.cursor()
            sql="SELECT id, usuario, nombre FROM usuario WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[1],None, row[2], None) 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)