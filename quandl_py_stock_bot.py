'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



#IF YOU FOUND THIS USEFUL, Please Donate some Bitcoin .... 1FWt366i5PdrxCC6ydyhD8iywUHQ2C7BWC
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
import json
import logging
import sys
import urllib
from time import time, sleep
import random
import time as systime
from statistics import mean, median
import numpy as np
# We are gonna use Scikit's LinearRegression model
from sklearn.linear_model import LinearRegression
import quandl
import math

#Joke here
#REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'

API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
API_KEY = '***************************************'
data = {"identifier":"***************************************","password": "***************************************"}

# FOR REAL....
# API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
# API_KEY = '***************************************'
# data = {"identifier":"***************************************","password": "***************************************"}

headers = {'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':API_KEY,
        'Version':'2'
		}

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)
 
headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print (R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print (R"X-SECURITY-TOKEN : " + x_sec_token)

#GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':API_KEY,
        'CST':CST_token,
		'X-SECURITY-TOKEN':x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)

for i in d['accounts']:
	if str(i['accountType']) == "SPREADBET":
		print ("Spreadbet Account ID is : " + str(i['accountId']))
		spreadbet_acc_id = str(i['accountId'])

#SET SPREAD BET ACCOUNT AS DEFAULT
base_url = REAL_OR_NO_REAL + '/session'
data = {"accountId":spreadbet_acc_id,"defaultAccount": "True"}
auth_r = requests.put(base_url, data=json.dumps(data), headers=authenticated_headers)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)
#ERROR about account ID been the same, Ignore! 

#--------------------FINISHED IG LOGIN------------------------
#--------------------FINISHED IG LOGIN------------------------
#--------------------FINISHED IG LOGIN------------------------
#--------------------FINISHED IG LOGIN------------------------

#KA.D.LLOY.DAILY.IP - LLoyds
#KA.D.BARC.DAILY.IP - Barclays
#epic_id = "KA.D.LLOY.DAILY.IP"
epic_id = "KA.D.BARC.DAILY.IP"

#QUAND_REF = "LSE/LLOY"
QUAND_REF = "LSE/BARC"

#UNIT TEST FOR OTHER STUFF
limitDistance_value = "1"
orderType_value = "MARKET"
size_value = "1"
expiry_value = "DFB"
guaranteedStop_value = True
currencyCode_value = "GBP"
forceOpen_value = True
stopDistance_value = "20" #Initial Stop loss, Worked out later per trade

base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

#DEBUG
# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)

MARKET_ID = d['instrument']['marketId']

#--------------------IG STUFF------------------------
#--------------------IG STUFF------------------------
#--------------------IG STUFF------------------------
#--------------------IG STUFF------------------------

#MORE INFORMATION HERE:
#http://help.quandl.com/article/320-where-can-i-find-my-api-key

quandl.ApiConfig.api_key = "quandl API Key here"
#data = quandl.get("LSE/UK3L", collapse="monthly", returns="numpy") #Good, But we do our own thing with these arrays
#data = quandl.get("LSE/UK3L", collapse="daily") #TOO MANY NaN's returned!!
#data = quandl.get("LSE/BARC", collapse="daily", start_date="2013-12-05", end_date="2017-12-08") #Automate this later
data = quandl.get(QUAND_REF, collapse="weekly")

#print (type(data))
#print (data)
tmp_price_list = data['Low'].values.tolist()
tmp_volume_list = data['Volume'].values.tolist()
high_prices = data['High'].values.tolist()
# print (tmp_price_list)
# print (tmp_volume_list)
main_list = []


for i in range(len(tmp_price_list)):
	tmp_list = []
	tmp_var_1 = tmp_price_list[i]
	tmp_var_2 = tmp_volume_list[i]
	if math.isnan(tmp_var_1):
		tmp_var_1 = 0
	if math.isnan(tmp_var_2):
		tmp_var_2 = 0
	# print (tmp_var_1)
	# print (tmp_var_2)
	tmp_list.append(float(tmp_var_1))
	tmp_list.append(float(tmp_var_2))
	main_list.append(tmp_list)


#TWO LISTS FOR PREDICTIONS
#main_list is made up of low prices and volumes
#high_prices = is made up of high prices
#print (main_list)

for i in range(len(high_prices)):
	if math.isnan(high_prices[i]):
		high_prices[i] = 0

