Bookelgouna project setup
=========================

Countries
---------
Your database should contain full list of countries. To import all countries you should call ``import_countries``
manage.py command. It can be done painless again if you are in doubt about consistency of db cause any existing
``Country`` will be not replaced by this command.

Booking email templates
-----------------------
Your database should contain booking email templates. To import default templates you should call 
``import_booking_templates`` manage.py command. It can be done painless again if you are in doubt about consistency 
of db cause any existing ``BookingEmailTemplate`` will be not replaced by this command.

Celery
------
On production you should install rabbitmq (``sudo apt-get install rabbitmq-server``) and run next commands:

1. ``cd bookelgouna;celery -A common worker -l info -E``
2. ``cd bookelgouna;celery -A common beat``
3. ``python bookelgouna/manage.py celerycam``

Testing
=======

Facebook sharing functionality
------------------------------
Sometimes during localhost development you need to check how pages look like if someone would share them on Facebook.
In order to test it you can do next things:

1. Use any service which can setup sharing tunnel for you. I.e. [http://localtunnel.me/](http://localtunnel.me/).
2. Open [Facebook Debugger](https://developers.facebook.com/tools/debug/) and input your temporarily assigned url there.
3. You can also open facebook main page and input your url into textarea on your wall.
