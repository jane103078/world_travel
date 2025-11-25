import bcrypt


class User:
    __username = ""
    __hash = ""

    def __init__(self, username, hash):
        self.__username = username
        self.__hash = hash

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "username": self.__username,
            "hash": self.__hash,
        }

    @classmethod
    def build(cls, dict):
        return cls(dict["username"], dict["hash"])

    def get_key(self):
        return self.__username.lower()

    def get_username(self):
        return self.__username

    def get_hash(self):
        return self.__hash

    @staticmethod
    def read_user(username):
        from database.Database import Database
        return Database.read_user(username)
        # if username == "Hsing":
        #     return User("Hsing", b'$2b$13$tnZM92073l7vTEOrlQaTFeLZ0h1rstQZiPLgdu0kQirgZbVokHgVu')
        # return None

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.__hash)
