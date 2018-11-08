#!/bin/bash

# The script is run as root, so only root should be able to modify
chown root cron_log_update.py
chgrp root cron_log_update.py
chmod 744 cron_log_update.py

chown root ip2integer.py ip2integer.pyc logfunctions.py logfunctions.pyc settings.py settings.pyc
chgrp root ip2integer.py ip2integer.pyc logfunctions.py logfunctions.pyc settings.py settings.pyc
chmod 755  ip2integer.py ip2integer.pyc logfunctions.py logfunctions.pyc settings.py settings.pyc

