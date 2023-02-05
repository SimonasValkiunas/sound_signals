import wave
import tkinter as tk
from matplotlib.figure import Figure
from Wave_obj import wave_obj
from ChartBulder import ChartBuilder
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal
import os

def readFile(path):
    w = wave.open(path, 'rb')
    w_obj = wave_obj(
        nchannels = w.getnchannels(),
        sampwidth = w.getsampwidth(),
        framerate = w.getframerate(),
        nframes = w.getnframes(),
        comptype = w.getcomptype(),
        compname = w.getcompname(),
        frames = w.readframes(-1)
    )
    return w_obj

def calculateSignalEnergy(signal, sample_rate, segment_size = 30, overlap = 0.5):

    sample_size = math.floor(segment_size / 1000 * sample_rate)
    signal_length = len(signal[0])
    num_intervals = int( signal_length / (sample_size * overlap)) - 1

    energy_data = np.array([])
    for c,v in enumerate(signal):
        for i in range(num_intervals):
            start = int(i * sample_size * overlap)
            end = int(start + sample_size)
            interval = np.array(signal[c][start:end]).astype(np.int32) #int16 overflows when squaring
            energy_data = np.append(energy_data,np.mean(np.square(interval))).astype(np.int32) #convert to round 

    energy_data = np.reshape(energy_data, (-1, num_intervals)) # format for stereo

    return [energy_data, np.arange(1, num_intervals + 1, 1)]

def createFigure(window):
    fig = Figure(figsize=(5, 1))
    canvas = FigureCanvasTkAgg(
        fig,
        window
    )
    return fig, canvas


def playsignal(signal,framerate):
    if len(signal) == 2:
        print("Playing stereo")
        stereo = np.column_stack((signal[0], signal[1]))
        sd.play(stereo, framerate, mapping=[1,2])
    else:
        print("Playing mono")
        sd.play(signal[0], framerate)

    sd.wait()

def modulateSignalSin(signal, sampling_rate, fs = 3, amp = 1):
    mod = [(np.cos(2 * np.pi * fs * x/sampling_rate) * amp ) for x in range(len(signal[0]))]
    mod_signal = np.array([c * mod for c in signal], dtype=np.int16)
    return [mod_signal,[mod]]

def multByWindow(signal):
    hanning = np.hanning(len(signal[0]))
    res_signal = np.array([ c * hanning for c in signal ],dtype=np.int16)
    return [res_signal,[hanning]]


