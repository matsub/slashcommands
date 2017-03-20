# coding: utf-8

import urllib.request
import urllib.parse


class Client:

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, url):
        url = urllib.parse.urljoin(self.baseurl, url)
        return urllib.request.urlopen(url)

    def post(self, url, data):
        url = urllib.parse.urljoin(self.baseurl, url)
        data = urllib.parse.urlencode(data).encode()
        return urllib.request.urlopen(url, data)
