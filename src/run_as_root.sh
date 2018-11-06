#!/bin/bash

# The script is run as root, so only root should be able to modify
chown root cron_log_update.py
chgrp root cron_log_update.py
chmod 744 cron_log_update.py


