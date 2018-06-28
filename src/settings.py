#!/usr/bin/env python

# Directory of the log files
# LOGDIR  = "../log"
LOGDIR  = "/var/log/nginx" # for Nginx server

# Base name of the log files
# LOGBASE = "mingear"
LOGBASE = "access" # for Nginx server

# File endings to ignore
IGNTYPE = [".jpg", ".png", ".svg", ".ico",
           ".css", ".js", ".json"]

# Files to track
# Provide primary key, secondary key and file with path
# "*" as last character allowed as wildcard 
TRACKLIST = [# ["","",""],
["Contact","Get Page","/contact"],
["Terms","Get Page","/terms"],
["Indigo", "Main", "/indigo"],
["Indigo", "Upload", "/indigo/upload"],
["Indigo", "Download", "/indigo/download/*"],
["Alfred","Get Page","/alfred"],
["Alfred","Upload","/alfred/upload"],
["Alfred","Download","/alfred/download/*"],
["Silica","Get Page","/silica"],
["Silica","Upload","/silica/upload"],
["Silica","Download","/silica/results/*"],
["Silica","Download","/silica/download/*"],
["Bgen","Get Page","/bgen"],
["Bgen","Download","/bgen/*"],
["Sage","Get Page","/sage"],
["Sage","Upload","/sage/upload"],
["Sage","Download","/sage/download/*"],
["Bistro","Get Page","/bistro"],
["Teal","Get Page","/teal"],
["Teal","Upload","/teal/upload"],
["Teal","Upload","/teal/api/v1/upload"],
["Verdin","Get Page","/verdin"],
["Verdin","Primers","/verdin/api/v1/primer*"],
["Maze","Get Page","/maze"],
["Wiley DNA Editor","Get Page","/wily-dna-editor"],
["Wiley DNA Editor","Get Page","/wily-dna-editor/index.html"],
["Wiley DNA Editor","Help","/wily-dna-editor/help.html"],
["Wiley DNA Editor","About","/wily-dna-editor/about.html"],
["Wiley DNA Editor","More","/wily-dna-editor/more.html"],
["Gear Main","Get Page","/"]
]

