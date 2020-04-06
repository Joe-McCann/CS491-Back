import falcon

from helloWorld import HelloWorld
from createEvent import createEvent
from login import Login
from register import Register
from getEvents import getEvents
from checkUserExists import CheckUserExists

api = application = falcon.API()

hw = HelloWorld()
ce = createEvent()
ge = getEvents()
log = Login()
cue = CheckUserExists()
register = Register()
api.add_route('/helloWorld', hw)
api.add_route('/checkUserExists', cue)
api.add_route('/createEvent', ce)
api.add_route('/getEvents', ge)
api.add_route('/login', log)
api.add_route('/register', register)


# -------------------------------------------------------------------------------
# For development only and should be removed for production environments
# -------------------------------------------------------------------------------
from refresh import RefreshDevServerResource
api.add_route('/refreshServer', RefreshDevServerResource())
# -------------------------------------------------------------------------------
