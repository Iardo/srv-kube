# Dockerfiles

Collection of docker files for a lot of different services

---

## Config

### 1. Create a Host

You can create separated `host` configurations,
copy the `/host/@host-sample` directory and rename it as you wish.

It has two files inside:
```
.env               : Environment variables overrides
docker-compose.yml : List of services that you want to install
```

### 2. Set the Environment

The environment file overrides the variables that the services needs at initialization so you can personalize the values to your needs.

The file has three main sections:
```
# Principal : DO NOT TOUCH THIS,
              It is required for the docker-compose.yml file
              to work correctly.

# Override  : This is were you can put your static,
              ENV variables for example the `timezone`.

# Generated : DO NOT TOUCH THIS,
              This section is auto generated based on the
              services that you listed on docker-compose.yml.
```

### 3. List your services

In the `docker-compose.yml` file there is an `include` definition where you list all the services that you want to install.

The sample file includes all the services available to you, you can remove the ones that you dont need.

The services base files are inside the `/serv` directory.

---

## Usage

You can always just go to the specific services that you want and run `docker-compose up -d` as normal, but this method have some limitations:
```
1. You'll need to run some initialization task manually
2. Is going to use the default .env file provided in the service directory
3. You have to do this whole process for each service
```

Or you can use the scripts provided that takes care of this for you instead.

You can run the scripts in two ways, and it applies to all the scripts:
```
./init.py                     : This shows you a list
                                of available hosts to choose from
                                and let you select which one
                                you want to install.

./init.py --host=@host-sample : This receive the hostname
                                directly.
```

There are three scripts you can use:
```
./init.py  : Initializes the services,
             it requires to be ran at first.

./start.py : Starts all the host services
             leveraging docker-compose.
             
./stops.py : Stops all the host services.
```

> Note: ⚠️  
> ----
> 1. There could be some manual tasks required for some services though, so stay observant of the console output.
> 
> 2. The `stops.py` script do not remove any docker volumes, for that you need to remove them manually.

---

## Tasks

All services has a `/task` directory with utilities functions.

Unfortunately these needs to be ran manually, so you'll have to `cd` to the service directory and run them from there.

Do not `cd` inside the `/task` directory itself, the scripts asume to be ran from the service directory as the root like this: `./task/data-set-permissions.sh`

The utilities vary from service to service but there are some common ones:
```
data-gen-directories.sh : Generate required directories.
data-set-permissions.sh : Concedes file permissions to $USER.
database-backup         : Generate a backup for the service.
database-restore        : Restores a backup for the service.
```

---

## Clean-up

> Note: ⚠️  
> ----
> Stopping the containers are not going to remove your previous configurations,
so you have to do this manually.

All the services uses it's own directory to store their local configurations,
this means that, once you initialized a service on a machine,
you'll need to clean up their folders if you want to start the services from scratch.

Almost all services store their data inside the `/serv/${SERVICE_NAME}/data` directory.

