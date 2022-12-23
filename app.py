import matplotlib.pyplot as plt
import numpy as np
import wave
import sys



nframes = w.getnframes()
print(nframes)

framesBytes = w.readframes(-1)
framesInt = list(framesBytes)

# If Stereo
if w.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

fs = w.getframerate()
Time = np.linspace(0, len(framesInt) / fs, num=len(framesInt))

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time,framesInt)
plt.show()