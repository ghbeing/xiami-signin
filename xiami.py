# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib, sys, re

class Xiami:
	loginurl = 'https://login.xiami.com/member/login'
	signinurl = 'http://www.xiami.com/web/checkin/id/'
	loginheaders = [('User-agent','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]
	signinheaders = [('User-Agent','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'), 
					 ('X-Requested-With','XMLHttpRequest'), 
					 ('Content-Length',0), 
					 ('Origin','http://www.xiami.com'), 
					 ('Referer','http://www.xiami.com/')]
	signindata = urllib.urlencode({})
	email = ''
	pwd = ''

	def __init__(self, email, pwd):
		self.email = email
		self.password = pwd
		self.logindata = urllib.urlencode({'_xiamitoken':'a15c56db0af05903a98334b227f73f49',
										   'done':'',
										   'type':'',
										   'email':email,
										   'password':pwd,
										   'autologin':'1',
										   'submit':'登 录',
										   '_xiamitoken':'a15c56db0af05903a98334b227f73f49',
										   'done':'/'})
		self.cj = cookielib.LWPCookieJar()
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cj)
		self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
		urllib2.install_opener(self.opener)

	def post(self, url, header, postdata):
		self.opener.addheaders = header;
		req = urllib2.Request(url=url,
							  data=postdata)
		try:
		    return self.opener.open(url, postdata).read()
		except:
		    sys.exit()

	def login(self):
		return self.post(self.loginurl,self.loginheaders,self.logindata)

	def signin(self):
		result = self.login()
		xiamiid = re.compile(r'<strong><a href="(.*?)" name_card="(.*?)">(.*?)</a></strong>').search(result).group(2)
		result = self.post(self.signinurl + xiamiid,self.signinheaders,self.signindata)
		#print result
		m = re.compile(r'<div class="idh">已连续签到(\d+)天</div>').search(result)
		if m == None :
			print "OOXX"




if __name__ == '__main__':
	user = Xiami('email', 'pwd')
	user.signin()
