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
import threading
import queue
import time
import wave
import urllib.request
import pyaudio
import boto3


BASE_PATH = "https://junglesounds.s3-ap-southeast-1.amazonaws.com/raw_audio/"
RECORDS_PATH = "https://junglesounds.s3-ap-southeast-1.amazonaws.com/analysis/records.txt"
CREDS_PATH = "creds.secret"

# variables
chunk = 1024
all_unparsed_files = []
all_parsed_files = []
all_files = []
index = 0
playing = False

print("Thank you for partcipating in this exercise.")
print("Please wait while the data is fetched from the server")

# get aws credentials
with open(CREDS_PATH) as f:
    temp = f.readlines()
    API_KEY, API_SECRET = [lines.strip() for lines in temp]

# start AWS session
session = boto3.Session(
    aws_access_key_id=API_KEY,
    aws_secret_access_key=API_SECRET
)

# reference to s3 and the bucket
s3 = session.resource('s3')
raw_audio = s3.Bucket('junglesounds')

# append all file samples names to the all_files array
# this is super hacky. there must be a better way to do this
for key in raw_audio.objects.all():
    thisFile = key.key.split("/")
    if(len(thisFile) > 1 and thisFile[0] == "raw_audio"):
        if(thisFile[1] != ""):
            all_files.append(thisFile[1])

# get the records file with all parsed files listed
request = urllib.request.Request(RECORDS_PATH)
textrecords = urllib.request.urlopen(request)

# save it as a temporary file
FILE = "~temprecords~.txt"
file = open(FILE, 'wb')
file.write(textrecords.read())
file.close()

# open the temporary file and read in the lines
with open(FILE) as f:
    all_parsed_files = f.readlines()
    all_parsed_files = [lines.strip() for lines in all_parsed_files]

# create an array of all unparsed file names
for i in range(len(all_files)):
    fileInList = False
    for fileName in all_parsed_files:
        if(all_files[i] == fileName.split("-")[0]):
            fileInList = True
    if(fileInList == False):
        all_unparsed_files.append(all_files[i])

# print out the summary
print("You have tagged {} files".format(len(all_parsed_files)))
print("You have {} files left to tag".format(len(all_unparsed_files)))


# Download the current index file from aws as a temporary file and play it
def listenToAudio():
    try:
        global index, playing
        playing = True
        print("Playing Audio Clip : {}".format(all_unparsed_files[index]))

        # get the raw audio data from aws
        request = urllib.request.Request("{}{}".format(
            BASE_PATH, all_unparsed_files[index]))
        wavfile = urllib.request.urlopen(request)

        # save it as a temporary wave file
        fname = "~tempread~.wav"
        file = open(fname, 'wb')
        file.write(wavfile.read())
        file.close()

        # open a wav format music
        f = wave.open(fname, "rb")
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
        # remove the temporary wave file
        os.remove(fname)

        playing = False
    except:
        # catch keyboard interrupt and clean up
        print("You Interrupted")
        os.remove(fname)
        os.remove(FILE)
        sys.exit(0)


# Check user input


def checkInput(inputStr):
    global index, playing
    if playing == False:
        if inputStr == "0" or inputStr == "1" or inputStr == "2":
            if inputStr == "0":
                listenToAudio()
            elif inputStr == "1" or inputStr == "2":
                # write to the temporary records file
                activeFile = open(FILE, "a")
                activeFile.writelines(
                    "{}-{}\n".format(all_unparsed_files[index], inputStr))
                activeFile.close()
                # upload the temporary records file to aws and make it public
                s3.meta.client.upload_file(
                    FILE, 'junglesounds', 'analysis/records.txt', ExtraArgs={'ACL': 'public-read'})

                if(index == len(all_unparsed_files) - 1):
                    print(
                        "Yay! All files have been tagged. Type exit to exit the program.")
                else:
                    index += 1
                    listenToAudio()
        else:
            print("Enter 0 to start the program or play the last clip again")
            print("Enter 1 to rate the clip you just heard worthwhile")
            print("Enter 2 to rate the clip you just heard useless")
            print("Enter exit to leave")
    else:
        print("Please wait for this audio to finish playing")

# Handle Keyboard Inputs


def read_kbd_input(inputQueue):
    print("Enter 0 to start the program or play the last clip again")
    print("Enter 1 to rate the clip you just heard worthwhile")
    print("Enter 2 to rate the clip you just heard useless")
    print("Enter exit to leave")
    while (True):
        input_str = input()
        inputQueue.put(input_str)


# Handle Keyboard Inputs


def main():
    global FILE
    try:
        EXIT_COMMAND = "exit"
        inputQueue = queue.Queue()

        inputThread = threading.Thread(
            target=read_kbd_input, args=(inputQueue,), daemon=True)
        inputThread.start()

        while (True):
            if (inputQueue.qsize() > 0):
                input_str = inputQueue.get()
                if (input_str == EXIT_COMMAND):
                    os.remove(FILE)
                    print("Exiting serial terminal.")
                    break
                checkInput(input_str)
            time.sleep(0.01)
        print("End.")
    except KeyboardInterrupt:
        print("You Interrupted")
        os.remove(FILE)
        sys.exit(0)


if (__name__ == '__main__'):
    main()
