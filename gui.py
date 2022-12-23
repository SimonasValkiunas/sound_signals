import eel
from waveVisualizer import waveVisualizer
import json

#control scale of graph
scale = 0

w = waveVisualizer("applause.wav",scale)

chart = w.createChart()
e_chart = w.getEnergyChart(0.01)

data = json.dumps(chart)
e_data = json.dumps(e_chart)

min, max = [0, w.getScale()]

eel.init('web')

# eel.init_chart(data)
eel.init_chart(e_data)
eel.create_slider(min, max)

eel.start('index.html')




