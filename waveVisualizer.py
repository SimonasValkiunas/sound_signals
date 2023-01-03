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

    def getSignal(self):
        signal_array = np.frombuffer(self._wave._frames, dtype=np.int16).tolist()
        sample_freq = self._wave._framerate
        n_samples = self._wave._nframes
        
        if self._wave._nchannels == 1:
            signal = [{
                "name": "Mono",
                 "data": signal_array,
                 "time": np.linspace(0, n_samples/sample_freq, num=n_samples).tolist()
                }]
            return signal
        else:
            signal = [{
                "name": "Left channel",
                 "data": signal_array[0::2],
                 "time": np.linspace(0, n_samples/sample_freq, num=n_samples).tolist()
            },
            {
                "name": "Right channel",
                 "data": signal_array[1::2],
                 "time": np.linspace(0, n_samples/sample_freq, num=n_samples).tolist()
            }
            ]
            return signal


    def scaleSignal(self,signal,scale):
        signal_scaled = []

        sample_freq = self._wave._framerate
        n_samples = self._wave._nframes
        
        for s in signal:
            s['data'] = self.calculateRMS(scale,n_samples,s['data'])
            s['time'] = np.linspace(0, n_samples/sample_freq, num=scale*2).tolist()
            signal_scaled.append(s)
        
        return signal_scaled

    # refactor later
    def formatChart(self,signal):
        n_channels = self._wave._nchannels

        chart = {
            "labels": signal[0]['time'],
            "mode": n_channels,
        }

        if n_channels > 1:
            chart['data'] = {
                "l_channel": signal[0]['data'],
                "r_channel": signal[1]['data']
            }
        else:
            chart['data'] = signal[0]['data']
        
        return chart

    #init a chart
    def createChart(self):
        self.readFile()

        signal = self.getSignal()

        if self._scale > 0:
            signal = self.scaleSignal(signal, self._scale)

        chart = self.formatChart(signal)      
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


    def getEnergyChart(self,sample_time, signal, nframes, signal_time):

        # signal = [0,1,0,1,0,1,0,1,0,1,0,1]
        # nframes = len(signal)
        # signal_time = 12 # some arbitraty value 

        nsamples = math.floor(signal_time / sample_time)
        N = math.floor(nframes / nsamples)

        t = np.array(range(0,nsamples*2))

        energy_data = np.array([])

        for i in range(0,nsamples*2-1):
            
            shift = math.floor(N*i/2)
            
            sample = np.array(signal[(N*i - shift):(N*(i+1) - shift)])
            sample_energy = np.mean(sample**2)

            energy_data = np.append(energy_data,sample_energy)
        

        chart = {
                "labels": t.tolist(),
                "data": energy_data.tolist(),
                "mode": 1
                }
        
        return chart

        # signal_time = self._wave._nframes/self._wave._framerate
        # n_samples = math.floor(signal_time/sample_time)
        # sample_width = math.floor(self._wave._nframes/n_samples)

        # #--- fix for stereo ---#
        # signal_wave = self._wave._frames
        # signal_array = np.frombuffer(signal_wave, dtype=np.int16).tolist()
        # #---------------------------------------------------------------#


        # energy_data = np.array([])
        # energy_time = np.array([])

        # # remove time labels
        # for i in range(0,math.floor(((self._wave._nframes/sample_width)*2)-1)):
        #     # make intervals overlap:
        #     shift = math.floor(sample_width*i/2)
        #     shift_time = math.floor(sample_time*i/2)
        #     samples = np.array(signal_array[(sample_width * i - shift):(sample_width * (i+1) - shift)])
        #     sample_energy = np.mean(samples**2)
        #     energy_data = np.append(energy_data,math.floor(sample_energy))
        #     energy_time = np.append(energy_time, round(sample_time*(i+1) - shift_time,5))

        # chart = {
        #         "labels": energy_time.tolist(),
        #         "data": energy_data.tolist(),
        #         "mode": 1
        #         }
        # return chart
    
    # def getNKSChart(self,sample_time):
    #     signal_time = self._wave._nframes/self._wave._framerate
    #     n_samples = math.floor(signal_time/sample_time)
    #     sample_width = math.floor(self._wave._nframes/n_samples)

    #     #--- fix for stereo ---#
    #     signal_wave = self._wave._frames
    #     signal_array = np.frombuffer(signal_wave, dtype=np.int16).tolist()
    #     #---------------------------------------------------------------#

    #     nks_data = np.array([])
    #     nks_time = np.array([])

    #     for i in range(0,math.floor(((self._wave._nframes/sample_width)*2)-1)):
    #         # make intervals overlap:
    #         shift = math.floor(sample_width*i/2)
    #         shift_time = math.floor(sample_time*i/2)
    #         nks = np.array([])    
    #         for j in range((sample_width*i-shift)+1, (sample_width*(i+1) - shift)):
    #             np.append(nks,self.s(signal_array[j]) - self.s(signal_array[j-1]))1
    #         np.append(nks_data,np.mean(nks)/2)
    #         np.append(nks_time, round(sample_time*(i+1) - shift_time,5))

    def s(self,x):
        if x >= 0:
            return 1
        else:
            return -1





