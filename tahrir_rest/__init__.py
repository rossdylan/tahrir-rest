import json
from flask import Flask, request, abort
from tahrir_api.dbapi import TahrirDatabase


class TahrirRestApp(object):
    def __init__(self, dburi, salt):
        self.dburi = dburi
        self.salt = salt

        self.database = TahrirDatabase(self.dburi)
        self.app = Flask(__name__)

        self.routes = {
                "/badges/<uid>": (self.badges_uid, {'methods': ['GET', 'DELETE']}),
                "/badges/": (self.add_badge, {'methods': ['POST']}),
                }
        map(lambda route: self.app.route(
                route,
                self.routes[0],
                **self.routes[1]
            ),
            self.routes
        )


    def badges_uid(self, uid):
        """
        GET: /badges/<uid>
        DELETE: /badges/<uid>
        return s a JSON blob with all the badge attributes
        Deletes a badge with the given uid
        """
        if request.method == 'DELETE':
            pass
        if request.method == 'GET':
            pass
    def add_badge(self):
        """
        POST: /badges
        accepts a json blob with all the badge attributes
        """
        try:
            data = json.loads(request.data)
        except:
            abort(503)
        try:
            badge_id = self.database.add_badge(
                    data['name'],
                    data['image'],
                    data['desc'],
                    data['criteria'],
                    data['issuer_id']
                    )
            return json.dumps({'badge_id': badge_id})
        except KeyError:
            abort(503)




def main(globalArgs, **localArgs):
    dburi = globalArgs.get('sqlalchemy.url', 'sqlite:///tahrir.db')
    salt = globalArgs.get('tahrir.salt', 'beefy')
    app = TahrirRestApp(dburi, salt)
    return app.app
