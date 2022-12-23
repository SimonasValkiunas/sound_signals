//Extend Chart.js
var originalLineDraw = Chart.controllers.line.prototype.draw;
Chart.helpers.extend(Chart.controllers.line.prototype, {
  draw: function() {
    originalLineDraw.apply(this, arguments);

    var chart = this.chart;
    var ctx = chart.chart.ctx;

    var index = chart.config.data.lineAtIndex;
    if (index) {
      var xaxis = chart.scales['x-axis-0'];
      var yaxis = chart.scales['y-axis-0'];

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(xaxis.getPixelForValue(undefined, index), yaxis.top);
      ctx.strokeStyle = '#ff0000';
      ctx.lineTo(xaxis.getPixelForValue(undefined, index), yaxis.bottom);
      ctx.stroke();
      ctx.restore();
    }
  }
});

var chart = null;
var chart2 = null;
var mode = 0;

eel.expose(init_chart);
function init_chart(data){
  console.log(data)
  let chartData = JSON.parse(data);
  mode = chartData.mode
  if(mode == 1){
    document.getElementById('chart')
    .innerHTML += `<div>
                  <canvas id="chart1"></canvas>
                  </div>`;
    const config = {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Sound wave',
            data: chartData.data,
            borderColor: "#084de0"
          }
        ],
        lineAtIndex: chartData.marker
      },
      options: {
        elements: {
            point:{
                radius: 0
            }
        }
    }
    };
    let chart_el = document.getElementById("chart1");
    chart = new Chart(chart_el, config);  
  } else if(mode == 2){
    document.getElementById('chart')
    .innerHTML += `<div>
                  <canvas id="chart1"></canvas>
                  </div>
                  <div>
                  <canvas id="chart2"></canvas>
                  </div>`;
    const config = {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Sound wave - L channel',
            data: chartData.data.l_channel,
            borderColor: "#084de0"
          }
        ],
        lineAtIndex: chartData.marker
      },
      options: {
        elements: {
            point:{
                radius: 0
            }
        }
      }
    };

    const config2 = {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Sound wave - R channel',
            data: chartData.data.r_channel,
            borderColor: "#084de0"
          }
        ],
        lineAtIndex: chartData.marker
      },
      options: {
        elements: {
            point:{
                radius: 0
            }
        }
      }
    };
    let chart_el = document.getElementById("chart1");
    let chart_el2 = document.getElementById("chart2");
    chart = new Chart(chart_el, config);
    chart2 = new Chart(chart_el2, config2);  
  }
}

eel.expose(chart_update)
function chart_update(chartLabels, chartData){
  chart.data.datasets[0].data = chartData;
  chart.data.labels = chartLabels;
  console.log("Updating chart")
  console.log(chart)
  chart.update();
}

eel.expose(create_slider)
function create_slider(min,max){
  let slider = `<div class="slidecontainer">
                  <input type="range" min="${min}" max="${max}" value=0 class="slider" id="myRange">
                </div>`

  document.getElementById('slider-placeholder').innerHTML += slider;
  document.getElementById('slider-placeholder').onchange = function(e){
    
    if(mode == 1){
      chart.data.lineAtIndex = e.target.value;
      chart.update();
    }else if(mode == 2){
      chart.data.lineAtIndex = e.target.value;
      chart.update();
      chart2.data.lineAtIndex = e.target.value;
      chart2.update();
    }

  }
}













