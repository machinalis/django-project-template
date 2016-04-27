{{project_name}}
===============

> Note: This is just template text, please adjust to your needs

This is a project template to be used to kickstart a django based website.

This template includes:

- A base layout and bootstrap scaffolding.
- Dev tools such as ipdb or django-debug-toolbar.
- A modern toolchain for javascript and sass.
- Some random sugar.

# Ussage

Clone this package:

    $ git clone git://github.com/tutuca/django-project-template.git

Setup and activate a [virtual environment](http://pypi.python.org/pypi/virtualenv):

    $ cd ~/venvs/ # or wherever you want
    $ virtualenv {{project_name}} -ppython3
    $ source {{project_name}}/bin/activate

Setup your python dependencies:

    ({{project_name}})$ cd ~/Projects/{{project_name}} # wherever you cloned this
    ({{project_name}})$ pip install -r requirements.txt

Install the package in development mode:

    ({{project_name}})$ python setup.py develop

# Create a blank application

    $ django-admin.py startapp  <app_name>

Add it to `INSTALLED_APPS` in `{{project_name}}/settings.py` and define your environment settings in a blank `{{project_name}}/local_settings.py`.

    #local_settings.py
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': '{{project_name}}',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
    }   

# Initialize your database as usual.

First create your schemas and run default migrations:
    
    $ {{project_name}} migrate

> Note that `{{project_name}}` is django's usual management wrapper made 
> available session-wide by setup tools.

Whenever you made further changes to your models run:

    $ {{project_name}} makemigrations <app_name>

# Static assets toolchain.

We rely on [npm](http://npmjs.org) and [grunt](http://gruntjs.com/) to handle the static assets dependency management and build tasks. Under the hood it is using:

- [webpack](http://webpack.github.io/): Javascript bundle
- [babel](https://babeljs.io/): JS Compiler, allowes us to use ecmascript 6 syntax.
- [sass](http://sass-lang.com/): CSS compiler, allowes us to use variables and mixins.
- [bootstrap](http://getbootstrap.com/): In it's official sass port, it is the most widely used layout framework with a large variety of built-in components.

While using this tools should be transparent to you as dev. Knowing their roles, uses and pitfals will help you write better code (and to fix them if they brake :).

We also ship [eslint](http://eslint.org/) and [stylelint](http://stylelint.io/).

To install the required tools and libraries use:

    $ npm install  

Then you may run:

    $ grunt

By default this is run in `watch` mode and will listen for changes in the `assets` folder as well as `package.json` and `Grunfile.js` files.

This will populate the `static/` folder which will be served by django's development server.

Now you are ready to run the development server:

    $ {{project_name}} runserver

Licence notice:
---------------
© 2016 {{project_name}} - ,
A copy of the project licence is available at COPYING.
