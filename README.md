Packman
=======

![Build status](https://secure.travis-ci.org/hasgeek/packman.png)
[![Coverage Status](https://coveralls.io/repos/hasgeek/packman/badge.png?branch=master)](https://coveralls.io/r/hasgeek/packman?branch=master)


Packman is HasGeek's new asset packing management tool, for tracking
where all our stuff is and what it is.

We are currenly building out an API, with the UI scheduled for later.
There's some boilerplate UI that is common across all our apps.

This app uses Compass for custom stylesheets. Stylesheets are located
in `packman/static/sass` and may be rebuilt with `compass compile` from
the base folder. To rebuild automatically, use `compass watch`.
