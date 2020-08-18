# Stack Configuration

## Overview

This stack is designed to include multiple backend and frontend technologies, each in separate docker containers, all initiated and networked together using the same docker-compose.yml file.

## Core Stack

The core web and database stack is defined in the docker-compose.yml, defined as 2 services:

- **db** - Postgres database, core SQL
- **web** - Django driven 

### db notes

```
    db:
      image: postgres
      environment:
        - POSTGRES_DB=postgres
        - POSTGRES_USER=postgres
        - POSTGRES_PASSWORD=postgres
      # this is for local administration only
      ports:
        - "6543:5432"
```
The exposed port is changed to 6543 to allow administration from the host without clashing with a previously installed version of Postgres

To Do Items:
- [ ] Set up secure credentials from ENV variables and AWS Secrets?, or from GitHub mechanism
- [ ] Set up local persisent storage version of database outside of container
- [ ] Possibly migrate Postgres to RDS services if cost effective, for prod version

*Currently, the entire database code is contained in the db container, with no local persistent storage.  Until changed, do not delete this container during development unless starting over*

### web notes

```
    web:
      build: 
        dockerfile: Dockerfile
        context: ./img-baseclient
      #command: python manage.py runserver 0.0.0.0:8000
      command: >
        sh -c "python manage.py makemigrations &&
               python manage.py migrate &&
               python manage.py runserver 0.0.0.0:8000"
      volumes:
        - ./img-baseclient:/code
      ports:
        - "8000:8000"
      depends_on:
        - db
```
A sub directory in the overall repository was created for this image, which is referred to in the web>build>context parameter.  Everything related to building this image goes inside this folder.  Dockerfile, requirements.txt and all of the django code lives in this folder and is shared as a volume during development.  All of this content is also copied into the working directory defined in the Dockerfile on each build.

To verify the files exist in the correct directory of the web container, run ```docker ps -a``` to get the container ID, then run the following to get a bash prompt:
```
docker exec -it <container ID> /bin/bash
```

### Initiation of the core stack.

This files initially used to create the stack, before modifications, is contained in the codearchive> coreinitiation directory.  This along with the following commands, executed at the root directory of the repo, will set up a brand new base stack with 2 containers: web with Django, db with Postgres.

**Step 1: Create the Django project in the local dev folder from the web image**
```
sudo docker-compose run --rm django-admin startproject steelecore ./img-baseclient
```
This will create the steelecore Django project, but will not launch the stack yet. The image that was initiated from the command will be removecd after the project has started.  (--rm)

**Step 2: Set the rights on the newly created Django folder**

The steelecore folder was created using **sudo**, so we need to set the rights so the current user can modify the files.  From within the img-baseclient directory:
```
ls -l   #check rights
sudo chown -R $USER:$USER .   #change rights
```

**Step 3: Update the Django project to use Postgres instead of sqlite**

Find the settings.py file in the new Django project.  Replace the DATABASES section with the following:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

**Step 4: Create the containers, launching the stack**

From the root of the repository, where the docker-compose.yml file lives:
```
docker-compose up
```
This configuration has our web server running on port 8000.  In the browser, open ```http://localhost:8000 ```

*This results in a successfully launched Django/Postgres web database system*

**Step 5: Build out Django models and functionality**

In order to create new apps and run migrations on the web image, a linux shell must be opened.  As shown above, run ```docker ps -a``` to get the container ID for the web, then run the following to get a bash prompt:
```
docker exec -it <container ID> /bin/bash
```
Once the prompt is open (and assuming the volume to the host dev repository is still indicated in the docker-compose.yml) any changes made by manage.py will be reflected in the host files.  For example:
```
python manage.py startapp snippets  
```
After the above is run, a new **snippets** directory appears in the host repo for the new django app.  Local file edits directly to that directory are immediately reflected in the running console for the system (where the docker-compose command to start the system was run).

**In order to modify the newly created application:** 
When python from within the container creates a new directory on the host, the rights of that directory must be changed so the user can make modifications.  This is the same issue that occurred above when the Django project was initially created. In this example, from within the snippets directory, run:
```
ls -l   #check rights
sudo chown -R $USER:$USER .   #change rights
``` 
Now changes to the models, views, etc can begin. 

**Reminder:** *Any changes requiring migrations to be run must be performed in the above bash prompt for the web container.*

**Step 5.1: Installing python modules into Docker Container**

As an example, the pygments model used in the snippets model is not included in the python image and must be installed.  This can be run manually from the above bash statement, but once the container is rebuilt, it will need to be installed again.  To check which modules are installed currently, type ```pip freeze``` in the container's console.

To solve the problem of having to manually install the module, the appropriate command must be added to the Dockerfile, or preferrably in the requirements.txt

To update the requirements.txt with the exact versions of the installed packages, follow these steps:

- Launch the containers and open a bash prompt for the web container
- Run ```pip install <package name>``` for the target package
- Verify the package is installed properly: ```pip freeze```
- Use the following command to overwrite the requirements.txt file (save a copy first): ```pip freeze > requirements.txt```
- Edit the file and remove anything that is already installed as a part of the base docker image.  Then edit the packages to install from exact versions to minimum versions:
```
Django>=2.0,<3.0
psycopg2-binary>=2.8
Pygments==2.6.1
```
- Save file, shut down containers, delete the web container and relaunch
- Open the bash prompt and verify the packages are installed.

Useful blog on requirements.txt [HERE](https://note.nkmk.me/en/python-pip-install-requirements/)

**Massive Gotcha on requirements.txt** 
If the above changes to the packages does not actually install during the build process, but you can run ```pip install -r requirements.txt``` successfully from the container bash, delete both the container AND the image and try again. (save 2 hours of your life)

## Stack Extension

Now that the base stack has been configured, additional technologies can be added by building on the base docker-compose.yml.  

**Next steps TBD**


---
## Reference

**To Read** Interesting tutorial on a different stack with multiple tech in same docker-compose [here](https://www.digitalocean.com/community/tutorials/workflow-multiple-containers-docker-compose)


[Return to Main README](README.md)