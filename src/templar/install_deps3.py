#!/usr/bin/python3

'''
this script downloads stuff that we don't have ubuntu packages for

TODO:
- add progress report on downloading
'''

import subprocess # for check_call
import urllib.request # for build_opener, urlretrieve
import os # for mkdir
import os.path # for isdir, join, isfile
import zipfile # for ZipFile

def download(url,output_file):
    if not os.path.isfile(output_file):
        print('downloading [{0}] because it is not there...'.format(output_file))
        # this doesn't work because I need user agent...
        #urllib.request.urlretrieve(url, output_file)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)
        f=open(output_file,'wb')
        f.write(response.read())
        f.close()

if not os.path.isdir('download'):
    os.mkdir('download')

download('http://code.highcharts.com/zips/Highcharts-3.0.5.zip', 'download/Highcharts-3.0.5.zip')
if not os.path.isdir('download/Highcharts'):
    os.mkdir('download/Highcharts')
    z=zipfile.ZipFile('download/Highcharts-3.0.5.zip', 'r')
    z.extractall('download/Highcharts')
    z.close()

folder='download/extjs'
fname='ext-4.2.1-gpl.zip'
url_prefix='http://cdn.sencha.com/ext/gpl'
local_file=os.path.join('download', fname)
remote_file=os.path.join(url_prefix, fname)
download(remote_file, local_file) 
if not os.path.isdir(folder):
    z=zipfile.ZipFile(local_file, 'r')
    z.extractall('download')
    z.close()
    os.rename('download/ext-4.2.1.883', folder)

download('http://veltzer.net/media/sample.ogg', 'download/sample.ogg')
download('http://veltzer.net/media/sample.ogv', 'download/sample.ogv')
download('http://veltzer.net/media/sample.mp4', 'download/sample.mp4')
download('http://veltzer.net/media/sample.mp3', 'download/sample.mp3')
