#!/usr/bin/env python3
# Copyright Anoop
# KTU Results downloader ver 2.5
import requests
import urllib.parse
from bs4 import BeautifulSoup
import argparse
import os
default_dir = os.path.expanduser('~')+'/Downloads/'

def check(outdir,username):
    with open(outdir+username+'_'+'grade_card.pdf', 'rb') as f:
        bytes=f.read()[:4]
        file_type=bytes.decode().strip('%')
        return file_type


def main(sem,username,password,outdir,timeout_seconds):

    retry = True

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
        while retry:
            print("trying to login")
            req = s.get(url, headers=headers, timeout=int(timeout_seconds))
            if req.status_code != 200:
                print("Retrying to login")
                continue
            soup = BeautifulSoup(req.content, 'html5lib')
            login_data_params['CSRF_TOKEN'] = soup.find('input', attrs={'name': 'CSRF_TOKEN'})['value']
            req = s.post(url, params=login_data_params, headers=headers, timeout=int(timeout_seconds))
            retry = False
        # get studid and semid
        retry = True
        grade_card_params['CSRF_TOKEN'] = login_data_params['CSRF_TOKEN']
        while retry:
            print('getting studid and semid')
            req = s.post(grade_card_url, headers=headers, params=grade_card_params, timeout=int(timeout_seconds))
            if req.status_code != 200:
                print('retrying to get studid and semid')
                continue
            soup = BeautifulSoup(req.content, 'html5lib')
            string_id = soup.findAll('a', {'class': 'btn btn-danger btn-xs pull-right'})[0]['href']
            string_id=string_id.split('&')
            download_params['semId'] = urllib.parse.unquote(string_id[-2].strip('semId='))
            download_params['studId'] = urllib.parse.unquote(string_id[-1].strip('studId='))
            retry = False
        # Download pdf
        retry = True

        with open(outdir+username+'_'+'grade_card.pdf',"wb") as grade_card_file:
            while retry:
                print('trying to download pdf')
                req = s.get(pdf_url,headers=headers, params=download_params, timeout=int(timeout_seconds))
                if req.status_code != 200:
                    print("Retrying to download pdf")
                    continue
                grade_card_file.write(req.content)
                retry = False

# CLI
parser = argparse.ArgumentParser(
    description='A script to download KTU student results as pdf')

parser.add_argument(
    '-s',
    '--semester',
    dest='sem',
    action='store',
    help='semester eg: -s4')

parser.add_argument(
    '-u',
    '--user-name',
    dest='username' ,
    default='<default>',
    action='store',
    help='username(your username)')
parser.add_argument(
    '-p',
    '--password',
    dest='password',
    action='store',
    help='password')
parser.add_argument(
    '-o',
    '--output',
    dest='outdir',
    action='store',
    default=default_dir,
    help='output directory')

parser.add_argument(
    '-t',
    '--timeout',
    dest='timeout_seconds',
    action='store',
    default=7,
    help='request timeout in seconds')

args = parser.parse_args()
if args.sem and args.password:
    print('Download location: ',args.outdir)
    while True:
        try:
            main(args.sem,args.username,args.password,args.outdir, args.timeout_seconds)
            file_type=check(args.outdir,args.username)
            if file_type != 'PDF':
                continue
            else:
                print("Download complete!")
                break
        except KeyboardInterrupt:
            break
        except:
            print("retrying")
            continue
else:
    print("Arguments missing. use -h for help")
