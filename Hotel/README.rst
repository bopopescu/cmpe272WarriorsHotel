Hotel
======
CMPE 272 : Project : Browse Hotel rooms listings

Team Warriors
--------------
* Pradeep 
* Sanjeevi
* Senthil
* Yuva

Setting up Project environment
------------------------------

Adapting code from Flaskr tutorial 
::
   * http://flask.pocoo.org/docs/1.0/tutorial/ 
   * https://github.com/pallets/flask/tree/1.0.2/examples/tutorial 
   * Reasons
      * Clean code base
      * Offers production grade deployment
        
Set up virtual env 
::
    cd <GitDir>/cmpe272WarriorsHotel/Hotel
    python3 -m venv venv 
    . venv/bin/activate

Generate Readme file from .rst 
::
   http://docutils.sourceforge.net/docs/user/rst/quickref.html 

Install Hotel (dev)
::
    pip install --upgrade pip   # ensure latest pip
    pip install -e .

Setting up Project SQLite file
    Download data.zip
    Unzip to local folder
    Create a new SQLite file
::
    sqlite> .open db.sqlite
    sqlite> .mode csv
    sqlite> .import /Users/athur/Downloads/data/listings.csv listings
    sqlite> .import /Users/athur/Downloads/data/reviews.csv reviews
    sqlite> .import /Users/athur/Downloads/data/calendar.csv calendar
    sqlite> .exit

Rename db.sqlite to hotel.sqlite and move it to /instance folder

Run
----
::

    export FLASK_APP=hotel
    export FLASK_ENV=development
    flask init-db   # to set up tables
    flask run

Open http://127.0.0.1:5000 in a browser.

Test # TODO
------------

::

    pip install '.[test]'
    pytest

Run with coverage report::

    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser

Create production image
------------------------
Ref: http://flask.pocoo.org/docs/1.0/tutorial/deploy/
::
    pip install wheel
    python setup.py bdist_wheel
    /Users/athur/Code/cmpe272WarriorsHotel/Hotel/dist/warriors_hotel-1.0.0-py2.py3-none-any.whl

Possible error conditions during build + install + run:
    Fixed: MANIFEST.in "LICENCE" - spelling error fixed for correct file name
    Fixed: Include schema (.sql), static and template pages (.html)

Install production instance
::
    cd /<New directory> # from new terminal
    # set up new venv and activate it
    python3 -m venv venv 
    . venv/bin/activate
    # then
    pip install warriors_hotel-1.0.0-py2.py3-none-any.whl
    # check /Users/athur/Code/prod/hotel-prod/venv/lib/python3.7/site-packages/hotel
    export FLASK_APP=hotel
    flask init-db

Possible error conditions
    Fixed: Reinstallation with new .whl file DOES NOT update venv.
    Fixed: So, delete venv and start all over again.

Configuring Secret key
    Running app creates venv/var/hotel-instance
    Generate secret key for production
::
    python -c 'import os; print(os.urandom(16))'
    # b'\xac/\xcdR\xa6\xa9"\xcd\x15d\x05F\xe1\x11]\xd5'
    # set secret key in venv/var/hotel-instance/config.py
    SECRET_KEY = b'\xac/\xcdR\xa6\xa9"\xcd\x15d\x05F\xe1\x11]\xd5'

Run with production server
::

    pip install waitress # production grade secure WSGI server
    waitress-serve --call 'flaskr:create_app'

Looking into more deployment options
Ref: http://flask.pocoo.org/docs/1.0/deploying/

