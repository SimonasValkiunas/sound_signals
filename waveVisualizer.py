import wave
import sys
import numpy as np
import math
from wave_obj import wave_obj

class waveVisualizer:

    def __init__(self, fname,scale = 0):
        self._file_name = fname
        self._data = []
        self._labels = []
        self._MODE_RB = "rb"
        self._SOUNDS_PATH = "./Sounds/"
        self._TONES_PATH = "./Tones/"
        self._scale = scale

    #read signal data
    def readFile(self):
        w = wave.open(self._SOUNDS_PATH + self._file_name, self._MODE_RB)

        w_obj = wave_obj(
            nchannels = w.getnchannels(),
            sampwidth = w.getsampwidth(),
            framerate = w.getframerate(),
            nframes = w.getnframes(),
            comptype = w.getcomptype(),
            compname = w.getcompname(),
            frames = w.readframes(-1)
        )

        self._wave = w_obj

    #init a chart
    def createChart(self):
        self.readFile()
        
        
        sample_freq = self._wave._framerate
        n_samples = self._wave._nframes

        n_channels = self._wave._nchannels

        signal_wave = self._wave._frames
        signal_array = np.frombuffer(signal_wave, dtype=np.int16).tolist()

        if self._scale > 1:
            times = np.linspace(0, n_samples/sample_freq, num=self._scale*2).tolist()
        else:
            times = np.linspace(0, n_samples/sample_freq, num=n_samples).tolist()
        
        if n_channels == 2:
            if self._scale > 1:
                l_channel = self.calculateRMS(self._scale,n_samples,signal_array[0::2])
                r_channel = self.calculateRMS(self._scale,n_samples,signal_array[1::2])
            else:
                l_channel = signal_array[0::2]
                r_channel = signal_array[1::2]

            chart = {"labels": times,
                "data": {
                    "l_channel": l_channel,
                    "r_channel": r_channel,
                },
                "mode": n_channels
            }
        else:
            if self._scale > 1:
                signal = self.calculateRMS(self._scale,n_samples,signal_array)
            else:
                signal = signal_array
                
            chart = {"labels": times,
                    "data": signal,
                    "mode": n_channels
                    }
                
        return chart
    
    def calculateRMS(self,p_width,t_samples,signal):
        signal_rms = np.array([])
        s = math.floor(t_samples/p_width)
        for i in range(0, p_width):
            rms = np.array([])
            for j in range(0, s):
                value = signal[i*s+j]
                rms = np.append(rms, value)
            squared_samples = rms**2
            mean_squared = np.mean(squared_samples)
            signal_rms = np.append(signal_rms,math.floor(np.sqrt(mean_squared)))
        signal_rms_repeat = np.repeat(signal_rms,2)
        signal_formated = [v if i%2 else -v for i,v in enumerate(signal_rms_repeat)]
        return signal_formated

    def getScale(self):
        if self._scale > 1:
            return self._scale
        else: 
            return self._wave._nframes
        pass

    def getEnergyChart(self,sample_time):

        # ,nframes = 12,signal_time = 12,sample_time = 2,signal = [0,1,2,3,4,5,6,7,8,9,10,11]
        signal_time = self._wave._nframes/self._wave._framerate
        n_samples = math.floor(signal_time/sample_time)
        sample_width = math.floor(self._wave._nframes/n_samples)

        signal_wave = self._wave._frames
        signal_array = np.frombuffer(signal_wave, dtype=np.int16).tolist()
        
        energy_data = np.array([])
        energy_time = np.array([])
        for i in range(0,math.floor(self._wave._nframes/sample_width)):
            samples = np.array(signal_array[(sample_width * i):(sample_width * (i+1))])
            sample_energy = np.mean(samples**2)/sample_width
            energy_data = np.append(energy_data,math.floor(sample_energy))
            energy_time = np.append(energy_time, round(sample_time*(i+1),5))

        chart = {
                "labels": energy_time.tolist(),
                "data": energy_data.tolist(),
                "mode": 1
                }
        return chart




