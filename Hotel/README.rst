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
    Ref: http://flask.pocoo.org/docs/1.0/tutorial/ 
    Reasons:
        Clean code base
        Offers production grade deployment
        
Set up virtual env
    cd <GitDir>/cmpe272WarriorsHotel/Hotel
    python3 -m venv venv 
    . venv/bin/activate

Generate Readme file from .rst
    Ref: http://docutils.sourceforge.net/docs/user/rst/quickref.html 

Install Hotel
    pip install --upgrade pip   # ensure latest pip
    pip install -e .

Run
----
::

    export FLASK_APP=hotel
    export FLASK_ENV=development
    flask init-db   # to set up tables
    flask run

Open http://127.0.0.1:5000 in a browser.


OLD Text for reference : TODO: Delete after above document is ready!
=====================================================================




Test
----

::

    pip install '.[test]'
    pytest

Run with coverage report::

    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
