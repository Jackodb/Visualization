function showChart() {
  console.log('showChart loaded');
  window.pywebview.api.getData().then(
    function(result) {
      drawChart(result.price,result.mountain,result.current,result.title);
    });
}

// function init() {
//   if (!window.pywebview) {
//     console.log('recheck');
//     return init();
//   }
//
//   showChart();
// }
//
// init();

function drawChart(x, y, z, w) {
    var ctx = document.getElementById("myChart");
    ctx.style.backgroundColor = 'rgb(21,43,42)';
    var barBackgroundColors1 = []; // initial
    var barBackgroundColors2 = []; // profit
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: x,
        datasets: [
          {
            label: 'Profit',
            data: z,
            backgroundColor: barBackgroundColors2 //"rgba(51, 204, 51, 0.9)"
          },
          {
            label: 'Initial',
            data: y,
            backgroundColor: barBackgroundColors1 //"rgba(58, 98, 87, 0.5)"
          }
        ]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
            xAxes: [{
                gridLines: {
                  display: false
                },
                stacked: true,
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: w,
                    fontSize: 16,
                    fontColor: 'white'
                },
                ticks: {
                  fontColor: 'white'
                }
            }],
            yAxes: [{
                gridLines: {
                  color: 'rgba(153,153,153,0.2)'
                },
                stacked: true,
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: "Order size",
                    fontSize: 16,
                    fontColor: 'white'
                },
                ticks: {
                  fontColor: 'white'
                }
            }]
         },
        tooltips: {
            displayColors: false,
            callbacks: {
                title: function(tooltipItem) {
                  return `${w}: ${String(tooltipItem[0].xLabel)}`; // ESS syntax
                },
                label: function(tooltipItemY) {
                    return "Total: " + `${Number(tooltipItemY.yLabel)}`;
                }
            }
          }
        }
    })

    for (i = 0; i < x.length; i++) {
        if (x[i] > 1) {
            barBackgroundColors1.push('rgb(230, 0, 0, 0.5)');
            barBackgroundColors2.push('rgb(255, 0, 0, 0.9)');
        }

        else {
          if (x[i] == 1) {
            barBackgroundColors1.push('rgb(217, 217, 217, 0.5)');
            barBackgroundColors2.push('rgb(242, 242, 242, 0.9)');
          }
          else {
            barBackgroundColors1.push('rgba(58, 98, 87, 0.5)');
            barBackgroundColors2.push('rgba(51, 204, 51, 0.9)');
          }
        }
    }

    myChart.update();
};
