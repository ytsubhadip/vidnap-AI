import os
import time
from text_to_speech import text_to_speech_file
import subprocess

def text_to_speech(folder):
    print(folder)
    with open(f"user_upload/{folder}/desc.txt", "r") as f:
            text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)

def create_reel(folder):
    print(folder)
    command = f'''ffmpeg -f concat -safe 0 -i user_upload/{folder}/input.txt -i user_upload/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/rells/{folder}.mp4'''
    subprocess.run(command,shell=True,check=True)

if __name__=="__main__":
    while True:
        print("processing Queue....")
        with open("done.txt",'r') as f:
            done_folder = f.readlines()

            
        done_folder = [f.strip() for f in done_folder]
        folders = os.listdir("user_upload")
        for folder in folders:
            if folder not in done_folder:
                text_to_speech(folder) # generate audio .mp3 from desc text
                create_reel(folder) # convert the image and mp3 into a reel
                with open("done.txt","a") as f:
                    f.write(folder + "\n")
        time.sleep(4)
    