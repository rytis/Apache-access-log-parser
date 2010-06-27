Apache access log parser
========================

A simple application that allows you to write custom plugins to exctract the 
statistical data from the Apache web server access logs.

The application was initially developed as an example for one of the 
["Pro Python System Administration"](http://apress.com/book/view/9781430226055) book chapters.

You can find more information about the application on [the project website](http://www.sysadminpy.com).

Application structure
---------------------

Application is split into three parts:

* The main application script (`http_log_parser.py`), which reads in the log lines
  and calls the plug-in framework
* The plug-in manager framework (`manager.py`), which handles the module loading
  and data passing functions
* The plug in modules (`plugins/plugin_*.py`). These modules implement the data
  gathering and processing functions.

Changing the log format
-----------------------

By default the application recognises the "combined" access log line format, which
is defined in the Apache configuration as:

    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
 
You can change the format structure by specifying it in the `LogLineGenerator`
constructor call. For example, if you are using a "Common Log Format" change
the following code:

    def main():
        ...
        log_generator = LogLineGenerator()
        ...

to:

    def main():
        ...
        log_generator = LogLineGenerator(log_format='%h %l %u %t %r %>s %b')
        ...

Developing the plug-in modules
------------------------------

All plug-in modules mus be placed in the `plugins/` directory. The filename
must be of the following format: `plugin_<plugin_name>.py`. The basic plug-in
module skeleton is:

    #!/usr/bin/env python
    
    from manager import Plugin
    
    class GeoIPStats(Plugin):
    
        def __init__(self, **kwargs):
            # plugin initialisation function
            ...
    
        def process(self, **kwargs):
            # this will be called for every line retrieved from the log file
            # the fields can be accessed as 'kwargs['remote_host']
            # the full listing of all available dictionary keys and their
            # mapping to the Apache log directives is defined in the
            # main application file
            ...

        def report(self, **kwargs):
            # this will be called when there are no more log entries left
            # this is the opportunity for the plug-in to calculate and
            # print some reports
            ...

Usage
-----

Running the main application will automaticaly load all the available plug-in
modules from the `plugins` directory. All files in the `logs` directory
are considered to be the Apache web server log files.

    $ ./http_log_parser.py 
    == Requests by country ==
            382: United States
            258: Sweden
            103: France
             42: China
             31: Russian Federation
              9: India
              8: Italy
              7: United Kingdom
              7: Anonymous Proxy
              6: Philippines
              6: Switzerland
              2: Tunisia
              2: Japan
              1: Croatia
    == HTTP code 200 counter ==
    HTTP 200 responses: 349
    All responses: 864


