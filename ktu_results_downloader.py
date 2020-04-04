#!/usr/bin/env python3
# Copyright Anoop
# KTU Results downloader ver 2.5
import requests
import urllib.parse
from bs4 import BeautifulSoup
import argparse
import os
import getpass
# colors
GREEN = '\033[32m'
YELLOW = '\033[33m'
WHITE = '\033[m' 
PURPLE = '\033[35m'
CYAN = '\033[36m'
# default downlaod dir
default_dir = os.path.expanduser('~')+'/'
# main
def main(sem,username,password,outdir,timeout_seconds):
    string_id=[]
    headers = {
        'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36'
    }

    login_data_params={}
    login_data_params['username'] = username
    login_data_params['password'] = password

    grade_card_params = {
        'form_name': 'semesterGradeCardListingSearchForm',
        'search': 'Search',
        'stdId': ''
    }
    grade_card_params['semesterId'] = sem
    
    download_params = {
        'pageAction': 'downloadItextPDF',
        'package': 'result',
        'class': 'SemesterGradeCardReport'
    }

    with requests.Session() as s:
        url = 'https://app.ktu.edu.in/login.jsp'
        grade_card_url = 'https://app.ktu.edu.in/eu/res/semesterGradeCardListing.htm'
        pdf_url = 'https://app.ktu.edu.in/eu/pub/attachments.htm'
        # Initial login
        while True:
            print(YELLOW,"trying to login",WHITE)
            req = s.get(url, headers=headers, timeout=int(timeout_seconds))
            if req.status_code != 200:
                raise Exception
            soup = BeautifulSoup(req.content, 'html5lib')
            login_data_params['CSRF_TOKEN'] = soup.find('input', attrs={'name': 'CSRF_TOKEN'})['value']
            req = s.post(url, params=login_data_params, headers=headers, timeout=int(timeout_seconds))
            break
        # get studid and semid
        grade_card_params['CSRF_TOKEN'] = login_data_params['CSRF_TOKEN']
        while True:
            print(YELLOW,'getting studid and semid',WHITE)
            req = s.post(grade_card_url, headers=headers, params=grade_card_params, timeout=int(timeout_seconds))
            if req.status_code != 200:
                raise Exception
            soup = BeautifulSoup(req.content, 'html5lib')
            string_id = soup.findAll('a', {'class': 'btn btn-danger btn-xs pull-right'})[0]['href']
            string_id=string_id.split('&')
            download_params['semId'] = urllib.parse.unquote(string_id[-2].strip('semId='))
            download_params['studId'] = urllib.parse.unquote(string_id[-1].strip('studId='))
            break
        # Download pdf
        with open(outdir+username+'_'+'grade_card.pdf',"wb") as grade_card_file:
            while True:
                print(YELLOW,'trying to download pdf',WHITE)
                req = s.get(pdf_url,headers=headers, params=download_params, timeout=int(timeout_seconds))
                if req.status_code != 200:
                    raise Exception
                file_type = req.content[:4].decode()
                if file_type != '%PDF':
                    raise Exception
                grade_card_file.write(req.content)
                break

# CLI
parser = argparse.ArgumentParser(
    description='A script to download KTU student results as pdf.')

parser.add_argument(
    '-s',
    '--semester',
    dest='sem',
    action='store',
    help='semester no.')

parser.add_argument(
    '-u',
    '--user-name',
    dest='username' ,
    action='store')
parser.add_argument(
    '-p',
    '--password',
    dest='password',
    action='store',
    help='prompt if not supplied')
parser.add_argument(
    '-o',
    '--output',
    dest='outdir',
    action='store',
    default=default_dir)

parser.add_argument(
    '-t',
    '--timeout',
    dest='timeout_seconds',
    action='store',
    default=7,
    help='request timeout in seconds')

args = parser.parse_args()
if args.sem and args.username:
    if not args.password:
        args.password = getpass.getpass(prompt='Password: ', stream=None)
    # Append '/' to given path if not present
    if args.outdir[-1] != '/':
        args.outdir = args.outdir+'/'
    print(CYAN,'Download location: ',WHITE,args.outdir)
    while True:
        try:
            main(args.sem,args.username,args.password,args.outdir, args.timeout_seconds)
            print(GREEN,"Download complete!",WHITE)
            break
        except KeyboardInterrupt:
            break
        except:
            print(PURPLE,"retrying",WHITE)
            continue
else:
    print("Arguments missing. use -h for help")
