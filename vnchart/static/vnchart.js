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


    datasets = stats['datasets'].map(
        function (dataset, i) {
            return {
                label: dataset['label'],
                data: dataset['transfer'],
                backgroundColor: getColor(i)
            }
        }
    )

    var size = stats['labels'].length
    var ctx = document.getElementById(chartId);
    var data = {
        labels: stats['labels'],
        datasets: datasets
    };

    var scatterChart = new Chart(ctx, {
        type: 'bar',
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
                            // if (index % Math.floor(size / 3) === 0) {
                                return dataLabel
                            // } else {
                            //     return null
                            // }
                        }
                    },
                    categoryPercentage: 0.8,
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}
