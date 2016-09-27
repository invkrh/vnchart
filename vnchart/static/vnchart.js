var colors = [
    'rgba(154, 18, 179, 1)',
    'rgba(46, 204, 113 ,1)',
    'rgba(242, 38, 19, 1)',
    'rgba(65, 131, 215, 1)'
]

function getColor(i) {
    return colors[i % colors.length];
}

function showTrends(chartId, titleText, stats) {

    if (chartId == 'hourly') {
        var unit = 'hour'
        var timeUnitFmt = 'HH:00'
        var tooltipFmt = 'ddd MMM DD, HH:00'
    }

    if (chartId == 'daily') {
        var unit = 'day'
        var timeUnitFmt = 'MMM DD'
        var tooltipFmt = 'ddd MMM DD'
    }


    datasets = stats.map(
        function (dataset, i) {
            return {
                label: dataset['label'],
                data: dataset['transfer'].map(
                    function (point) {
                        return {
                            x: moment.parseZone(point[0]),
                            y: point[1],
                        }
                    }
                ),
                backgroundColor: getColor(i)
            }
        }
    )

    var ctx = document.getElementById(chartId);
    var data = {
        datasets: datasets
    };

    var scatterChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            title: {
                display: true,
                text: titleText,
                fontSize: 20
            },
            tooltips: {
                mode: 'x-axis',
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        tooltipFormat: tooltipFmt,
                        displayFormats: {
                            [unit]: timeUnitFmt
                        },
                        unit: unit
                    },

                    ticks: {
                        callback: function (dataLabel, index) {
                            return dataLabel
                            // if (index === 0) {
                            //     return dataLabel
                            // }
                            // else if (index === points.idx.length) {
                            //     // show the end of the last period
                            //     return dataLabel
                            // } 
                            // else if (index % Math.floor(stats['max_offset'] / 4) === 0) {
                            //     return dataLabel
                            // } else {
                            //     return null
                            // }
                        }
                    }
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}
