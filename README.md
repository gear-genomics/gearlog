# gearlog
Usage of gear tools.

In short, gearlog translates the server log files into permalog files 
stripped of ip addresses. The access is translated into a primary and 
a secondary key, which are used for counting. The original ip is also 
used for a geo-lookup.

No personal data is stored in the permalogs.

Installing
----------

`git clone https://github.com/gear-genomics/gearlog.git`

`cd gearlog`

Setup
-----
Install the Geolite2 database from MaxMind, available from http://www.maxmind.com:

`./src/update_GeoLite2.py`

Analyze log files:

`./src/create_report.py`

Results end up in the folder /log_report

Adapt the monitored pages in:

`vim src/settings.py`

Run the script after logrotate or as cronjob:

`./src/cron_log_update.py`


Install Web Interface
---------------------

`sudo apt install python python-pip`

`pip install flask flask_cors`


Running local
-------------

`python server/server.py`

Open in Browser:

`client/index.html`


