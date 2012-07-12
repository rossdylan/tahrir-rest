import json
from flask import Flask, request, abort
from tahrir_api.dbapi import TahrirDatabase
import logging

log = logging.getLogger("TahrirRest")

class TahrirRestApp(object):
    def __init__(self, dburi, salt):
        self.dburi = dburi
        self.salt = salt

        self.database = TahrirDatabase(self.dburi)
        self.app = Flask(__name__)

        self.routes = {
                "/badges/<uid>": (self.badges_uid, {'methods': ['GET', 'DELETE']}),
                "/badges/": (self.add_badge, {'methods': ['POST']}),
                "/people/<uid>": (self.people, {'methods': ['GET', 'DELETE']}),
                "/people/": (self.add_person, {'methods': ['POST']}),
                "/issuers/<uid>": (self.issuers, {'methods': ['GET', 'DELETE']}),
                "/issuers/": (self.add_issuer, {'methods': ['POST']}),
                "/assertions/<email>": (self.assertions, {'methods': ['GET']}),
                "/assertions/": (self.add_assertions, {'methods': ['POST']}),
                }
        map(
            lambda route: self.app.route(route, **self.routes[route][1])(
                self.routes[route][0]
            ),
            self.routes
        )

    def people(self, uid):
        """
        GET: /people/<uid>
        Delete: /people/<uid>
        Get info on a person, or delete them
        """
        if request.method == 'DELETE':
            result = self.database.delete_person(uid)
            if result != False:
                log.info("DELETE Request for /people/{0} succeeded".format(uid))
                return json.dumps({'success': True, 'id': result})
            else:
                log.info("DELETE Request for /people/{0} failed",format(uid))
                return json.dumps({'success': False, 'id': uid})

        if request.method == 'GET':
            person = self.database.get_person(uid)
            if person == None:
                log.info("GET request for /people/{0} failed".format(uid))
                return json.dumps({})
            else:
                log.info("GET request for /people/{0} suceeded".format(uid))
                return json.dumps(person.__json__())

    def add_person(self):
        """
        POST: /people/
        Add a new Person
        """
        try:
            data = json.loads(request.data)
        except:
            log.info("add_person Failed: could not parse request.data")
            abort(503)
        try:
            result = self.database.add_person(
                    hash(data['email']),
                    data['email']
                    )
            log.info("Added Person: {0}".format(data['email']))
            return json.dumps({'email': result})
        except KeyError:
            log.info("add_person Failed: JSON doesn't include all required fields")
            abort(503)



    def badges_uid(self, uid):
        """
        GET: /badges/<uid>
        DELETE: /badges/<uid>
        return s a JSON blob with all the badge attributes
        Deletes a badge with the given uid
        """
        if request.method == 'DELETE':
            result = self.database.delete_badge(uid)
            if result != False:
                log.info("DELETE Request for /badges/{0} suceeded".format(uid))
                return json.dumps({'success': True, 'id': result})
            else:
                log.info("DELETE Request for /badges/{0} failed".format(uid))
                return json.dumps({'success': False, 'id': uid})

        if request.method == 'GET':
            badge = self.database.get_badge(uid)
            if badge == None:
                log.info("GET Request for /badges/{0} failed".format(uid))
                return json.dumps({})
            else:
                log.info("GET Request for /badges/{0} succeeded".format(uid))
                return json.dumps(badge.__json__())

    def add_badge(self):
        """
        POST: /badges
        accepts a json blob with all the badge attributes
        """
        try:
            data = json.loads(request.data)
        except:
            log.info("add_badge Failed: Could not parse request.data")
            abort(503)
        try:
            badge_id = self.database.add_badge(
                    data['name'],
                    data['image'],
                    data['desc'],
                    data['criteria'],
                    data['issuer_id']
                    )
            log.info("Added Badge: {0}".format(data['name']))
            return json.dumps({'id': badge_id})
        except KeyError:
            log.info("add_badge Failed: JSON does not have required fields")
            abort(503)

    def issuers(self, uid):
        """
        GET /issuers/<id>
        DELETE /issuers/<id>
        Delete or Get an issuer
        """

        if request.method == 'GET':
            issuer = self.database.get_issuer(uid)
            if issuer == None:
                log.info('GET Request for /issuers/{0} failed'.format(uid))
                return json.dumps({})
            else:
                log.info('Get Request for /issuers/{0} succeeded'.format(uid))
                return json.dumps(issuer.__json__())
        if request.method == 'DELETE':
            result = self.database.delete_issuer(uid)
            if result != False:
                log.info("DELETE Request for /issuers/{0} suceeded".format(uid))
                return json.dumps({'success': True, 'id': uid})
            else:
                log.info('DELETE Request for /issuers/{0} failed'.format(uid))
                return json.dumps({'success': False, 'id': uid})

    def add_issuer(self):
        """
        POST /issuers/
        Add a new issuer
        """

        try:
            data = json.loads(request.data)
        except:
            log.info("add_issuer Failed: Could not parse request.data")
            abort(503)
        try:
            issuer_id = self.database.add_badge(
                    data['origin'],
                    data['name'],
                    data['org'],
                    data['contact']
                    )
            log.info("Added issuer: {0}".format(data['name']))
            return json.dumps({'id': issuer_id})
        except KeyError:
            log.info("add_issuer Failed: JSON does not have required fields")
            abort(503)

    def assertions(self, email):
        """
        GET /assertions/<email>
        Return a list of all assertions awarded to the given email
        """
        results = self.database.get_assertions_by_email(email)
        if results == False:
            log.info("GET /assertions/{0} failed".format(email))
            return json.dumps({"success": False, "email": email})
        else:
            expanded_results = {
                    'success': True,
                    'assertions': [r.__json__() for r in results]}
            return json.dumps(expanded_results)

    def add_assertion(self):
        """
        POST /assertions/
        Add a new assertion
        """

        try:
            data = json.loads(request.data)
        except:
            log.info("add_assertion Failed: Could not parse request.data")
            abort(503)
        try:
            person_email, badge_id = self.database.add_assertion(
                    data['badge_id'],
                    data['person_email'],
                    data.get('issued_on', None)
                    )
            return json.dumps({
                'success': True,
                'badge_id': badge_id,
                'person_email': person_email
                })
        except KeyError:
            log.info("add_assertion Failed: JSON does not have the required fields")
            abort(503)

def main(globalArgs, **localArgs):
    dburi = globalArgs.get('sqlalchemy.url', 'sqlite:///tahrir.db')
    salt = globalArgs.get('tahrir.salt', 'beefy')
    app = TahrirRestApp(dburi, salt)
    return app.app
