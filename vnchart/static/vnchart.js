function last(n, unit) {
    if (unit == 'hour') {
        return moment().utc().minute(0).second(0).add(-n, 'h');
    }

    if (unit == 'day') {
        return moment().utc().hour(0).minute(0).second(0).add(-n, 'd');
    }
}

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
                            x: moment(point[0]),
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

    console.log(datasets[0])

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
                    // stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}
