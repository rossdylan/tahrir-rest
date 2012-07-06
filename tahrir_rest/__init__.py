from flask import Flask
from tahrir_api.dbapi import TahrirDatabase

class TahrirRestApp(object):
    def __init__(self, dburi, salt):
        self.dburi = dburi
        self.salt = salt

        self.database = TahrirDatabase(self.dburi)
        self.app = Flask(__name__)

    def get_badge(self, uid):
        """
        GET: /badges/<uid>
        return s a JSON blob with all the badge attributes
        """
        pass

    def add_badge(self):
        """
        POST: /badges
        accepts a json blob with all the badge attributes
        """
        pass

    def remove_badge(self):
        """
        DELETE /badges/<uid>
        Deletes a badge with the given uid
        """


def main(globalArgs, **localArgs):
    dburi = globalArgs.get('sqlalchemy.url', 'sqlite:///tahrir.db')
    salt = globalArgs.get('tahrir.salt', 'beefy')
    app = TahrirRestApp(dburi, salt)
    return app.app
