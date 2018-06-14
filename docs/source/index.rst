.. morgynstryker.com documentation master file, created by
   sphinx-quickstart on Sun Mar 11 16:09:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to morgynstryker.com's documentation!
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. include:: _pages/docs_setup.rst

For this documentation `(morgynstryker)$` will indicate that you have activated the virtualenvironment.

Create an App
-------------

Create your first app within the project. For the first app we will create a simple home page and this will be
responsible for your `index.hmtl` and other main sections of a basic website. Also, I like creating some
helper models to use down the road, so we will create a `util` app as well.

   (morgynstryker)$ cd morgynstryker
   (morgynstryker)$ python manage.py startapp home
   (morgynstryker)$ python manage.py startapp utils

You will then want to add `utils` and `home` to the end of your `INSTALLED_APPS` in your `settings.py` file (the order
here will matter). We will also be enabling the sites framework as this can allow you to use the same database
across different websites. Your `INSTALLED_APPS` should look like this:

.. code-block:: python
   INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'django.contrib.sites',
      'utils',
      'home',
   ]

You should also have `SITE_ID = 1` in your `settings.py` somewhere.

NOTE: It is very important to note that `utils` should always be imported from within your project!
You should NEVER import anything from your project into `utils` as this will lead to circular dependency
import issues.

Create an Abstract Audit Model (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is always a good idea to see when and who has modified a table, so I will create an abstract models to
add to my tables. In the `utils.models` I created a couple of models for this:

.. code-block:: python
   from django.conf import settings
   from django.db import models


   class TimeStampAbstractModel(models.Model):
       created_at = models.DateTimeField(auto_now_add=True)
       # updated_at isn’t updated when making updates to other fields in other ways such as QuerySet.update()
       updated_at = models.DateTimeField(auto_now=True)

       class Meta:
           abstract = True


   class UserAuditAbstractModel(models.Model):
       created_by = models.ForeignKey(
           settings.AUTH_USER_MODEL,
           null=False,
           on_delete=models.CASCADE,
           related_name='%(class)s_created_by')
       updated_by = models.ForeignKey(
           settings.AUTH_USER_MODEL,
           null=False,
           on_delete=models.CASCADE,
           related_name='%(class)s_updated_by')
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)

       class Meta:
           abstract = True


Django comes with an awesome admin interface and to use it, you will need a User model. Before you
start it is a good idea to consider if you will be customizing the default User model as it can be
extremely hard to change it down the road.

You should read some basics on `user auth <https://docs.djangoproject.com/en/2.0/topics/auth/>`_.

For this application we will keep things simple and `extend the User model <https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-user>`_.

Create the Database
~~~~~~~~~~~~~~~~~~~

For this application we will use Postgres and you can create a database locally for this. You
can visit the `PostgreSQL site <https://www.postgresql.org/>`_ to get familiar with and install
it. You should have it installed and log into the CLI to create your database ("=#" indicates
the database CLI):

   =# CREATE DATABASE morgynstryker_com WITH ENCODING 'UTF8';

It is important to always not what type of encoding you have on your database as this could
cause issues with special characters. Latin-8 is not the same as UTF-8 and I have once had
a "fun" situation where someone created a database with Latin-8 encoding. I always specify
encoding on creation just for safety due to that scenario.

When you create the database the owner should be your Postgres root user, but it is always
a good idea to not have that user be the one you put in your settings configuration. It is
good to always have users with specific roles in a database! Sometimes you only want some users
to have read access and only read access on specific tables. A scenario where you would not want
to give everyone access is in the case of PII (Personally Identifiable Information). You should
never pull PII off of production databases onto staging, testing, dev, or local databases. All
PII should be ran through a munging/scrubbing script to randomize the data so that you cannot
trace this back to a specific user. In some situations, you may not even want to do that at all
and just have the data live in production. This is something that some people forget!

So, we will create a user and grant privileges to the newly created database, where you
can use whatever user of password you would like:

   =# CREATE USER morgyn WITH PASSWORD 'somesecretpassword';
   =# GRANT ALL PRIVILEGES ON DATABASE morgynstryker_com TO morgyn;

Woot, you should have just created a database with access to a user "morgyn". You can review
this by entering the following:

   =# \l

This should give you a `List of databases` with Name, Owner, Encoding, Collate, Ctype, and
Access Privileges.

