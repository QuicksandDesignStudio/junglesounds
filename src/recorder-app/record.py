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

Copyright (c) 2018 Joshua Hrisko
Copyright (c) 2020 Romit Raj
Copyright (c) 2020 Thejesh GN 
"""

import sys
import os
import pyaudio
import wave
import time

MAX_RECORD_TIME = 8  # in hours
FILE_PATH = '/home/pi/audio/'
RECORD_TIME = 5  # seconds to record
WAIT_TIME = 1  # seconds to wait in between recordings
FORM_1 = pyaudio.paInt16  # 16-bit resolution
CHANS = 1  # 1 channel
SAMPLE_RATE = 44100  # 44.1kHz sampling rate
CHUNK = 4096  # 2^12 samples for buffer

# the index is 2, the 1st two indices are both HDMI, I am guessing one is video and the other is audio
# this may change if and when we add an external HD
DEV_INDEX = 2  # device index found by p.get_device_info_by_index(ii)

# starting conditions
time_now = time.time()
wav_output_filename = str(FILE_PATH) + str(time_now) + '.wav'


def sample_into_wav(wav_output_filename):
    audio = pyaudio.PyAudio()  # create pyaudio instantiation
    stream = audio.open(format=FORM_1, rate=SAMPLE_RATE, channels=CHANS,
                        input_device_index=DEV_INDEX, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    # loop through stream and append audio chunks to frame array
    for ii in range(0, int((SAMPLE_RATE/CHUNK)*RECORD_TIME)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    # stop the stream, close it, and terminate the pyaudio instance
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename, 'wb')
    wavefile.setnchannels(CHANS)
    wavefile.setsampwidth(audio.get_sample_size(FORM_1))
    wavefile.setframerate(SAMPLE_RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()


def wait_to_record():
    global time_now, WAIT_TIME, wav_output_filename
    print("Waiting to record again for : " + str(WAIT_TIME) + " seconds")
    while(True):
        loop_duration = time.time() - time_now
        if(loop_duration > WAIT_TIME):
            break
    print("Finished waiting for record")


def iterative_record():
    for i in range(int((60 / (RECORD_TIME + WAIT_TIME)) * 60 * MAX_RECORD_TIME)):
        time_now = time.time()
        print("Recording File Named : " + str(time_now) + ".wav")
        wav_output_filename = str(FILE_PATH) + str(time_now) + '.wav'
        sample_into_wav(wav_output_filename)
        wait_to_record()


# start recording
iterative_record()
