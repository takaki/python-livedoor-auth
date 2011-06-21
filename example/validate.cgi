#!/usr/bin/python
import livedoor
import cgitb; cgitb.enable()
import cgi
import config
key = config.key
sec = config.sec


print "Content-Type: text/html"     # HTML is following         
print 

form = cgi.FieldStorage()
query = {}
print "<dl>"
for k in form.keys():
	print "<dt>%s</dt>" %  k 
	print "<dd>%s</dd>" % form.getfirst(k)
	query[k] = form.getfirst(k)
	
a = livedoor.Auth(key, sec)
user = a.validate_response(query)
livedoor_id = a.get_livedoor_id(user)
for k in user.__dict__.keys():
	print "<dt>livedoor.%s</dt>" %  k 
	print "<dd>%s</dd>" % user.__dict__[k]
	
print "</dl>"
