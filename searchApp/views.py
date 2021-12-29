from django.shortcuts import render
import requests
from django.conf import settings

def searchQuerry(request):

    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_parameters = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 10,
            'type' : 'video',
            'regionCode' : 'IN'
        }

        data = requests.get(url=search_url,params=search_parameters)
        results = data.json()['items']
        
        videoId_list = []
        for result in results:
            videoId_list.append(result['id']['videoId'])

        video_parameters = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails,statistics',
            'id' : ','.join(videoId_list),
            'maxResults': 10
        }

        video_data = requests.get(video_url,params=video_parameters)
        videos_results = video_data.json()['items']

        for video_result in videos_results:
            data = {
                'title' : video_result['snippet']['title'],
                'id' : video_result['id'],
                'thumbnail' : video_result['snippet']['thumbnails']['high']['url'],
                'views' : video_result['statistics']['viewCount'],
                'url' : f'https://www.youtube.com/watch?v={ video_result["id"] }'
            }
            videos.append(data)

    final_data = {
        'videos' : videos
    }
    return render(request,'searchApp/index.html',final_data)
