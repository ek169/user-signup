#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

sign_up = """
    <h3> Sign Up </h3>
    <br>
    <form method='post'>
        <label>
            User:
            <input type='text' name='user' value='%(user)s'/>
        %(error_user)s
        </label>
        <br>
        <label>
            Password:
            <input type='password' name='password'/>
        </label>
        %(error_password)s
        <br>
        <label>
            Verify Password:
            <input type='password' name='verify'/>
        </label>
        %(error_verify)s
        <br>
        <label>
            Email (optional):
            <input type='text' name='email' value='%(email)s'/>
        </label>
        %(error_email)s
        <br>
        <input type='submit'/>
    </form>
"""


class MainHandler(webapp2.RequestHandler):
    def write_form(self, params):

        self.response.out.write(sign_up % params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Signup(MainHandler):
    def get(self):
        params = dict(user='', password='', verify='', error_user='', error_password='', error_verify='', error_email='', email='')
        self.write_form(params)

    def post(self):
        error = False

        self.user = self.request.get('user')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(user=self.user, password='', verify='', error_user='', error_password='', error_verify='',
                      error_email='', email=self.email)


        if not valid_user(self.user):
            params['error_user'] = "Your user isn't valid"
            error = True

        if not valid_password(self.password):
            params['error_password'] = "Your password must be longer than three characters"
            error = True

        elif self.password != self.verify:
            params['error_verify'] = "Your passwords don't match"
            error = True

        if self.email:
            if not valid_email(self.email):
                params['error_email'] = "Your email isn't valid"
                error = True

        if error:
            self.write_form(params)
        else:
            self.redirect('/welcome?user=' + self.user)


class Welcome(MainHandler):
    def get(self):
        user = self.request.get('user')
        if valid_user(user):
            welcome_str = '<p>Welcome ' + str(user) + '</p>'
            self.write(welcome_str)

        else:
            self.redirect('/')




USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_user(user):
    return USER_RE.match(user)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")
def valid_email(email):
    return EMAIL_RE.match(email)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
