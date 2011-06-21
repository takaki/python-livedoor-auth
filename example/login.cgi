#!/usr/bin/env python 
import livedoor
import cgitb; cgitb.enable()
import cgi
import config
import time

key = config.key
sec = config.sec

a = livedoor.Auth(key,sec)
ct = time.ctime()
uri = a.uri_to_login(perms='id', userdata=ct)


print "Content-Type: text/html"     # HTML is following         
print 
print """userdata = %s<br />"""  % ct
print """<a href="%s">login</a>""" % cgi.escape(uri)
