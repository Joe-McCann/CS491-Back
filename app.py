import falcon

from helloWorld import HelloWorld

api = application = falcon.API()

hw = HelloWorld()
api.add_route('/helloWorld', hw)
