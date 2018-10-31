# Gearlog
Gearlog monitors the usage of gear tools.

In short, gearlog translates the server log files into permalog files 
stripped of ip addresses. The access is translated into a primary and 
a secondary key, which are used for counting. The original ip is also 
used for a geo-lookup.

No personal data is stored in the permalogs.

Installing a local copy for testing
-----------------------------------

`git clone https://github.com/gear-genomics/gearlog.git`

`cd gearlog`


Setup the scripts and cronjob
-----------------------------

Set the path to the log folders with environment variables:

Path to the server logs:

`export GEARLOG_SERVER_LOG_PATH=/PATH_TO_NGINX_OR_APACHE_LOG`

Path to the Primer3Plus logs (only if present):

`export GEARLOG_P3P_LOG_PATH=/PATH_TO_PRIMER3PLUS_LOG`

Install the Geolite2 database from MaxMind, available from http://www.maxmind.com:

`./src/update_GeoLite2.py`

Analyze log files:

`./src/create_report.py`

Results end up in the folder /log_report

Adapt the monitored pages in:

`vim src/settings.py`

Run the script after logrotate or as cronjob:

`./src/cron_log_update.py`


Setup and run the server
------------------------

The server runs in a terminal.

Install the dependencies:

`sudo apt install python python-pip`

`pip install flask flask_cors`

Start the server:

Path to the server logs:

`export GEARLOG_SERVER_LOG_PATH=/PATH_TO_NGINX_OR_APACHE_LOG`

Path to the Primer3Plus logs (only if present):

`export GEARLOG_P3P_LOG_PATH=/PATH_TO_PRIMER3PLUS_LOG`

`cd PATH_TO_GEARLOG/gearlog`

`python server/server.py`


Setup and run the client
------------------------

The client requires a different terminal

Install the dependencies:

`cd PATH_TO_GEARLOG/gearlog/client`

`sudo apt install npm`

`npm install`

Start the client:

`cd PATH_TO_GEARLOG/gearlog/client`

`npm run dev`



