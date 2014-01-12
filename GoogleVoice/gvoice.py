"""
gvoice.py

Created by: Scott Hillman
Modified by: David Bjanes

http://www.everydayscripting.blogspot.com

This module comes as is an with no warranty. 
You are free to use, modify and distribute this 
code however you wish, but I ask that if you post 
it anywhere, you at least make reference to me and
my blog where you acquired it.
"""

import csv
import sys
import re
import urllib
import urllib2
import json
from bs4 import BeautifulSoup
from cookielib import CookieJar
from operator import itemgetter, attrgetter

class GoogleVoiceLogin:
	""" 
	Class that attempts to log in the Google Voice 	using the provided 
	credentials. 
	
	If either no password or email is provided, the user will be 
	prompted for them.
	
	Once instantiated, you can check to see the status of the log in 
	request by accessing the "logged_in" attribute
	
	The primary usage of a GoogleVoiceLogin object is to be passed
	in to other constructors, such as the TextSender, or NumberDialer
	"""

	def __init__(self, email = None, password = None, verbose = False):
		"""
		Given the email and password values, this method will attempt to log
		in to Google Voice. The "response" attribute can be checked to 
		see if the login was a success or not.
		 
		If the login was successful, the "opener" and "key" attributes will
		be available to use when creating other objects. 
		
		To use an this object with the other classes in this module, simply
		pass it in to the constructor. (ie text_sender = TextSender(gv_login))
		"""
		
		if email is None:
			email = raw_input("Please enter your Google Account username: ")
		if password is None:
			import getpass
			password = getpass.getpass("Please enter your Google Account password: ")

		# Set up our opener
		cj = CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(self.opener)

		# Define URLs
		self.login_page_url   = 'https://accounts.google.com/ServiceLogin?service=grandcentral'
		self.authenticate_url = 'https://accounts.google.com/ServiceLogin?service=code&ltmpl=phosting&continue=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64&followup=http%3A%2F%2Fcode.google.com%2Fp%2Fpygooglevoice%2Fissues%2Fdetail%3Fid%3D64'
		self.gv_home_page_url = 'https://www.google.com/voice/#inbox'
		self.gv_sms_page_url  = 'https://www.google.com/voice/m/i/sms'
		self.logout_url       = 'https://www.google.com/voice/account/signout'
		self.gv_sms_mark_read = 'https://www.google.com/voice/m/mark?p=1&label=sms&id='
		self.headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }

		# Load sign in page
		login_page_contents = self.opener.open(self.login_page_url).read()
		cookie_list = [];
		for cookie in cj:
			cookie_list.append(cookie.value);
		
		# Set up login credentials
		self.login_params = urllib.urlencode({
			'Email' : email,
			'Passwd' : password,
			'continue' : 'https://www.google.com/voice/account/signin',
			'GALX' : cookie_list[0],
		})

		# Login
		req = urllib2.Request(self.authenticate_url, self.login_params, self.headers)
		auth_html_page = self.opener.open(req)

		# Open GV home page
		gv_home_page_contents = self.opener.open(self.gv_home_page_url).read()

		# Fine _rnr_se value
		key = re.search('name="_rnr_se".*?type="hidden".*?value="(.*?)"', gv_home_page_contents)

		if not key:
			self.logged_in = False
			if verbose:
				print("Google Login Failure.")
		else:
			self.logged_in = True
			self.key = key.group(1)
			if verbose:
				print("Google Login Successful!")


	def logout(self, verbose = False):
		"""
		Logs out an instance and makes sure it does not still have a session
		"""
		self.opener.open(self.logout_url).read()
		
		gv_home_page_contents = self.opener.open(self.gv_home_page_url).read()
		
		# Fine _rnr_se value
		key = re.search('name="_rnr_se".*?type="hidden".*?value="(.*?)"', gv_home_page_contents)
		
		if not key:
			self.logged_in = False
			if verbose:
				print "Google Logout Successful!"
		else:
			self.logged_in = True
			if verbose:
				print "Google Logout Failure."


	def extractsms(self):
		"""
		extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

		Example:
		gv_login = GoogleVoiceLogin('username', 'password')
		for msg in extractsms(gv_login):
			print str(msg)
		"""
		# accum message items here
		msgitems = [] 
		htmlsms = self.opener.open(self.gv_sms_page_url).read()

		# Extract all conversations by searching for a DIV with an ID at top level.
		# parse HTML into tree
		tree = BeautifulSoup(htmlsms)
		read_conversations = tree.findAll("div",attrs={"class" : "mr"})
		
		unread_conversations = tree.findAll("div",attrs={"class" : "mu"})
		for conversation in unread_conversations :
			# For each conversation, extract each row, which is one SMS message.
			ms3Classes = conversation.findAll("div",attrs={"class" : "ms3"})
			rows = ms3Classes[0].findAll("div",attrs={"class" : ""})
			# for all rows
			for row in rows :
				# For each row, which is one message, extract all the fields.
				# tag this message with conversation ID
				sender = row.findAll("span",attrs={"class" : "sf"})
				msg = row.findAll("span",attrs={"class" : ""})
				time = row.findAll("span",attrs={"class" : "ms"})
				
				global_time = conversation.findAll("span",attrs={"class" : "ms"})
				contact = conversation.findAll("span",attrs={"class" : "sf"})
				contact = contact[0].text.strip()
				contact = contact[1:-1]
				
				msgitem = {
					"time" : time[0].text.strip(),
					"global_time" : global_time[0].text.strip(),
					"Contact" : contact,
					"id" : conversation["id"], 
					"Sender" : sender[0].text.strip(),
					"text" : msg[0].text.strip()					
				}
				msgitems.append(msgitem)
				
			mark_sms_read_url = self.gv_sms_mark_read + conversation["id"] + '&read=1'
			self.opener.open(mark_sms_read_url).read()
		return msgitems


