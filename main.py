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
import urllib, urllib2
from bs4 import BeautifulSoup
from google.appengine.api import mail
from google.appengine.ext import db


url = 'http://www.asp.gov.al/index.php/home-2/13-shqip/37-kontroll-per-kundravajtjet-rrugore'

data = urllib.urlencode({'plate' : '******', #fut targen
                         'vin'  : '*********'}) #fut shasine

class Gjobat(db.Model):
	gjoba_db = db.StringProperty(required=True);

class MainHandler(webapp2.RequestHandler):
    def get(self, gjoba_vjeter=None, send_email=False):
   
        content = urllib2.urlopen(url=url, data=data).read()
        soup = BeautifulSoup(content)
        table = soup.find("table")
        gjoba_aktuale = table.find("td").get_text().strip()

        for q in Gjobat.all():
        	gjoba_vjeter = q.gjoba_db
        if gjoba_vjeter!=gjoba_aktuale:
        	send_email = True
        	db.delete(Gjobat.all(keys_only=True))
        	e = Gjobat(gjoba_db=gjoba_aktuale)
        	e.put()

        if send_email:
        	mail.send_mail(sender="NJOFTUESI <my_email@gmail.com>",
              to="Emri <my_email@gmail.com>",
              subject="Alert",
              body="""
              Vlera e gjobes suaj u ndryshua. Shkoi ne """ + str(gjoba_aktuale) + """ ishte ne """ + str(gjoba_vjeter) )
        self.response.out.write('gjoba aktuale nr:' + str(gjoba_aktuale) + '<p>' +'gjoba vjeter nr:' + str(gjoba_vjeter))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
