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
import audioop

FILE_PATH = '/home/pi/audio/'
RECORD_TIME = 10  # seconds to record
SAMPLE_TIME = 0.5  # seconds to sample
FORM_1 = pyaudio.paInt16  # 16-bit resolution
CHANS = 1  # 1 channel
SAMPLE_RATE = 44100  # 44.1kHz sampling rate
CHUNK = 4096  # 2^12 samples for buffer
TRIGGER_INTENSITY = 1000

# the index is 2, the 1st two indices are both HDMI, I am guessing one is video and the other is audio
# this may change if and when we add an external HD
DEV_INDEX = 2  # device index found by p.get_device_info_by_index(ii)

# starting conditions
time_now = time.time()
wav_output_filename = str(FILE_PATH) + str(time_now) + '.wav'

# record audio


def record_audio():
    global time_now
    print("Recording File Named : " + str(time_now) + ".wav")
    sample_into_wav()
    print("Recording Complete")
    time_now = time.time()
    sample_audio()
# sample audio to check for intensity


def sample_audio():
    global time_now, SAMPLE_TIME, wav_output_filename
    intensityHigh = False
    audio = pyaudio.PyAudio()  # create pyaudio instantiation
    stream = audio.open(format=FORM_1, rate=SAMPLE_RATE, channels=CHANS,
                        input_device_index=DEV_INDEX, input=True,
                        frames_per_buffer=CHUNK)

    for i in range(0, int(SAMPLE_RATE / CHUNK * SAMPLE_TIME)):
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)
        if(rms > TRIGGER_INTENSITY):
            intensityHigh = True
    stream.stop_stream()
    stream.close()
    audio.terminate()
    if(intensityHigh):
        time_now = time.time()
        wav_output_filename = str(FILE_PATH) + str(time_now) + '.wav'
        record_audio()
    else:
        print("Waiting for recording to be triggered")
        sample_audio()
# sample from the mic (SPI or I2C)


def sample_into_wav():
    audio = pyaudio.PyAudio()  # create pyaudio instantiation
    stream = audio.open(format=FORM_1, rate=SAMPLE_RATE, channels=CHANS,
                        input_device_index=DEV_INDEX, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    # loop through stream and append audio chunks to frame array
    for ii in range(0, int((SAMPLE_RATE/CHUNK)*RECORD_TIME)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop the stream, close it, and terminate the pyaudio instantiation
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


# start by sampling
sample_audio()
