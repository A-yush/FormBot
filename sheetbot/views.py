from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json,re,json,requests
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def sheetAccess(pos,stat):
	scope=['https://spreadsheets.google.com/feeds']
	credentials=ServiceAccountCredentials.from_json_keyfile_name('gspread_service.json',scope)
	gc=gspread.authorize(credentials)
	ss=gc.open("sheetTest")
	wks=ss.get_worksheet(0) 	
	wks.update_acell(pos,stat)

PAGE_ACCESS_TOKEN='EAAQemtiTbv4BAI1mkQ2ZAPKAQCZBlafO59UHdXBktJCE68Wpb7uNM4seeni1SY4qGJQMgPoeR3MTED2BJco8aX85kaqKgNjRQlUKN83FkJOeeJCjpsBpZCncWPlK8G4SRc34wLgMm6cjj52ACLab3TNWDrZAmxAtGmUIZAoOXPgZDZD'
VERIFY_TOKEN='654321'

class sheetView(generic.View):
	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error,Invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)
	def post(self,request,*args,**kwargs):
		incoming_msgs=json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_msgs['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)
					post_fb_msg(message['sender']['id'],message['message']['text'])
			return HttpResponse()

def post_fb_msg(fbid,received_msg):
	spread_text=''
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	pprint(user_details)
	tokens=re.sub(r"[^a-zA-Z0-9\s]",' ',received_msg).lower().split()
	for token in tokens:
		 list1=['hy','hello','sup','hola','hey']
		 spread_text="Hy"+user_details['first_name']+"I am form Bot.To fill the form please answer the following questions"

		 if token in list1:
		 	spread_text="Hy"+user_details['first_name']+"I am form Bot.To fill the form please answer the following questions"
		 	print(spread_text)
			
	post_response_message(fbid,spread_text)     

def post_response_message(fbid,spread_text):
	post_msg_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":spread_text}})
	status=requests.post(post_msg_url,headers={"content-Type":"application/json"},data=response_msg)




#sheetAccess('A4','bamboo')