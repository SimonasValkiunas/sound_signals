class wave_obj:
    def __init__(self, nchannels, sampwidth, framerate, nframes, comptype, compname, frames = []):
        self._nchannels = nchannels
        self._sampwidth = sampwidth
        self._framerate = framerate
        self._nframes = nframes
        self._comptype = comptype
        self._compname = compname
        self._frames = frames
    