def sliceArray(array):
    end = 0
    if len(array[0]) % 2 == 0:
        end = (len(array[0]) // 2)
    else:
        end = ((len(array[0]) + 1) // 2)
    end = int(end)
    sliced = [c[0:end] for c in array]

    return sliced

def amplifyArray(array,org_N):
    result = []
    for c in array:
        if org_N % 2 == 0:
            res = [ v * 2 for i,v in enumerate(c)  if i > 0 or i < len(c)-2 ]
        else:
            res = [ v * 2 for i,v in enumerate(c)  if i > 0 or i < len(c)-1 ]
        result.append(res)
    return np.array(result, dtype=np.int64)

def calculateDFT(signal,fs):
    sig,hanning = multByWindow(signal)
    dft_sig = [ abs(np.fft.fft(c)) for c in sig] 
    sliced = sliceArray(dft_sig)
    amp_dft = amplifyArray(sliced,len(dft_sig))

    f_array = np.fft.fftfreq(len(dft_sig[0]), 1/(fs))
    print(len(f_array))
    f_array = f_array[:len(f_array) //  2]

    print(len(amp_dft[0]))
    print(len(f_array))

    return [amp_dft,f_array]

def closest_value(lst, target):
    return min(range(len(lst)), key=lambda x: abs(lst[x]-target))


def main():

    window = tk.Tk()
    window.geometry("1200x800")

    w_obj, signal_array, time_array, mod_sig, entry1, entry2, fig, canvas  = None, None, None, None, None, None, None, None
    buttonframe = tk.Frame(window)
    
    def Analize():
        global w_obj, signal_array, time_array, entry1, entry2, fig, canvas
        
        w_obj = readFile("./sounds/{}".format(value_inside.get()))
        signal_array = w_obj.getSignalArray()
        time_array = w_obj.getTimeArray()
        
        fig,canvas = createFigure(window)
        chart1 = ChartBuilder(time_array, signal_array, fig, canvas)
        chart1.draw()

        energy,segs = calculateSignalEnergy(signal_array, w_obj._framerate)

        fig2,canvas2 = createFigure(window)
        chart2 = ChartBuilder(segs, energy, fig2, canvas2)
        chart2.draw()

        entry1 = tk.Entry(window)
        entry1.pack()
        entry2 = tk.Entry(window)
        entry2.pack()

    def Modulate():
        global w_obj, signal_array, time_array, mod_sig
        mod_sig, mod = modulateSignalSin(signal_array, w_obj._framerate)

        fig1,canvas1 = createFigure(window)
        chart1 = ChartBuilder(time_array, mod, fig1, canvas1)
        chart1.draw()

        fig2,canvas2 = createFigure(window)
        chart2 = ChartBuilder(time_array, mod_sig, fig2, canvas2)
        chart2.draw()

        energy,segs = calculateSignalEnergy(mod_sig, w_obj._framerate)

        fig3,canvas3 = createFigure(window)
        chart3 = ChartBuilder(segs, energy, fig3, canvas3)
        chart3.draw()

    
    def PlayOriginal():
        global w_obj, signal_array
        playsignal(signal_array, w_obj._framerate)

    def PlayNew():
        global w_obj, mod_sig
        playsignal(mod_sig, w_obj._framerate)

    def GetSegment():
        global w_obj, signal_array, time_array, mod_sig, entry1, entry2, fig, canvas

        v1,v2 = int(entry1.get()) / 1000, int(entry2.get()) / 1000
        start, end = closest_value(time_array.tolist(), v1), closest_value(time_array.tolist(), v2)
        
        for c in fig.axes:
            c.axvline(v1, color = "r")
            c.axvline(v2, color = "r")
        canvas.draw()

        sample_rate = w_obj._framerate

        segment = [c[start:end] for c in signal_array]

        dft_sig,f_array = calculateDFT(segment, sample_rate)

        fig1,canvas1 = createFigure(window)
        chart1 = ChartBuilder(f_array, dft_sig, fig1, canvas1)
        chart1.draw() 

        seg_ms = 25
        seg_size = math.floor(seg_ms / 1000 * sample_rate)
        results = [ scipy.signal.stft(c,window='hann',nperseg=seg_size,noverlap=seg_size // 2) for c in segment]
        
        fig2,canvas2 = createFigure(window)
        chart2 = ChartBuilder(None, results, fig2, canvas2, "bitmap")
        chart2.draw()

        segment_mod = [c[start:end] for c in mod_sig]
        dft_sig_mod,f_array_mod = calculateDFT(segment_mod, sample_rate)

        fig3,canvas3 = createFigure(window)
        chart3 = ChartBuilder(f_array_mod, dft_sig_mod, fig3, canvas3)
        chart3.draw() 

        results_mod = [ scipy.signal.stft(c,window='hann',nperseg=seg_size,noverlap=seg_size // 2) for c in segment_mod]
        fig4,canvas4 = createFigure(window)
        chart4 = ChartBuilder(None, results_mod, fig4, canvas4, "bitmap")
        chart4.draw()

    sounds = os.listdir('sounds')

    value_inside = tk.StringVar(window)
    value_inside.set("Select a sounds")

    question_menu = tk.OptionMenu(window, value_inside, *sounds)
    question_menu.pack()

    
    submit_button = tk.Button(buttonframe, text='Read File', command=Analize).grid(row=0, column=0)
    modulate__button = tk.Button(buttonframe, text='Modulate signal', command=Modulate).grid(row=0, column=1)
    play_org__button = tk.Button(buttonframe, text='Play Original', command=PlayOriginal).grid(row=0, column=2)
    play_new_button = tk.Button(buttonframe, text='Play New', command=PlayNew).grid(row=0, column=3)
    get_segment_button = tk.Button(buttonframe, text='Get Segment', command=GetSegment).grid(row=0, column=4)
    buttonframe.pack()

    window.mainloop()

main()





