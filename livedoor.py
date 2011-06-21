#!/usr/bin/env python

# Python livedoor Auth API
# Copyright (C) 2007 TANIGUCHI Takaki <taaki@asis.media-as.org>

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import urlparse
import urllib
import time
import sha
import hmac
import json


BASE_URL = 'http://auth.livedoor.com/'
DEFAULT_TIMEOUT = 60 * 5

class Auth:
    def __init__(self, app_key, secret, ver='1.0', timeout=DEFAULT_TIMEOUT):
        self.app_key = app_key
        self.secret  = secret
        self.ver     = ver
        self.timeout = timeout

    def uri_to_login(self, perms='userhash', userdata=None, t=None):
        if not (perms == 'userhash' or perms == 'id'):
            raise ValueError("argument 'perms' should be 'id' or 'userhash'.")

        
        query = { 'v': self.ver, 'app_key' : self.app_key, 'perms' : perms}
        if t is None:
            query['t'] = str(int(time.time()))
        if userdata is not None:
            query['userdata'] = userdata

        query['sig'] = self.calc_sig(query)
        uri = "%s?%s" % (urlparse.urljoin(BASE_URL, '/login/'),
                         urllib.urlencode(query))
        return uri
        
    def validate_response(self, query):
        # query = self._normalize_query(query) # does not need it, maybe.
        if query['sig'] == self.calc_sig(query):
            if time.time() - int(query['t']) > self.timeout:
                raise RuntimeError('LOCAL TIMEOUT')
            user = User()
            if query.has_key('userdata'):
                user.userdata = query['userdata']
            user.userhash = query['userhash']
            user.token = query['token']
            return user
        else:
            raise RuntimeError('INVALID SIG' + ' ' +
                               query['sig'] + ' ' +  self.calc_sig(query))
    
    def get_livedoor_id(self, user):
        self.call_auth_rpc(user)
        return user.livedoor_id

    def call_auth_rpc(self, user):
        query = {'app_key' : self.app_key,
                 'v' : self.ver,
                 'format' : 'json', 
                 'token' : user.token,
                 't' : str(int(time.time())) }
        query['sig'] = self.calc_sig(query)
        uri = urlparse.urljoin(BASE_URL, '/rpc/auth')
        params = urllib.urlencode(query)
        res = urllib.urlopen(uri,params).read()
        js = json.read(res)
        if js['error']:
            raise RuntimeError(js['message'])
        user.livedoor_id = js['user']['livedoor_id']
        return user

    def calc_sig(self, query):
        context = hmac.new(self.secret, digestmod=sha)
        # query = self._normalize_query(query) # does not need it, maybe.
        keys = query.keys()
        keys.sort()
        for k in keys:
            if k == 'sig':
                continue
            context.update(k)
            context.update(query[k])
        return context.hexdigest()

class User:
    def __init__(self):
        self.token = None
        self.userhash = None
        self.userdata = None
        self.livedoor_id = None


def _test():
    key = 'key'
    sec = 'sec'
    a = Auth(key, sec)
    print a.uri_to_login()

if __name__ == '__main__':
    _test()

