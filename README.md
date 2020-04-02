# ktu results downloader

A script to download ktu exam result as pdf.

Written as part of learning python.

##  Why use this:
When ktu publishes result usually their servers
are overloaded to the point its almost impossible 
to view result for several hours. 

This script will try
to download the result and it will keep trying
until it's been downloaded. so no need to refresh the pages !


## Installation : 
sudo pip install -r requirements.txt

##  usage: 
python3 ktu_results_downloader.py -s[semester no.] -u[username] -p[password] -t[timeout in seconds(default 7)] -o[dir]

### example: 
python3 ktu_results_downloader.py -s 3 -u MYUSERNAME -p PASSWORD -t 10 