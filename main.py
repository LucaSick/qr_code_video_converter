import random
import string
import pyqrcode
import cv2
import os
from PIL import Image
from pyzbar.pyzbar import decode

# generate random string
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# creates video from QR codes, the codes are generated from random strings
# returns array of strings and video file name
def create_video(frame_number, string_number, string_length):
    string_arr = []
    qr_arr = []

    #generate strings
    for i in range(string_number):
        string_arr.append(get_random_string(string_length))

    # generate QR codes from strings
    for string in string_arr:
        qr = pyqrcode.create(string)
        qr_arr.append(qr)
        for j in range(frame_number):
            qr.png('images/' + string + str(j) + '.png', scale=6)
    
    image_folder = 'images'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")] # arr of images
    frame = cv2.imread(os.path.join(image_folder, images[0])) # arr of frames
    height, width, _ = frame.shape

    #create video
    video = cv2.VideoWriter(video_name, 0, 60, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

    return string_arr, video_name

# from video get strings, from which the QR codes were generated
# returns set of strings
def get_strings_from_video(video_name):
    vidcap = cv2.VideoCapture(video_name)
    success,image = vidcap.read()
    count = 0
    result = set()
    while success:
        cv2.imwrite('frames/frame%d.png' % count, image)
        data = decode(Image.open('frames/frame' + str(count) + '.png'))
        result.add(data[0].data.decode("utf-8"))
        success,image = vidcap.read()
        count += 1
    
    return result
    

FRAME_NUMBER = 3 # number of frames for signle QR code
STRING_NUMBER = 100 # number of string or QR codes
STRING_LENGTH = 8 # length of strings

string_arr, video_name = create_video(FRAME_NUMBER, STRING_NUMBER, STRING_LENGTH)
result = get_strings_from_video(video_name)

# if True, then we got the same strings as we had in the beginning
assert result == set(string_arr)
