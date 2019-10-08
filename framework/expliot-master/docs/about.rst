About
=====

History
-------

I started dreaming about an IoT vulnerability scanner way back in 2014. My
idea was to automate the painful parts of an IoT penetration test. I figured
that in our pen-tests, we were wasting a lot of time in setting up the test
case environment and trying out different tools for specific purposes. Some
tools were new, some were incomplete, buggy, some were proprietary with the
hardware. After a while, we ended up writing our own scripts. Also, the nature
of the IoT pentest projects is such that no two projects will be the same,
today you might be pentesting a fleet management device and tomorrow you
will get to test a smart vacuum cleaner or a gas sensor or something else,
all of which have completely different use cases and physical interfaces
i.e. attack surface. So, I started conceptualizing and implementing a
framework that can encompass different functionality for an IoT pentest.
I chose Ruby as a language for implementing it as it is quite flexible.
During the development, I realized that there was not much support for
hardware and radio interfacing in Ruby. The first version was written in Ruby
and after a lot of thought and stress I decided to rewrite it in Python. The
current version is obviously in Python 3.

License
-------

EXPLIoT Framework is under the GNU AGPLv3 license.

Author
------

EXPLIoT Framework is conceptualized, designed and implemented by
`Aseem Jakhar <https://gitlab.com/aseemj>`_.

Contributors
------------

* `Arun Magesh <https://gitlab.com/arun.m>`_
* `Fabian Affolter <https://gitlab.com/fabaff>`_
* `Sneha Rajguru <https://twitter.com/Sneharajguru>`_

Thank you
---------

* Computer pirates HDS
* `null - The open security community <http://null.co.in>`_
* `Abhisek Datta <https://twitter.com/abh1sek>`_
* `Javier Vazquez Vidal <https://twitter.com/fjvva>`_
* `Milosch Meriac <https://www.meriac.com/>`_
* `Payatu Bandits <http://www.payatu.com/>`_
* `Hardwear.io Conference <https://hardwear.io/>`_
* `nullcon Conference <http://nullcon.net/>`_
