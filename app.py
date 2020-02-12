import falcon

from helloWorld import HelloWorld
from events import Events

api = application = falcon.API()

hw = HelloWorld()
ev = Events()
api.add_route('/helloWorld', hw)
api.add_route('/events', ev)
