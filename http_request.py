#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Wenqian Wang"

import urllib2


def http_get_info(url, header):
    req = urllib2.Request(url=url, headers=header)
    try:
        resp = urllib2.urlopen(req)
        ret = resp.info()
        return ret
    except urllib2.HTTPError as e:
        print e
        return ""


def http_get_content(url, header):
    req = urllib2.Request(url=url, headers=header)
    try:
        resp = urllib2.urlopen(req)
        ret = resp.read()
        return ret
    except urllib2.HTTPError as e:
        print e
        return ""


def http_delete(url):
    req = urllib2.Request(url=url)
    req.get_method = lambda: 'DELETE'
    try:
        resp = urllib2.urlopen(req)
        ret = resp.read()
        return ret
    except urllib2.HTTPError as e:
        print e
        return ""

