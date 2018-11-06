#!/usr/bin/env python

# Directory of the log files
# LOGDIR  = '/var/log/nginx'
LOGDIR = "/home/uni/embl/gearlog/bla_log"

# Base name of the log files
# LOGBASE = "mingear"
LOGBASE = "access" # for Nginx server

# File endings to ignore
IGNTYPE = [".jpg", ".png", ".svg", ".ico",
           ".css", ".js", ".json", ".txt",
           ".gz", ".pdf"]

# Files to track
# Provide primary key, secondary key and file with path
# "*" as last character allowed as wildcard 
TRACKLIST = [# ["","",""],
["Gear Main","Get Page","/"],
["Contact","Get Page","/contact"],
["Terms","Get Page","/terms"],

["Alfred","Get Page","/alfred"],
["Alfred","Upload","/alfred/upload"],
["Alfred","Upload","/alfred/api/v1/upload"],
["Alfred","Download","/alfred/download/*"],
["Alfred","Download","/alfred/api/v1/download/*"],
["Bistro","Get Page","/bistro"],
["Bgen","Get Page","/bgen"],
["Bgen","Download","/bgen/*"],
["Gearlog","All Interactions","/gearlog*"],
["Indigo", "Main", "/indigo"],
["Indigo", "Upload", "/indigo/upload"],
["Indigo", "Upload", "/indigo/api/v1/upload"],
["Indigo", "Download", "/indigo/download/*"],
["Indigo", "Download", "/indigo/api/v1/download/*"],
["Halo","Get Page","/halo"],
["Maze","Get Page","/maze"],
["Primer3Plus I","Get Page","/primer3plus"],
["Primer3Plus I","Get Page","/primer3plus/index.html"],
["Primer3Plus I","Get Page with UUID","/primer3plus/index.html?UUID=*"],
["Primer3Plus I","Load Default Settings","/primer3plus/api/v1/defaultsettings"],
["Primer3Plus I","Run Primer3","/primer3plus/api/v1/runprimer3"],
["Primer3Plus I","Pick Success","/zduzcbjhebjhcjgczjegbcjhejg"],
["Primer3Plus I","Pick Fail","/flktddtsuatudszuzewzuszezuz"],
["Primer3Plus I","Load Server Data","/primer3plus/api/v1/loadServerData"],
["Primer3Plus II","Get Compare Files","/primer3plus/primer3compareFiles.html"],
["Primer3Plus II","Get Manager","/primer3plus/primer3manager.html"],
["Primer3Plus II","Get Package","/primer3plus/primer3plusPackage.html"],
["Primer3Plus II","Get About","/primer3plus/primer3plusAbout.html"],
["Primer3Plus II","Get Help","/primer3plus/primer3plusHelp.html"],
["Primer3Plus II","Load Version","/primer3plus/api/v1/primer3version"],
["Sage","Get Page","/sage"],
["Sage","Upload","/sage/upload"],
["Sage","Upload","/sage/api/v1/upload"],
["Sage","Download","/sage/download/*"],
["Sage","Download","/sage/api/v1/download/*"],
["Silica","Get Page","/silica"],
["Silica","Load Genome Index","/silica/api/v1/genomeindex"],
["Silica","Upload","/silica/upload"],
["Silica","Upload","/silica/api/v1/upload"],
["Silica","Download","/silica/results/*"],
["Silica","Download","/silica/api/v1/results/*"],
["Silica","Download","/silica/download/*"],
["Silica","Download","/silica/api/v1/download/*"],
["Teal","Get Page","/teal"],
["Teal","Upload","/teal/upload"],
["Teal","Upload","/teal/api/v1/upload"],
["Verdin","Get Page","/verdin"],
["Verdin","Primers","/verdin/api/v1/primer*"],
["Wiley DNA Editor","Get Page","/wily-dna-editor"],
["Wiley DNA Editor","Get Page","/wily-dna-editor/index.html"],
["Wiley DNA Editor","Help","/wily-dna-editor/help.html"],
["Wiley DNA Editor","About","/wily-dna-editor/about.html"]
]

