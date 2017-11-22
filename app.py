# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# import requests
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    
    '''
    #Google Location API Integration Working fine
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=28.7041,77.1025"
    yql_url = baseurl + "&format=json"
    result = urlopen(yql_url).read()
    data1 = json.loads(result)
    res = makeWebhookResult_1(data1['results'][0]['address_components'][1]['long_name'])
    '''
    #Yatra Flight Rest API Integration
#     baseurl = "https://flight.yatra.com/air-service/dom2/search?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=DEL&originCountry=IN&destination=BLR&destinationCountry=IN&flight_depart_date=25/11/2017&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-homeUrl"
#     baseurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=28.7041,77.1025"
   
#     Gobaseurl = "https://www.goibibo.com/hotels/search-data/?app_id=6cdea2ed&app_key=21851393be2971afb5cdf941c20e4390&vcid=710870868236923145&ci=20171003&co=20171124&r=1-1_0"
#     Hotbaseurl = "http://api.travelguru.com/f1/v1/api/hotels/00101778?apiKey=OKMNBxsjHO7JgRMztkt5&type=content"
    VivekBaseurl = "https://secure.yatra.com/ccwebapp/mobile/flight/mdomios/book2.htm?suc=true&merchant_code=yatra&appVersion=204&hk=0eVKALJLFcVSCxQLN13KKQ&mid=rzp_live_Ei1Z14MSrfWuGj&product_code=mdomandroid&type=flights&deviceId=98f6eb15002f212d&pricingId=1b5388e6-082e-48d2-bbda-a010775dd414&mode=pur&searchId=6c4c2300-7af6-488e-a1af-7e61edc44785&osVersion=22&txnid=pay_94OomCYjuZmKzi&amount=2891600&mtxnid=112211775121632-2391498231151&psuc=true&sessionId=98f6eb15002f212d15113285793977025&payment_gateway_response_code=4001&ttid=112211775121632&wallet_id=2C36U1L21N5H77R1&pg=razor_pay&payment_gateway_response_message=Success&desc=Success&wallet_amount=300"

    
#     yql_url = Gobaseurl + "&format=json"
#     yql_url = Hotbaseurl + "&format=json"
    yql_url = VivekBaseurl + "&format=json"

    result = urlopen(yql_url).read()
    data = json.loads(result)
    if not data:
       data1 = "No Response from API"
    else:
       data1 = "Getting Response from API"
    
    res = makeWebhookResult_1(data['interationType'])
#     res = makeWebhookResult_1(data['data']['content']['address'])    
#   res = makeWebhookResult_1(data['results'][0]['address_components'][1]['long_name'])
#     res = makeWebhookResult_1(data['city_meta_info']['amenities']['Business Services'])
    return res
     
    '''
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult_1(data)
    return res
    '''
    

def makeWebhookResult_1(data):
    speech = data
#     speech = "API Is Working fine"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
