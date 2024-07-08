from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from detection.camera import VideoCamera
from django.http import StreamingHttpResponse, JsonResponse
import cv2
# Create your views here.
import subprocess
# Load the pre-trained model
import os
from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
from django.shortcuts import render

from django.http import HttpResponse
import moviepy.editor
from moviepy.editor import VideoFileClip, concatenate_videoclips

import os


video= VideoCamera()
# Path to your images folder
images_folder = 'D:/GraduationProjecGPmainproject/GraduationProject-main/project1/blog/static/videos'

# Mapping of letters to their corresponding video file names
sign_language_dict = {
    'انت': 'you.mp4',
    'انا': 'i.mp4',
    'جيد': 'good.mp4',
    'احبك': 'love.mp4',
    'خ': 'khaa.webm',
    'د': 'dal.webm',
    'ذ': 'zal.webm',
    ' ': 'space.webm',
}

def translate(request):
    if request.method == 'POST':
        text_to_translate = request.POST.get('text', '')  # Retrieve text from POST data

        # Translate text to sign language videos
        video_path = text_to_sign_language(text_to_translate)

        if video_path:
           # video_path='D:/GraduationProjecGPmainproject\GraduationProject-main\project1\blog\static\videos\output_video.mp4'
            # Pass the video path to the template for rendering
            return render(request, 'detection/translation.html', {'video_path': video_path})

    return HttpResponse("Invalid request method.")

def text_to_sign_language(text):
    video_paths = []
 
    words = text.split()
      # Split the text into words
    for word in words:
        if word in sign_language_dict:
            video_filename = sign_language_dict[word]
            video_path = os.path.join(images_folder, video_filename)
            if os.path.exists(video_path):
                video_paths.append(video_path)
            else:
                print(f"Video file not found: {video_path}")
    
    if video_paths:
        # Combine videos into a single output video using MoviePy
        output_video_path = os.path.join(images_folder, 'output_video.mp4')
        combine_videos(video_paths, output_video_path)
        return output_video_path
    
    return None



def combine_videos(video_paths, output_path):
    # Load video clips
    clips = [VideoFileClip(path) for path in video_paths]

    # Concatenate the video clips
    final_clip = concatenate_videoclips(clips)

    # Write the concatenated video to a file
    final_clip.write_videofile(output_path)



# Path to your images folder



cnt=0
def zyadaa(request):
	return render(request, 'detection/zyada.html')
def predict(request):
    return render(request, 'detection/predict.html')
def trans(request):
    return render(request, 'detection/translation.html')
def gen(camera):
    while True:
        frame, _ = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def video_feed(request):
        global video
        video= VideoCamera()
        return StreamingHttpResponse(gen(video),content_type='multipart/x-mixed-replace; boundary=frame')
def get_result(request):
    _, result_text = video.get_frame()
    return JsonResponse({'result': result_text})

#def Arrayemotion(request):
#	print(array)