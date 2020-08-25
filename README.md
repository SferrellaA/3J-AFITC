# 3J-AFITC
Team 3-J's entry for the [2020 AFITC hackaton](http://www.innovateafitc.com); rur project is an API enabling the tracking of equipment in a hospital system.

Items are tangible objects, such as a table or stetheschope, that require tracking. Items can be moved, used, and broken, all of which is recorded in their history along with timestamps and notes. "Use" events also record a list of (anonymous) patients that came into contact with it during use.

A skeletal **anonymous** patient tracker is also included. It records no pii, merely a "unique user id", optional notes, and a list of "flags". Flags represent anything pertinent to the history of an item the patient came into contact with, such as "diagnosed covid positive at this time". The anonymous nature of patients allows for integration with other, pii-rated patient databases.

To run the application, use `python manage.py runserver`. A simple "gui" is included in the `demo.html` file.
