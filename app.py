import falcon

from helloWorld import HelloWorld
from createEvent import createEvent
from login import Login
from register import Register
from getEvents import getEvents
from checkUserExists import CheckUserExists
from getFriends import getFriends
from friendRequest import friendRequest
from updateFriendRequest import updateFriendRequest
from inviteEvent import inviteEvent
from updateEventStatus import updateEventStatus
from changeEventModifier import ChangeEventModifier
from searchUsername import SearchUsername

api = application = falcon.API()

hw = HelloWorld()
ce = createEvent()
ge = getEvents()
log = Login()
cue = CheckUserExists()
register = Register()
gf = getFriends()
fr = friendRequest()
ufr = updateFriendRequest()
ie = inviteEvent()
ues = updateEventStatus()
cem = ChangeEventModifier()
su = SearchUsername()

api.add_route('/helloWorld', hw)
api.add_route('/checkUserExists', cue)
api.add_route('/createEvent', ce)
api.add_route('/getEvents', ge)
api.add_route('/login', log)
api.add_route('/register', register)
api.add_route('/getFriends', gf)
api.add_route('/friendRequest', fr)
api.add_route('/updateFriendRequest', ufr)
api.add_route('/inviteEvent', ie)
api.add_route('/updateEventStatus', ues)
api.add_route('/changeEventModifier', cem)
api.add_route('/searchUsername', su)


# -------------------------------------------------------------------------------
# For development only and should be removed for production environments
# -------------------------------------------------------------------------------
from refresh import RefreshDevServerResource
api.add_route('/refreshServer', RefreshDevServerResource())
# -------------------------------------------------------------------------------
