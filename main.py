import pyqrcode
import cv2
import os
import sys
from PIL import Image
from pyzbar.pyzbar import decode


# creates video from QR codes, the codes are generated from input file strings
# returns array of strings and video file name

def create_video(file_name, frame_number):
    string_arr = []
    qr_arr = []

    # get all words from file
    with open(file_name, 'r') as file:
        string_arr = file.read().splitlines()

    image_folder = 'images'

    # create folder or clear it
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    else:
        for f in os.listdir(image_folder):
            os.remove(os.path.join(image_folder, f))

    # generate QR codes from strings
    for string in string_arr:
        qr = pyqrcode.create(string)
        qr_arr.append(qr)
        qr.png(f'{image_folder}/{string}.png', scale=6)
    
    
    video_name = file_name[:-3] + 'avi'

    # create arr of images
    images = []
    for img in os.listdir(image_folder):
        if img.endswith('.png'):
            tmp = [img] * frame_number
            images.extend(tmp)
    
    frame = cv2.imread(os.path.join(image_folder, images[0])) # arr of frames
    height, width, _ = frame.shape

    #create video
    video = cv2.VideoWriter(video_name, 0, 60, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

    return video_name

# from video get strings, from which the QR codes were generated
# returns set of strings
def get_strings_from_video(video_name):
    frames_folder = 'frames'

    # create folder or clear it
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)
    else:
        for f in os.listdir(frames_folder):
            os.remove(os.path.join(frames_folder, f))

    vidcap = cv2.VideoCapture(video_name)
    success,image = vidcap.read()
    count = 0
    result = set()
    while success:
        cv2.imwrite(f'{frames_folder}/frame{count}.png', image)
        data = decode(Image.open(f'{frames_folder}/frame{str(count)}.png'))
        result.add(data[0].data.decode("utf-8"))
        success,image = vidcap.read()
        count += 1
    
    filename = f'{video_name[:-3]}txt'

    file = open(filename, 'w+')
    file.writelines(f'{line}\n' for line in list(result))
    
    return filename


# string_arr, video_name = create_video(FRAME_NUMBER, STRING_NUMBER, STRING_LENGTH)
# result = get_strings_from_video(video_name)
# # if True, then we got the same strings as we had in the beginning
# assert result == set(string_arr)

FRAME_NUMBER = 3 # number of frames for signle QR code

if __name__ == "__main__":
    print('Start')
    filename = sys.argv[1]
    if filename.endswith('.txt'):
        print('Transforming words into video')
        video_name = create_video(filename, FRAME_NUMBER)
        print(f'Created {video_name} video')
    else:
        print('Deciphering video into words')
        file_name = get_strings_from_video(filename)
        print(f'Words are written into {file_name}')