#print (high_prices)
main_list = np.asarray(main_list)
high_prices = np.asarray(high_prices)

PREDICT_FOR = quandl.get(QUAND_REF, collapse="daily")
PREDICT_FOR_price_list = data['Low'].values.tolist()
PREDICT_FOR_volume_list = data['Volume'].values.tolist()
PREDICT_x = PREDICT_FOR_price_list[-1]
PREDICT_y = PREDICT_FOR_volume_list[-1]

print ("PREDICT_x : " + str(PREDICT_x))
print ("PREDICT_y : " + str(PREDICT_y))

# Initialize the model then train it on the data
genius_regression_model = LinearRegression()
genius_regression_model.fit(main_list,high_prices)
# Predict the corresponding value of Y for X
pred_ict = [PREDICT_x,PREDICT_y]
pred_ict = np.asarray(pred_ict) #To Numpy Array, hacky but good!! 
pred_ict = pred_ict.reshape(1, -1)
price_prediction = genius_regression_model.predict(pred_ict)
print ("PRICE PREDICTION FOR " + str(QUAND_REF) + str(price_prediction))

score = genius_regression_model.score(main_list,high_prices)
predictions = {'intercept': genius_regression_model.intercept_, 'coefficient': genius_regression_model.coef_,   'predicted_value': price_prediction, 'accuracy' : score}
print ("-----------------DEBUG-----------------")
print (score)
print (predictions)
print ("-----------------DEBUG-----------------")

#--------------------------IG INDEX--------------------

base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)
# print ("-----------------DEBUG-----------------")
# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)
# print ("-----------------DEBUG-----------------")
current_price = d['snapshot']['bid']

price_diff = current_price - price_prediction
print ("Price Difference Away (Point's) : " + str(price_diff))
#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
predict_accuracy = 0.91

if price_diff < 0 and score > predict_accuracy: #BUY
	DIRECTION_TO_TRADE = "BUY"
	DIRECTION_TO_CLOSE = "SELL"
	DIRECTION_TO_COMPARE = 'bid'
	DO_A_THING = True
	#-----------------------------
	limitDistance_value = "1"
	orderType_value = "MARKET"
	size_value = "10"
	expiry_value = "DFB"
	guaranteedStop_value = True
	currencyCode_value = "GBP"
	forceOpen_value = True
	stopDistance_value = "14" #Initial Stop loss, Worked out later per trade
elif price_diff > 0 and score > predict_accuracy: #SELL
	DIRECTION_TO_TRADE = "SELL"
	DIRECTION_TO_CLOSE = "BUY"
	DIRECTION_TO_COMPARE = 'offer'
	DO_A_THING = True
	#-----------------------------
	limitDistance_value = "1"
	orderType_value = "MARKET"
	size_value = "10"
	expiry_value = "DFB"
	guaranteedStop_value = True
	currencyCode_value = "GBP"
	forceOpen_value = True
	stopDistance_value = "14" #Initial Stop loss, Worked out later per trade


base_url = REAL_OR_NO_REAL + '/positions/otc'
authenticated_headers = {'Content-Type':'application/json; charset=utf-8',
		'Accept':'application/json; charset=utf-8',
		'X-IG-API-KEY':API_KEY,
		'CST':CST_token,
		'X-SECURITY-TOKEN':x_sec_token}
		
data = {"direction":DIRECTION_TO_TRADE,"epic": epic_id, "limitDistance":limitDistance_value, "orderType":orderType_value, "size":size_value,"expiry":expiry_value,"guaranteedStop":guaranteedStop_value,"currencyCode":currencyCode_value,"forceOpen":forceOpen_value,"stopDistance":stopDistance_value}
r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers)
# MAKE AN ORDER
d = json.loads(r.text)
deal_ref = d['dealReference']
systime.sleep(2)
#CONFIRM MARKET ORDER
base_url = REAL_OR_NO_REAL + '/confirms/'+ deal_ref
auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)
DEAL_ID = d['dealId']
print("DEAL ID : " + str(d['dealId']))
print(d['dealStatus'])
print(d['reason'])
	
# the trade will only break even once the price of the asset being traded has surpassed the sell price (for long trades) or buy price (for short trades). 
#READ IN INITIAL PROFIT
	
base_url = REAL_OR_NO_REAL + '/positions/'+ DEAL_ID
auth_r = requests.get(base_url, headers=authenticated_headers)		
d = json.loads(auth_r.text)

