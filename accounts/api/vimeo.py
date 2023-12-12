import requests
from MobileApp.serializers import stream_vimeo_video
from aceapp.settings.base import vimeo_access_token
from rest_framework.response import Response


def get_540p_video_link(files):
    for file_info in files:
        if file_info.get('public_name') == '540p':
            return file_info.get('link')
    return None  # Return None if the 540p quality is not found

def upload_video_to_vimeo(file, video_name, video_description):
    # access_token = 'd9a01813f50cf7a68e966e285d557f36'
    access_token = vimeo_access_token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.vimeo.*+json;version=3.4',
    }

    video_file_size = file.size

    data = {
        'upload': {
            'approach': 'tus',
            'size': str(video_file_size)
        },
        'name': video_name,
        'description': video_description
    }

    # Step 1: Create the video
    response = requests.post('https://api.vimeo.com/me/videos', headers=headers, json=data, verify=False)
    if response.status_code == 200:
        video_data = response.json()
        print(video_data,"******************")
        upload_link = video_data['upload']['upload_link']
        video_uri = video_data['uri']
        video_id = video_uri.split('/')[-1]  # Extract the video ID from the URI
        desired_uri = f'/video/{video_id}'  # Construct the desired URI format

        # Step 2: Upload the video file
        headers = {
            'Tus-Resumable': '1.0.0',
            'Upload-Offset': '0',
            'Content-Type': 'application/offset+octet-stream'
        }
        response = requests.patch(upload_link, headers=headers, data=file)
        print(response.links,'KKKK')
        print(response.status_code)
        if response.status_code == 204:
            # Step 3: Verify the upload
            response = requests.head(upload_link, headers=headers)
            if response.status_code == 200:
                upload_status = response.headers.get('Upload-Status')
                upload_length = response.headers.get('Upload-Length')
                upload_offset = response.headers.get('Upload-Offset')

                if upload_length == upload_offset:
                    print(stream_vimeo_video(video_id),"#############")
                    # print(return.response,'dddd')
                    print(video_id,'PPPP')
                    print(response,"%%%%%")
                    # Call the stream_vimeo_video function and get the response
                    response = stream_vimeo_video(video_id)
                    print(response,"DDDDD")

                    # Get the 540p quality video link
                    link_540p = get_540p_video_link(response)

                    if link_540p:
                        print("540p video link:", link_540p)
                    else:
                        print("540p quality not found")
                    

                    return {
                        'message': 'Video upload complete',
                        'link': f'https://player.vimeo.com{desired_uri}'
                    }
                elif upload_length != upload_offset:
                    return {'error': 'Video upload incomplete'}
                else:
                    return {'error': 'Error verifying upload'}
        else:
            return {'error': 'Video upload failed'}
    else:
        return {'error': 'Video creation failed'}



from rest_framework.pagination import PageNumberPagination

class SinglePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'pagesize'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and 'http://' in next_url:
            next_url = next_url.replace('http://', 'https://')
        if previous_url is not None and 'http://' in previous_url:
            previous_url = previous_url.replace('http://', 'https://')

        return Response({
            'count': self.page.paginator.count,
            'next': next_url,
            'previous': previous_url,
            'current' : self.page.number,
            'results': data
        })

    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0 and (self.max_page_size is None or page_size <= self.max_page_size):
                    return page_size
            except ValueError:
                pass
        return self.page_size
