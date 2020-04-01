# ktu results downloader

A script to download ktu exam result as pdf.
It will keep trying until the results is downloaded.

## Installation : 
sudo pip install -r requirements.txt

##  usage: 
ktu_results_downloader.py -s[semester no.] -u[username] -p[password] -t[timeout in seconds] -o[dir]

### example: ktu_results_downloader.py -s 3 -u MYUSERNAME -p PASSWORD -t 6 