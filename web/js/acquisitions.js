


(async function() {
  const config = {
    type: 'bar',
    data: {
      labels: data.map(row => row.year),
      datasets: [
        {
          label: 'Acquisitions by year',
        //   data: data.map(row => row.count)
          data: [0,1,2,3,4,5,6]
        }
      ]
    }
  };

  let chart = new Chart(document.getElementById('acquisitions'), config);
})();