# DEBUG
# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)

if DIRECTION_TO_TRADE == "SELL":
	PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][DIRECTION_TO_COMPARE])
	PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(size_value)
	print ("Profit/Loss : " + str(PROFIT_OR_LOSS))
else:
	PROFIT_OR_LOSS = float(d['market'][DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
	PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(size_value)
	print ("Profit/Loss : " + str(PROFIT_OR_LOSS))
	
#KEEP READING IN FOR PROFIT
try:
	while PROFIT_OR_LOSS < 0.5: #Over 50p otherwise not worth it and price could move
		base_url = REAL_OR_NO_REAL + '/positions/'+ DEAL_ID
		auth_r = requests.get(base_url, headers=authenticated_headers)		
		d = json.loads(auth_r.text)
		
		if DIRECTION_TO_TRADE == "SELL":
			PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][DIRECTION_TO_COMPARE])
			PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(size_value))
			print ("Profit/Loss : " + str(PROFIT_OR_LOSS))
			systime.sleep(2) #Don't be too keen to read price
		else:
			PROFIT_OR_LOSS = float(d['market'][DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
			PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(size_value))
			print ("Profit/Loss : " + str(PROFIT_OR_LOSS))
			systime.sleep(2) #Don't be too keen to read price
			
		# ARTIFICIAL_STOP_LOSS = int(size_value) * STOP_LOSS_MULTIPLIER
		# ARTIFICIAL_STOP_LOSS = ARTIFICIAL_STOP_LOSS * -1 #Make Negative, DO NOT REMOVE!!
		# print (PROFIT_OR_LOSS)
		# print (ARTIFICIAL_STOP_LOSS)
		
		# if PROFIT_OR_LOSS < ARTIFICIAL_STOP_LOSS:
			# #CLOSE TRADE/GTFO
			# print ("WARNING!! POTENTIAL DIRECTION CHANGE!!")
			# SIZE = size_value
			# ORDER_TYPE = orderType_value
			# base_url = REAL_OR_NO_REAL + '/positions/otc'
			# data = {"dealId":DEAL_ID,"direction":DIRECTION_TO_CLOSE,"size":SIZE,"orderType":ORDER_TYPE}
			# #authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
			# authenticated_headers_delete = {'Content-Type':'application/json; charset=utf-8',
			# 'Accept':'application/json; charset=utf-8',
			# 'X-IG-API-KEY':API_KEY,
			# 'CST':CST_token,
			# 'X-SECURITY-TOKEN':x_sec_token,
			# '_method':"DELETE"}
			# auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)	
			# #DEBUG
			# print(r.status_code)
			# print(r.reason)
			# print (r.text)
			# systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER)) #Obligatory Wait before doing next order
					
except Exception as e:
	#print(e) #Yeah, I know now. 
	print ("ERROR : ORDER MIGHT NOT BE OPEN FOR WHATEVER REASON")
	#WOAH CALM DOWN! WAIT .... STOP LOSS MIGHT HAVE BEEN HIT
	systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER))
	pass

		
if PROFIT_OR_LOSS > 0:
	print ("ASSUME PROFIT!!")
	SIZE = size_value
	ORDER_TYPE = orderType_value
	
	base_url = REAL_OR_NO_REAL + '/positions/otc'
	data = {"dealId":DEAL_ID,"direction":DIRECTION_TO_CLOSE,"size":SIZE,"orderType":ORDER_TYPE}
	#authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
	authenticated_headers_delete = {'Content-Type':'application/json; charset=utf-8',
			'Accept':'application/json; charset=utf-8',
			'X-IG-API-KEY':API_KEY,
			'CST':CST_token,
			'X-SECURITY-TOKEN':x_sec_token,
			'_method':"DELETE"}
	
	auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)	
	#CLOSE TRADE
	print(r.status_code)
	print(r.reason)
	print (r.text)
	
	# #CONFIRM CLOSE - FUTURE
	# base_url = REAL_OR_NO_REAL + '/confirms/'+ deal_ref
	# auth_r = requests.get(base_url, headers=authenticated_headers)
	# d = json.loads(auth_r.text)
	# DEAL_ID = d['dealId']
	# print("DEAL ID : " + str(d['dealId']))
	# print(d['dealStatus'])
	# print(d['reason'])
	
	systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER)) #Obligatory Wait before doing next order
