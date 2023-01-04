from executor import execute
from az.cli import az as azure
import hug ,uuid , datetime ,requests , sys, jwt, json


class myServer():
    
    def azureCmd(Self, cmd):
        #this is az.cli function wrapper
        Self.azureInit = azure(f"{cmd}")
        Self.azureStatus = Self.azureInit[0]
        Self.azureResponse = Self.azureInit[1]
        Self.azureLog = Self.azureInit[2]
        #now checking the status code assigning a ray id and keeping in sqlite
        return Self
    
    def performChecks(Self):
        Self.azureCmd('version')

        terraform = execute('terraform -version', capture=True)
        docker = execute('docker version',capture=True)
        dockerj = json.dumps(docker)
        terraformj = json.dumps(terraform)
        passed = {
            "azure-cli-version": Self.azureResponse,
            "Logged-in-as": Self.azureLogin(),
            "docker.io": dockerj,
            "terraform": terraformj,
            "status": 'ok'
        }
        return passed
                 
    def location(Self):
        try:
            Self.response = requests.get('https://ipapi.co/json/').json()
            return Self.response
        except:
            return False  


    @hug.object.get('/ping')
    def heartbeat(Self):
        heartbeat = {
            "message": 'pong!',
        }
        return heartbeat
    
    @hug.object.get("/azure/{command}")
    async def azureCli(Self, command):

        Self.azureCmd(command)


        return Self.azureStatus , Self.azureResponse, Self.azureLog
    
route = hug.route.API(__name__)
route.object('/')(myServer)