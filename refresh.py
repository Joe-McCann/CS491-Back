import subprocess

class RefreshDevServerResource(object):

    def on_post(self, req, resp):
        """Handles the GitHub webhook request to refresh the server with the newly pushed repository code"""
        subprocess.call("./refreshScript.sh")
