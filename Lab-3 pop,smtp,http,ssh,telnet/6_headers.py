# /usr/bin/env python3

import urllib.request
url = input("Enter the URL: ")
http_respons = urllib.request.urlopen(url)
if http_respons.code == 200:
    print(http_respons.headers)
    for key,value in http_respons.getheaders():
        print(key,value)