class TextSender():
    """
    Class used to send text messages.
    
    Example usage:
    
    gv_login = GoogleVoiceLogin('username', 'password')
    text_sender = TextSender(gv_login)
    text_sender.text = "This is an example"
    text_sender.send_text('555-555-5555')
    
    if text_sender.response:
        print "Success!"
     else:
        print "Fail!"
    """
    def __init__(self, gv_login):
        """ 
        Pass in a GoogleVoiceLogin object, set the text message 
        and then call send_text
        """
        self.opener = gv_login.opener
        self.key = gv_login.key
        self.sms_url = 'https://www.google.com/voice/sms/send/'
        self.text = ''

    def send_text(self, phone_number):
        """
        Sends a text message containing self.text to phone_number
        """
        sms_params = urllib.urlencode({
            '_rnr_se': self.key,
            'phoneNumber': phone_number,
            'text': self.text
        })
        # Send the text, display status message  
        self.response = "true" in self.opener.open(self.sms_url, sms_params).read()

class NumberDialer():
    """ 
    Class used to make phone calls.

    Example usage:

    gv_login = GoogleVoiceLogin('username', 'password')
    number_dialer = NumberDialer(gv_login)
    number_dialer.forwarding_number = 'number-to-call-you-at'

    number_dialer.place_call('number-to-call')

    if number_dialer.response:
        print "Success!"
     else:
        print "Fail!"
    """
    def __init__(self, gv_login):
        self.opener = gv_login.opener
        self.key = gv_login.key
        self.call_url = 'https://www.google.com/voice/call/connect/'
        self.forwarding_number = None
        self.phone_type = None

    def place_call(self, number):
        """ 
        Pass in a GoogleVoiceLogin object, set the forwarding_number
        and then call place_call('number-to-call')
        """
        call_params = urllib.urlencode({
            'outgoingNumber' : number,
            'forwardingNumber' : self.forwarding_number,
            'subscriberNumber' : 'undefined',
            'remember' : '0',
            'phoneType' : self.phone_type,
            '_rnr_se': self.key
        })

        # Send the text, display status message  
        self.response = self.opener.open(self.call_url, call_params).read()
