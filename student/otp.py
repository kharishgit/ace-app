# import urllib,urllib.request,urllib.parse
# class SendSms:
#     def __init__(self,mobilenumber,message):
#         url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
#         values = {'user' : 'acemanjeri',
#         'passwd' : 'babu2769220',
#         'message' : message,
#         'mobilenumber':mobilenumber,
#         'mtype':'N',
#         'DR':'Y'
#         }
#         data = urllib.parse.urlencode(values)
#         print(data)
#         data = data.encode('utf-8')
#         print(data)
        
#         request = urllib.request.Request(url,data)
#         response = urllib.request.urlopen(request)
#         print(data)
        
#         print (response.read().decode('utf-8'))
        
        
# sms = SendSms('919567238587', 'Hello, World!')


# import urllib, urllib.request, urllib.parse

# class SendSms:
#     def __init__(self):
#         url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
#         values = {
#             'user': 'acemanjeri',
#             'passwd': 'babu2769220',
#             'message': 'Dear test, Your OTP for accessing AceApp is 123456. Do not share your OTP with anyone. -AceApp testing',
#             'mobilenumber': 919562313456,
#             'mtype': 'N',
#             'DR': 'Y',
#             'sid':'ACEAPP'
#         }
#         data = urllib.parse.urlencode(values)
#         data = data.encode('utf-8')
#         request = urllib.request.Request(url, data)
#         response = urllib.request.urlopen(request)
#         response_str = response.read().decode('utf-8')
#         print(response_str)
#         if "OK:" in response_str:
#             print("Message sent successfully.")
#         else:
#             print("Failed to send message.")

# # Create an object of SendSms class and send the message
# sms = SendSms()


# from datetime import datetime, timedelta

# time1_str = "7:10:28.770708"
# time2_str = "6:59:44.694383"

# time1 = datetime.strptime(time1_str, '%H:%M:%S.%f')
# print(time1)
# time2 = datetime.strptime(time2_str, '%H:%M:%S.%f')
# print(time2)
# print(time1-time2)

# duration = (time1 - time2).total_seconds()

# print(duration)


# import http.client

# conn = http.client.HTTPSConnection("pincode.p.rapidapi.com")

# payload = "{\r\n    \"searchBy\": \"pincode\",\r\n    \"value\": 670007\r\n}"

# headers = {
#     'content-type': "application/json",
#     'Content-Type': "application/json",
#     'X-RapidAPI-Key': "cb42d2c114mshaae9432bba83371p19b29fjsn725500060119",
#     'X-RapidAPI-Host': "pincode.p.rapidapi.com"
#     }

# conn.request("POST", "/", payload, headers)

# res = conn.getresponse()
# data = res.read()
# print('))))))))))')
# print(data.decode("utf-8"))

# import requests

# url = "https://api.opencagedata.com/geocode/v1/json?q=India&countrycode=in&limit=1000&key=8838e8c231874f959e0ea2f84c758787"

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     results = data.get('results', [])
#     places = [result.get('formatted') for result in results]
#     print(places)
# else:
#     print("Error:", response.status_code)


import requests


def sendsms(number,otp):
    response = requests.get(f"https://api.smscountry.com/SMSCwebservice_bulk.aspx?User=acemanjeri&passwd=babu2769220&mobilenumber={number}&message=Dear%20user,%20Your%20OTP%20for%20accessing%20AceApp%20is%20{otp}.%20Do%20not%20share%20your%20OTP%20with%20anyone.%20-AceApp&sid=ACEAPP&mtype=N&DR=Y")
    try:

        if response.status_code == 200:
            # Request was successful
            data = response.json()  # Parse response content as JSON
            print(data)
            # return Response(data,'data')
        else:
            # Request was not successful
            print("Request failed with status code:", response.status_code)
    except:
        pass


#common email function
from django.core.mail import EmailMessage
def commonmail(mail_subject,to_email,body):
    #bodyexample
        # nameuser = (user.username)
        # body = f"Hi {nameuser},\n\n Thank you for registering with us.\n We will sent a confirmation message in Whatsapp and Email after verification.\n Then You can log in to your account using this link. \n\nLogin Link: https://v2.aceonline.app/login \n\n\nACE EDUCATION CENTER,Manjeri"
    #endbodyexampl
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    send_email.send()
