# morgynstryker.com

This is an application for my upcoming refreshed personal website. 

I haven't been updating my [website](https://morgynstryker.com) due to work and I as I looked at what I had 
started over a year ago, I have decided to start fresh. I will be using Django 2.0.2 and Python 3.6.4. The 
reason for doing this in Django over Flask or another framework is because you have so many features built-in. 
Django has the ORM built-in where Flask requires you to use a SQLAlchemy ORM or something similar/else. 
Django has admin functionality built-in, so you can manage the site and easily add new posts to the page behind 
a login. Due to these features and many more, Django is extremely quick to build a fairly secure website. 

If you wish to not be placed in the box that Django restricts you to, Flask is an excellent alternative. However,
time to flight can be a bit longer with Flask.

I have another site up [with Django](https://wonkrz.com/), if you wanted to see something working.

## Pre-requisites 

The following items are needed to setup the application.

- [Python 3.6](https://python.org)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)


## Setup 

Create a virtualenv

    $ mkvirtualenv -p python3 morgynstryker
    $ workon morgynstryker
    
The app was created using the following:

    (morgynstryker)$ django-admin startproject morgynstryker
    
I reorganized the default django setup, as you can see in the Project Structure section below. I had to modify the
`manage.py`, `wsgi.py`, and `settings.py` to point to the correct location of the files on reorganization.

`manager.py`
```python
import os
...
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "morgynstryker.config.settings")
...
```
`wsgi.py`
```python
import os
...
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "morgynstryker.config.settings")
...
```
`settings.py`
```python
...
ROOT_URLCONF = 'morgynstryker.config.urls'
...
WSGI_APPLICATION = 'morgynstryker.config.wsgi.application'
...
```
If you are like me and would like to modify the structure of the application, these are the items you will
need to change. I have created a `settings_example.py` to see some of these changes. This will NEVER get used and so, it
is ok to check into the project.

Now, I haven't done any migrations yet, but you should still be able to run the application and see an 
HTML page. If you go to your command line and enter the following:

    (morgynstryker)$ python manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    
    You have 14 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    
    March 11, 2018 - 22:26:00
    Django version 2.0.2, using settings 'morgynstryker.config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
As you can see, you will get some useful output, such as where to access your application in the browser.

    http://127.0.0.1:8000/  # or localhost:8000

Woot! We have the start of the project!

    
## Project Structure
    
The project was restructured to the following format:
    
    .
    morgynstryker.com
    |-- docs
    |-- morgynstryker
        |-- config
        |   |-- __init__.py
        |   |-- settings.py  # Do not check into source control
        |   |-- settings_example.py  # for reference, do not put secret stuff here
        |   |-- urls.py
        |   |-- wsgi.py
        |-- __init__.py
        |-- manage.py
    |-- .gitignore
    |-- LICENSE
    |-- README.md
    |-- requirements.txt
    |-- requirements_dev.txt
    |-- requirements_test.txt  # TODO: Add for testing config
    |-- setup.py
    
From a previous job, I picked up using `config` for all things application configuration as it keeps
things nice and tidy and reduces some confusing with Django's `from django.conf import settings`. Anytime 
you need to reference settings within a project, it is best practice to import that way.


### docs

This is where I will be setting up Sphinx documentation.

TODO: Add Sphinx docs


### morgynstryker

This is the application that will be updated with time.

TODO: Add more stuff


### .gitignore

This is one of the first things I ALWAYS create within an application because:

- one should NEVER check in passwords or secret keys
- one should NEVER check in `*.pyc` files
- one should not check in databases
- one should not check in IDE based configurations because all developers have different preferences


### LICENSE

It is a good idea to always have a LICENSE file with the project to inform users if they can freely
use and distribute the application or not.


### manage.py

This is what I will be using to call the management commands for the application.


### README.md

This is the what you are currently reading.


### Requirements

As you may have noticed, I have a few different requirements txt files. Each one has or will have the
following purpose:

`requirements.txt` - Everything you need to run the application on the server, and only what you need to
                     run the application on the server.

`requirements_dev.txt` - Everything you need as a developer, such as Sphinx for documentation.

`requirements_test.txt` - All packages or applications you need to test your code. These should never be installed
                          on a production instance. They are good to have checked into source control so
                          you can can setup automated testing with Jenkins or something similar. I am very
                          partial to Jenkins because of the open-source community and support for it.
                          

### setup.py

This is the center of all activity in building, distributing, and installing modules using the `Distutils`. If
you would like more information, [go here](https://docs.python.org/3.6/distutils/setupscript.html).


## Items TODO

This application will be hosted on AWS (current plan), unless I decide to go for Google App Engine or 
something similar. AWS has excellent integration with GitHub and CodeDeploy that will allow me to have
deployments trigger automatically happen when branches are pushed to master (CD).

Because planning is a good step to stay organized and be able to release items quickly (sometimes I get sidetracked), 
I have added a few items to get me started in creating this application.
 
This site should have the following items for release:

As a site administrator, I would like to...
- have a scalable application that meets demand of many users.
- have an alert system in case things stop working.
- have a fallback static site to give users information that the site/service is down.

As an admin user of the site, I would like to...
- upload photos and attach watermarks through an admin UI.
- post articles/blogs through an admin UI.
- tag articles/blogs through an admin UI.
- create a series of articles/blogs with future release dates through an admin UI.
- "deactivate" articles/blogs through an admin UI.
- have comments for readers to react to the articles/blogs or ask questions for clarification.
- filter out malicious comments from users and not display them.
- read direct messages from users via a "Contact" page in an admin UI.

As a developer of this project, I would like to...
- have confidence that new features/changes will not break existing code.
- have an organized git workflow that allows me to develop features and rollback if needed.
- receive alerts if users hit exceptions within the code.

As a developer reading this project, I would like to...
- be able to have documentation that walks me through the setup process of creating this site.

As a site user, I would like to...
- to view the articles/blogs through the main application.
- to comment on articles/blogs.


Now, these items are not too exhaustive, but a good starting point to give you a transparent direction
that I intend to go with this application. GitHub has some basic project management tools that I may decide
to incorporate into this should anyone else want to learn or contribute. But, since it will just be
me developing this application, I may elect to keep things simple and sweet.


## Documentation

Sphinx has been installed for application documentation, this can be viewed by doing the following:

    (morgynstryker)$ open docs/index.html
    

Stay tuned for more development!

---
