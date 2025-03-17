from flask_bcrypt import Bcrypt

class BcryptSingleton:
    _instance = None
    bcrypt = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def init_bcrypt(self, app):
        if self.bcrypt is None:
            self.bcrypt = Bcrypt(app)
        return self.bcrypt

    def get_bcrypt(self):
        if self.bcrypt is None:
            raise RuntimeError("Bcrypt not initialized. Call init_bcrypt with Flask app first.")
        return self.bcrypt
