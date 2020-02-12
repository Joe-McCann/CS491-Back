import falcon

from helloWorld import HelloWorld
from events import Events
from login import Login

api = application = falcon.API()

hw = HelloWorld()
ev = Events()
log = Login()
api.add_route('/helloWorld', hw)
api.add_route('/events', ev)
api.add_route('/login', log)
