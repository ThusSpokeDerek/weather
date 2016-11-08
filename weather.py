import env
import urllib
import requests
import json
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

def weatherFromYahoo():
	zip_converter = requests.get("http://arguments.callee.info/sandbox/zip-woeid/?zip=" + zipcode)
	woeid_find = BeautifulSoup(zip_converter.content, "html.parser")
	woeid = woeid_find.findAll("strong")
	woeid = woeid[1].text
	yahoo = requests.get(r"https://www.yahoo.com/news/weather/\*/\*/\*-" + woeid)
	yahoo_content = BeautifulSoup(yahoo.content, "html.parser")
	city = yahoo_content.findAll("h1", { "class" : "city" })
	if city[0].text:
		temp = yahoo_content.findAll("span", { "class" : "Va(t)" })
		weatherFromYahoo.temp = temp[0].text
		desc = yahoo_content.findAll("span", { "class" : "description"})
		weatherFromYahoo.desc = desc[0].text
		prec_approx = yahoo_content.findAll("span", { "class" : "M(5px) D(ib)"})
		weatherFromYahoo.prec_approx = prec_approx[0].text
		temp_feel_like = yahoo_content.findAll("li", { "class" : "item BdB Cf Py(8px) Fz(1.1em) Bds(d) Bdbc(#fff.12)"})
		weatherFromYahoo.temp_feel_like = temp_feel_like[0].text[-3:][:-1]
		# print 'temperature is ' + temp[0].text + ' F'
		# print desc[0].text
		# print 'Expected precipitation is: ' + prec_approx[0].text
		# print temp_feel_like[0].text[-3:][:-1]
def weatherFromNOAA():
	google_api = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address=" + zipcode)
	json = google_api.json()['results'][0]['geometry']['bounds']['northeast']
	lat = str(json['lat'])
	lon = str(json['lng'])
	noaa = requests.get("http://forecast.weather.gov/MapClick.php?lat=" + lat + "&lon=" + lon)
	noaa_content = BeautifulSoup(noaa.content, "html.parser")
	city = noaa_content.findAll("h2", { "class" : "panel-title" })
	if city[0].text:
		temp = noaa_content.findAll("p", { "class" : "myforecast-current-lrg" })
		weatherFromNOAA.temp = temp[0].text[:-2]
		desc = noaa_content.findAll("p", { "class" : "myforecast-current"})
		weatherFromNOAA.desc = desc[0].text
		more_desc = noaa_content.findAll("div", { "class" : "col-sm-10 forecast-text"})
		weatherFromNOAA.more_desc = more_desc[0].text

		# print 'temperature is ' + temp[0].text[:-2] + ' F'
		# print desc[0].text.replace(" ", "")
		# print more_desc[0].text
weatherFromNOAA()
weatherFromYahoo()

try:
	if weatherFromYahoo.temp != weatherFromNOAA.temp:
		avg_temp = (int(weatherFromYahoo.temp)+int(weatherFromNOAA.temp))/2

	if weatherFromYahoo.desc.replace(" ","").strip().lower() != weatherFromNOAA.desc.replace(" ","").strip().lower():
		raise ValueError('just continue its ok')
except ValueError:
	weatherFromYahoo.desc =  weatherFromYahoo.desc

account_sid = env.sid # Your Account SID from www.twilio.com/console
auth_token  = env.token  # Your Auth Token from www.twilio.com/console
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
	body='The temperature currently is ' + weatherFromNOAA.temp + ' and ' + weatherFromYahoo.desc + '. ' + 'The tempature feels like its ' + weatherFromYahoo.temp_feel_like + '. ' + 'More info: ' + weatherFromNOAA.more_desc,
    to=env.cell,    # Replace with your phone number
    from_=env.twilio_num) # Replace with your Twilio number
