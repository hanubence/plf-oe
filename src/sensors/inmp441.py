# The MIT License (MIT)
# Copyright (c) 2019 Michael Shi
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:
# - read 32-bit audio samples from the left channel of an I2S microphone
# - snip upper 16-bits from each 32-bit microphone sample
# - write 16-bit samples to a SD card file using WAV format
#
# Recorded WAV file is named:
#   "mic_left_channel_16bits.wav"
#
# Hardware tested:
# - INMP441 microphone module 
# - MSM261S4030H0 microphone module

import os
from machine import Pin, SDCard, I2S

def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    datasize = num_samples * num_channels * bitsPerSample // 8
    o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(
        4, "little"
    )  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", "ascii")  # (4byte) File type
    o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
    o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2, "little")  # (2byte)
    o += (sampleRate).to_bytes(4, "little")  # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
    o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
    o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
    return o

class INMP441:

    SCK_PIN = 13
    WS_PIN = 14
    SD_PIN = 12
    I2S_ID = 0
    BUFFER_LENGTH_IN_BYTES = 40000

    # ======= AUDIO CONFIGURATION =======
    RECORD_TIME_IN_SECONDS = 10
    WAV_SAMPLE_SIZE_IN_BITS = 16
    FORMAT = I2S.MONO
    SAMPLE_RATE_IN_HZ = 10_000
    # ======= AUDIO CONFIGURATION =======

    format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
    NUM_CHANNELS = format_to_channels[FORMAT]
    WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
    RECORDING_SIZE_IN_BYTES = (
        RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
    )

    def record(self, sd, seconds=1, filename='recording.wav'):
        wav = open("/sd/{}".format(filename), "wb")

        self.RECORDING_SIZE_IN_BYTES = (
            seconds * self.SAMPLE_RATE_IN_HZ * self.WAV_SAMPLE_SIZE_IN_BYTES * self.NUM_CHANNELS
        )

        wav_header = create_wav_header(
            self.SAMPLE_RATE_IN_HZ,
            self.WAV_SAMPLE_SIZE_IN_BITS,
            self.NUM_CHANNELS,
            self.SAMPLE_RATE_IN_HZ * self.RECORD_TIME_IN_SECONDS,
        )

        num_bytes_written = wav.write(wav_header)

        audio_in = I2S(
            self.I2S_ID,
            sck=Pin(self.SCK_PIN),
            ws=Pin(self.WS_PIN),
            sd=Pin(self.SD_PIN),
            mode=I2S.RX,
            bits=self.WAV_SAMPLE_SIZE_IN_BITS,
            format=self.FORMAT,
            rate=self.SAMPLE_RATE_IN_HZ,
            ibuf=self.BUFFER_LENGTH_IN_BYTES,
        )

        mic_samples = bytearray(10000)
        mic_samples_mv = memoryview(mic_samples)
        num_sample_bytes_written_to_wav = 0

        print("Recording size: {} bytes".format(self.RECORDING_SIZE_IN_BYTES))
        print("==========  START RECORDING ==========")
        try:
            while num_sample_bytes_written_to_wav < self.RECORDING_SIZE_IN_BYTES:
                # read a block of samples from the I2S microphone
                num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
                if num_bytes_read_from_mic > 0:
                    num_bytes_to_write = min(
                        num_bytes_read_from_mic, self.RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
                    )
                    # write samples to WAV file
                    num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
                    num_sample_bytes_written_to_wav += num_bytes_written

            print("==========  DONE RECORDING ==========")
        except (KeyboardInterrupt, Exception) as e:
            print("caught exception {} {}".format(type(e).__name__, e))

        wav.close()
        os.umount("/sd")
        sd.deinit()

