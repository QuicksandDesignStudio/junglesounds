"""
This is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

Copyright (c) 2020 Romit Raj
Copyright (c) 2020 Thejesh GN 
"""

import sys
import os
import pyaudio
import wave
import time
import threading
import queue

PATH = "../recorder-app/audio/audio"
FILE = "records.txt"
chunk = 1024
all_files = os.listdir(PATH)
all_unparsed_files = []
all_parsed_files = []
index = 0
playing = False

with open(FILE) as f:
    all_parsed_files = f.readlines()
    all_parsed_files = [lines.strip() for lines in all_parsed_files]


for i in range(len(all_files)):
    fileInList = False
    for fileName in all_parsed_files:
        if(all_files[i] == fileName.split("-")[0]):
            fileInList = True
            print("Found in list : {}".format(all_files[i]))
    if(fileInList == False):
        all_unparsed_files.append(all_files[i])


def listenToAudio():
    global index, playing
    playing = True
    print("Playing Audio Clip : {}".format(all_unparsed_files[index]))
    # open a wav format music
    f = wave.open(r"{}/{}".format(PATH, all_unparsed_files[index]), "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
    playing = False


def checkInput(inputStr):
    global index, playing
    if playing == False:
        if inputStr == "0" or inputStr == "1" or inputStr == "2":
            if inputStr == "0":
                listenToAudio()
            elif inputStr == "1" or inputStr == "2":
                activeFile = open(FILE, "a")
                activeFile.writelines(
                    "{}-{}\n".format(all_unparsed_files[index], inputStr))
                activeFile.close()
                if(index == len(all_unparsed_files) - 1):
                    print(
                        "Yay! All files have been tagged. Type exit to exit the program.")
                else:
                    index += 1
                    listenToAudio()
        else:
            print("Enter 0 to start the program or play the current clip again")
            print("Enter 1 to rate previous clip worthwhile")
            print("Enter 2 to rate previous clip useless")
    else:
        print("Please wait for this audio to finish playing")


def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')
    while (True):
        input_str = input()
        inputQueue.put(input_str)


def main():
    EXIT_COMMAND = "exit"
    inputQueue = queue.Queue()

    inputThread = threading.Thread(
        target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    while (True):
        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get()
            if (input_str == EXIT_COMMAND):
                print("Exiting serial terminal.")
                break

            # Insert your code here to do whatever you want with the input_str.
            checkInput(input_str)

        # The rest of your program goes here.

        time.sleep(0.01)
    print("End.")


if (__name__ == '__main__'):
    main()
