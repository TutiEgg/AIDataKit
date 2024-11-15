import pyaudio
import wave

### configurations ###
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

# print some device infos
default_audio_device_infos = p.get_default_input_device_info()
print("Default Audio Device:  ", default_audio_device_infos['name'])
print("maxInputChannels:      ", default_audio_device_infos['maxInputChannels'])
print("defaultSampleRate:     ", default_audio_device_infos['defaultSampleRate'])

# configuration of the data stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* start recording for", RECORD_SECONDS, 'seconds')
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()