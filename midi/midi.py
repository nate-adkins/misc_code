# PRESSED = 0x9f
# RELEASED = 0x8f


# def parse_id_to_key(id):

#     keys = {
#         0 : 'c',
#         1 : 'c#',
#         2 : 'c#',

#     }

# # Open the MIDI device file
# midi_device = open('/dev/midi', 'rb')

# while True:

#     new_data = list(midi_device.read(3))
#     hex_list = [f'0x{byte:02x}' for byte in new_data]

#     # time.sleep(1)
#     print(new_data, hex_list)
#     print('\n')

import sounddevice as sd
import numpy as np

# Parameters for the sine wave
sample_rate = 44100  # Samples per second
duration = 2  # Duration in seconds
frequency = 453  # Frequency of the sine wave (A4)

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)  # Sine wave normalized to [-0.5, 0.5]

# Play audio using sounddevice
sd.play(audio_data, samplerate=sample_rate)
sd.wait()  # Wait until the sound has finished playing
