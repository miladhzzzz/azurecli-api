import asyncio, json, requests, sentry_sdk, uvicorn
from fastapi import FastAPI, BackgroundTasks, Request, Response
from pydantic import BaseModel
from az.cli import az as azure
from executor import execute
    
# !!! CHANGE THIS
sentry_sdk.init(
    dsn="https://842a456040cb46c798ae53f13c343992@o4503956234764288.ingest.sentry.io/4503956236730368",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

class AzureResponse(BaseModel):
    azureStatus : str
    azureResponse: str
    azureLog: set

app = FastAPI()
    
# global variables
loop = asyncio.get_event_loop()

# BackGround Tasks Functions / Global Functions
async def azureCmd(cmd):
        #this is az.cli function wrapper
        azureInit = azure(f"{cmd}")
        AzureResponse.azureStatus = azureInit[0]
        AzureResponse.azureResponse = azureInit[1]
        AzureResponse.azureStatus = azureInit[2]
        #now checking the status code assigning a ray id and keeping in sqlite
        return AzureResponse
    
async def performChecks():
    res = azureCmd('version')

    terraform = execute('terraform -version', capture=True)
    docker = execute('docker version',capture=True)
    dockerj = json.dumps(docker)
    terraformj = json.dumps(terraform)
    passed = {
         "azure-cli-version": res.azureResponse,
         "Logged-in-as": "azureLogin()",
         "docker.io": dockerj,
           "terraform": terraformj,
          "status": 'ok'
     }
    return passed
# because we live in iran i wrote this so i can break before accessing azure if my ip address is from iran!                 
async def location():
    try:
        response = requests.get('https://ipapi.co/json/').json()
        return response
    except:
        return False  


@app.on_event("startup")
async def startup_event():
    #performChecks()
    print("h")

@app.on_event("shutdown")
async def shutdown_event():
    print("bye")


# >>>>>>>>>>>ACTUAL END POINTS <<<<<<<<<<<<<<<

@app.get("/api/v1/azure/login")
async def azureLogin():
    res = await azureCmd("login")
    return res

@app.get("/api/v1/azure/{command}")
async def azureCli(command: str, background_tasks: BackgroundTasks):
   res = await azureCmd(command)
   background_tasks.add_task(location)
   
   return res.azureResponse

# !! call this only on linux based machines like from inside a container that has terraform/az cli/docker/ etc... isntalled!
@app.get("/api/v1/checkEnv")
async def check():
    res = await performChecks()
    return res

# >>>>>>>>>>>>>> TESTS <<<<<<<<<<<<<<<<

@app.get("/ping")
async def ping():
    return {"message": "pong!"}

if __name__ == "__main__":
    uvicorn.run("fastapi-azure:app", host="0.0.0.0",port=5000, log_level="info" , reload=True)