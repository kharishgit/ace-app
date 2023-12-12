# import qrcode
# from PIL import Image
# import requests
# import json
 
# # taking image which user wants
# # in the QR code center
# def get_image(url):
#     response = requests.get(url='https://v2devapi.aceonline.app/accounts/questionimages/283/')

# # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#     # Get the response data as bytes
#         response_data = response.content
#         data=json.loads(response_data)
#         res= requests.get(url=data['url'])
#         print(res.content)
#         return res.content

#     # Now you can work with the response data as needed
#     # For example, you can save it to a file or process it further
    
#     # # Example: Save the response data to a file
#     #     with open('image_data.jpg', 'wb') as file:
#     #         file.write(response_data)
#     else:
#     # Handle the case where the request was not successful
#         print(f"Request failed with status code: {response.status_code}")


# def qr():
#     # Logo_link = 'g4g.jpg'
#     Logo_link=get_image("llll")
#     logo = Image.open(Logo_link)
    
#     # taking base width
#     basewidth = 100
    
#     # adjust image size
#     wpercent = (basewidth/float(logo.size[0]))
#     hsize = int((float(logo.size[1])*float(wpercent)))
#     logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
#     QRcode = qrcode.QRCode(
#         error_correction=qrcode.constants.ERROR_CORRECT_H
#     )
    
#     # taking url or text
#     url = 'https://www.geeksforgeeks.org/'
    
#     # adding URL or text to QRcode
#     QRcode.add_data(url)
    
#     # generating QR code
#     QRcode.make()
    
#     # taking color name from user
#     QRcolor = 'Blue'
    
#     # adding color to QR code
#     QRimg = QRcode.make_image(
#         fill_color=QRcolor, back_color="white").convert('RGB')
    
#     # set size of QR code
#     pos = ((QRimg.size[0] - logo.size[0]) // 2,
#         (QRimg.size[1] - logo.size[1]) // 2)
#     QRimg.paste(logo, pos)
    
#     # save the QR code generated
#     QRimg.save('gfg_QR.png')
    
#     print('QR code generated!')
    
from accounts.api.authhandle import attendanceIns
import requests
from PIL import Image
import qrcode
import io
import datetime

from accounts.models import QuestionImage

def get_image_url(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            image_url = data.get('url')
            return image_url
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def qr(id):
    # base_url = 'https://v2devapi.aceonline.app/accounts/questionimages/283/'
    # image_url = get_image_url(base_url)
    image_url = QuestionImage.objects.get(id=283).questionimage.url

    if image_url:
        try:
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            if 'image' in image_response.headers.get('Content-Type', ''):
                image_data = image_response.content
                # print(image_data)
                image_file = io.BytesIO(image_data)
                logo = Image.open(image_file)
                
                # taking base width
                basewidth = 100
                
                # adjust image size
                wpercent = (basewidth/float(logo.size[0]))
                hsize = int((float(logo.size[1])*float(wpercent)))
                logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
                QRcode = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_H
                )
                token=attendanceIns.get_token(payload={'id':id})
                # taking url or text
                # url = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQzLCJ1c2VybmFtZSI6IkF6bGFtIGF6IiwiZW1haWwiOiJhemxhbWFiZHVsbGFhekBnbWFpbC5jb20iLCJhZG1pbiI6ZmFsc2UsInJvbGUiOmZhbHNlLCJmYWN1bHR5IjpmYWxzZSwic3R1ZGVudCI6dHJ1ZSwiaWF0IjoxNjkxNzI1NDk1LCJleHAiOjE2OTI1ODk0OTV9.ds5ZI5RYETN6iLCxWnqdaNWIQA4JgXQpz5OLdzVSYDw'
                # url = str(datetime.datetime.now())
                url = token
                print(url)
                # adding URL or text to QRcode
                QRcode.add_data(url)
                
                # generating QR code
                QRcode.make()
                
                # taking color name from user
                QRcolor = '#34909e'
                
                # adding color to QR code
                QRimg = QRcode.make_image(
                    fill_color=QRcolor, back_color="white").convert('RGB')
                
                # set size of QR code
                pos = ((QRimg.size[0] - logo.size[0]) // 2,
                    (QRimg.size[1] - logo.size[1]) // 2)
                QRimg.paste(logo, pos)
                
                # save the QR code generated
                # QRimg.save('gfg_QR.png')
                
                print('QR code generated!')
                return QRimg

                # Continue with generating the QR code and adding the image as needed
                # ...
            else:
                print("The response does not contain an image.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Failed to obtain the image URL.")