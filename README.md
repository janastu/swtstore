swtstore (Sweet Store)
======================

----


Introduction
------------

This is the sweet store application.

The store for the decentralized, semantic, social web tweets a.k.a SWeeTs!

This application acts as the repository store for all the SWeeTs that are
generated from the clients registered with the sweet store. It also provides
query APIs to query the SWeeTs.

Sweet store provides the following APIs:

    - [GET] /api/sweets/<id>: Get a specific SWeeT by its id.

    - [POST] /api/sweets : Post a SWeeT to this swtstore with the data in the
    body of the request. Only registered applications can sweet to sweet store.

    - [POST] /api/context : Create a new context on the swtstore.


Any client side application can communicate with the sweet store using these
APIs.


Installing
----------

The swtstore application is written in Python and uses a relational database.

Hence, the dependencies of this application is Python and any relational database
supported by SQLAlchemy.

Most common RDBMS supported by SQLAlchemy are MySQL, Postgresql.

For more information on supported databases see
[here](http://docs.sqlalchemy.org/en/rel_0_9/dialects/index.html).

_Important:_
__So once you are sure you have Python and a relational database (like
MySQL/Postgresql etc.) installed. You can go ahead and follow these steps:__

* Clone the repository from [https://git.pantoto.org/sweet-web/sweet-web-engine]
  (https://git.pantoto.org/sweet-web/sweet-web-engine) OR you can download the
  code from the same link.

* Initialize a python virtual environment using virtualenv in the same place
  where you cloned the reposiory in the above step. Now, activate the
  environment ``$ source <path/to/your/current-virtual-env>/bin/activate ``

  See
  [http://www.virtualenv.org/en/latest/virtualenv.html]
  (http://www.virtualenv.org/en/latest/virtualenv.html) for more details.

* Run the setup.py script to install  `` python setup.py install ``

You're done installing swtstore. Now you need to configure it to run.


Configure swtstore
------------------

* Copy the contents of ``sample_config.py`` inside the ``swtstore`` directory
  into ``config.py`` inside ``swtstore`` directory itself.

  Assuming you are using a Unix based system, and you are in the root directory
  of the codebase,

  `` $ cp swtstore/sample_config.py swtstore/config.py``

* Edit the config.py file, and change the values accordingly.



Running the server locally
--------------------------

Run the runserver.py script to run the server locally,

`` python runserver.py ``

This runs the application locally, on port 5001



Deploying the application
-------------------------

The wsgi script to deploy the application is present.
Point your webserver like Apache, or Nginx to point to the swtstore.wsgi
script.

See Apache WSGI configuration here:
[http://modwsgi.readthedocs.org/en/latest/configuration-directives/WSGIScriptAlias.html]
(http://modwsgi.readthedocs.org/en/latest/configuration-directives/WSGIScriptAlias.html)


Help / Feedback
---------------

If you need any help, or have any questions, comments or feedback, you can contact at
rayanon or arvind or bhanu @servelots.com

You can also join channel #servelots on freenode network, using your favourite
IRC client. We usually hang out at #servelots.


License
-------

BSD Licensed.

See LICENSE for more details.
