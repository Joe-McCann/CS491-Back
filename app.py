import falcon

from helloWorld import HelloWorld
from events import Events
from login import Login
from register import Register

api = application = falcon.API()

hw = HelloWorld()
ev = Events()
log = Login()
register = Register()
api.add_route('/helloWorld', hw)
api.add_route('/events', ev)
api.add_route('/login', log)
api.add_route('/register', register)


# -------------------------------------------------------------------------------
# For development only and should be removed for production environments
# -------------------------------------------------------------------------------
from refresh import RefreshDevServerResource
app.add_route('/refreshServer', RefreshDevServerResource())
# -------------------------------------------------------------------------------
