import numpy as np

class wave_obj:
    def __init__(self, nchannels, sampwidth, framerate, nframes, comptype, compname, frames = []):
        self._nchannels = nchannels
        self._sampwidth = sampwidth
        self._framerate = framerate
        self._nframes = nframes
        self._comptype = comptype
        self._compname = compname
        self._frames = frames
    
    def getSignalArray(self):
        if self._nchannels == 1:
            return [np.frombuffer(
                        self._frames,
                        dtype=np.int16)
                    ]
        else:
            return [
                np.frombuffer(
                    self._frames,
                    dtype=np.int16)[0::2],
                np.frombuffer(
                    self._frames,
                    dtype=np.int16)[1::2]
                ]

    def getTimeArray(self):
        return np.linspace(
            0,
            self._nframes/self._framerate,
            num=self._nframes
        )

    def getDuration(self):
        return self._nframes/self._framerate
