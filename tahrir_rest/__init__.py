from flask import Flask, reqeust
from tahrir_api.dbapi import TahrirDatabase

class TahrirRestApp(object):
    def __init__(self, dburi, salt):
        self.dburi = dburi
        self.salt = salt

        self.database = TahrirDatabase(self.dburi)
        self.app = Flask(__name__)



def main(globalArgs, **localArgs):
    dburi = globalArgs.get('sqlalchemy.url', 'sqlite:///tahrir.db')
    salt = globalArgs.get('tahrir.salt', 'beefy')
    app = TahrirRestApp(dburi, salt)
    return app.app