You are not done though, you will need to hook this database up to your Django project in the
`settings.py` file as follows:

.. code-block:: python
   DATABASES = {
       # 'default': {
       #     'ENGINE': 'django.db.backends.sqlite3',
       #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       # }
       'default': {
           'NAME': 'morgynstryker_com',
           'PORT': 5432,
           'ENGINE': 'django.db.backends.postgresql',
           'USER': 'morgyn',
           'PASSWORD': 'somesecretpassword'
       }
   }

As you can see I left the default sqlite3 information in and commented it out and replaced it
with the newly created Postgres database. You should also see that I have the password in raw
text here, which is why you NEVER want to check this into source control and why you will
see the `settings.py` file in the `.gitignore`. If you have check passwords into source control,
you should immediately change the passwords and remove the file(s) from source control. For
deployment, I will not be using this information and I have this information here for example
only.

Create the Initial Schema
~~~~~~~~~~~~~~~~~~~~~~~~~

For the `home` app, we will start with an `About` model that allows us to change what the about page
can say:

.. code-block:: python
   class About(UserAuditAbstractModel):
       header = models.CharField(max_length=100, default='About Me')
       description = models.TextField(null=False)
       default = models.BooleanField(default=False)
       site = models.ForeignKey(Site, on_delete=models.CASCADE, default=default_site)

       class Meta:
           verbose_name_plural = 'about'

In this model, we have created a header, description, default, and site columns beyond the audit information.
The `verbose_name_plural` will change how you see your objects in admin and such. By default, the plural name
ends with a "s" and "Abouts" isn't what we want to see, so we will see "About" instead.

Some will argue that we do not need to supply `max_length` with Postgres as character field and a text field
timing is the same, however having this allows us to apply length validation without extra work. The `default`
field will be used to determine what content we show to the user. If default is True, this will be what the
user will see. If no default is supplied for the site, then the user should see a 404 page.

When the models have been created in your `models.py`, you can create your migration scripts.

.. code-block:: bash
   (morgynstryker)$ python manage.py makemigrations
   Migrations for 'home':
     home/migrations/0001_initial.py
       - Create model About

This should have created an `0001_initial.py` file in `home.migrations`. If you look in `utils.migrations`
you will notice that it does not have this file. This is because we created `Abstract` model classes
that we can add to any table we want to get basic audit information. If you want to track each
individual change in order to revert if needed, that will be a bit more work and something that
can be covered down the road. For now, we should get who logged in and created the entry and who
the last person was to log in and change the entry.

You will need to apply these migrations once you have created them:

.. code-block:: bash
   (morgynstryker)$ python manage.py migrate
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, home, sessions, sites
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying admin.0001_initial... OK
     Applying admin.0002_logentry_remove_auto_add... OK
     Applying contenttypes.0002_remove_content_type_name... OK
     Applying auth.0002_alter_permission_name_max_length... OK
     Applying auth.0003_alter_user_email_max_length... OK
     Applying auth.0004_alter_user_username_opts... OK
     Applying auth.0005_alter_user_last_login_null... OK
     Applying auth.0006_require_contenttypes_0002... OK
     Applying auth.0007_alter_validators_add_error_messages... OK
     Applying auth.0008_alter_user_username_max_length... OK
     Applying auth.0009_alter_user_last_name_max_length... OK
     Applying sites.0001_initial... OK
     Applying sites.0002_alter_domain_unique... OK
     Applying home.0001_initial... OK
     Applying sessions.0001_initial... OK

You should be able to verify your tables have been created in the database:

   =# \c morgynstryker_com
   =# \d

Create a Superuser
------------------

One of my favorite features of Django over a framework like Flask is that Django comes with
an admin interface that is pretty easy to hook up. However, to use it you will need to create
a super user to log into it for the first time:

   (morgynstryker)$ python manage.py createsuperuser

When you have done this, you can launch the application:

   (morgynstryker)$ python manage.py runserver
   Performing system checks...

   System check identified no issues (0 silenced).
   June 01, 2018 - 22:09:29
   Django version 2.0.2, using settings 'config.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   [01/Jun/2018 22:09:35] "GET / HTTP/1.1" 200 666

You should then be able to go to `localhost:8000` and get your `index.html` page. If you go to
`localhost:8000/admin` and enter your superuser credentials, you should be able to log into the
admin page.




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
