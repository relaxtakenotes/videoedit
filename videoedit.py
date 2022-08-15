import pyperclip
import subprocess
import shlex
import sys
import ctypes
import shlex
import json

def runCMD(command):
    process = subprocess.Popen(shlex.split(command), stdout=sys.stdout, stderr=sys.stdout)
    process.wait()

def compressVideo(path, mode):
    dataRaw = subprocess.run(shlex.split(f'ffprobe -i {path} -v quiet -print_format json -show_format -show_streams -hide_banner'), stdout=subprocess.PIPE).stdout
    dataJSON = json.loads(dataRaw)
    duration = float(dataJSON['format']['duration'])
    size = 0
    endPath = "empty"
    if mode == "discord":
        size = 62000
        end_path = path.replace(".mp4", "_compressed8.mp4")
    elif mode == "nitro":
        size = 790000
        end_path = path.replace(".mp4", "_compressed100.mp4")
    calculated_bitrate = math.floor(size/duration)
    runCMD(f"ffmpeg -i {path} -c:v h264_amf -vf scale=1280:720,setsar=1 -usage 0 -quality 0 -rc 2 -vbaq true -b:v {calculated_bitrate}K -c:a copy {end_path}")

def upscaleVideo(path, res):
    end_path = path.replace(".mp4", f"_upscaled.mp4")
    runCMD(f"ffmpeg -i {path} -c:v h264_amf -vf scale={res},setsar=1 -usage 0 -quality 0 -rc 0 -qp_p 21 -qp_i 21 -c:a copy {end_path}")

def main():
    path = pyperclip.paste()

    welcomeString = f"Video path: {path}\n"
    welcomeString += "Choose what to do with it. \n"
    welcomeString += "(D)iscord, Discord (N)itro, (U)pscale, (R)eload path: "
    choice = input(welcomeString).lower()

    match choice:
        case "d":
            compressVideo(path, "discord")
        case "n":
            compressVideo(path, "nitro")
        case "u":
            res = int(input("(1) 1080p | (2) 1440p: "))
            if res == 1:
                upscaleVideo(path, "1920:1080")
            elif res == 2:
                upscaleVideo(path, "2560:1440")
        case "r":
            return

    ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
    input("Work done.")

if __name__ == '__main__':
    while True:
        main()
