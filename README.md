# azurecli-api FASTAPI
**Azure CLI wrapped in HTTP REST API**
<br>
dead simple HTTP-REST-API written in python using FASTAPI to execute commands on azure cli without leaving the browser.
<br>
**this project uses sentry for monitoring be sure to change the accesskey**
<br>
**Usage**
<br>
* swagger at "http://your-ip-address:5000/docs"
<br>
* login to azure "http://your-ip-address:5000/api/v1/azure/login"
<br>
* send a get request to "http://your-ip-address:5000/api/v1/azure/{command}" command is what ever you want to execute, cli example would be "az {command}" running on your os command line.
<br>
* **you can also deploy this as a docker container using "docker build -t" . after cloning repository**
<br>
have fun!
<br>
# azurecli-hug hug
this is the same thing but i used hug instead of fastapi
