SvxLinkWrapper - wrapper for SvxLink
====================================
By Guy Sheffer 4Z7GAI <guysoft at gmail dot com>

Features
--------

* Autoconnect to stations on startup, and keep-alive option
* QSO Echolink logger in sqlite3 and a simple web viewer for it
* Send DTMF preset commands from echolink chat

Requirements
------------
1. python
2. python modules:     importlib python-sqlite3
3. Svxlink ready to run and configured (https://sourceforge.net/apps/trac/svxlink/)

Install all requirements except svxlink on Ubuntu / Debian
----------------------------------------------------------

::
    
    apt-get install python-sqlite3



Quick setup on Ubuntu / Debian
------------------------------
::
    
    git clone https://github.com/guysoft/SvxLinkWrapper.git
    cd SvxLinkWrapper
    cp config.ini.example to config.ini
    python src/SvxLinkWrapper.py


How to configure and run
------------------------
1. copy config.ini.example to config.ini
2. Set the variables according to your need in main


How to configure QSO logger module
-----------------------------------
1. set DATABASE_PATH in modules.EcholinkLoggerModule to the location of EcholinkQsoLog.sqlite
2. Make sure the folder that EcholinkQsoLog.sqlite has read/write permissions, as well as the file
3. If you want to view latest qsos from a browser you can move ``www/EcholinkQsoLog.php`` to a location on your webserver (on Ubuntu / Debian the default path is ``/vart/www`` )
