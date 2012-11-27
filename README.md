Location
========

Save, view, edit, and delete your favorite locations.

Try it out! http://shrouded-lake-4711.herokuapp.com

About
-----
This was started for a programming challenge, but I want to incorporate it
with [Promt] (http://promtapp.com) eventually and because the frontend was
becoming unwieldy I took the opportunity to finally learn Backbone and spent
a little time on the frontend. Much thanks to
[Todos] (http://documentcloud.github.com/backbone/examples/todos/index.html) for that.
The backend consists of a standard REST API for managing locations, and some
simple user registration and session management.

Built With
----------
 * [Flask] (http://flask.pocoo.org/)
 * [Backbone] (http://backbonejs.org/)
 * [Google Maps JavaScript API] (https://developers.google.com/maps/documentation/javascript/)

Install
-------
You already made a a virtualenv right?

```shell
$ python runserver.py
```

Test
----
The backend is decently tested, though there is a problem with the current_user
alias provided by the Flask-Login extension which is preventing testing of some sections.
There are test written, but they are hidden behind 2 `if False:` statements for now.

```shell
$ python runtests.py
```
