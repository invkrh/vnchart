function last(n, unit) {
    if (unit == 'hour') {
        return moment().tz("America/Los_Angeles").minute(0).second(0).add(-n, 'h');
    }

    if (unit == 'day') {
        return moment().tz("America/Los_Angeles").hour(0).minute(0).second(0).add(-n, 'd');
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
        var tooltipFmt = 'ddd MMM DD, HH:00 + [1h]'
    }

    if (chartId == 'daily') {
        var unit = 'day'
        var timeUnitFmt = 'MMM DD'
        var tooltipFmt = 'ddd MMM DD + [1d]'
    }

    datasets = stats['datasets'].map(
        function (dataset, i) {
            // alert(getColor(i))
            return {
                label: dataset['interface'],
                data: dataset['transfer'],
                backgroundColor: getColor(i)
            }
        }
    )

    size = stats['offsets'].length

    var ctx = document.getElementById(chartId);
    var data = {
        /**
         *  xValues are indices start from 0, 1, 2, ...
         *  whose value is used as backoff step,
         *  hence, it means from now to past
         *  while yValues represents the same thing
         * 
         *  When displaying the chart, (x, y) pair will
         *  be arranged by the ascendant order of x 
         *  (starts from the smallest timestamp at origin).
         */
        labels: stats['offsets'].map(function (num) {
            return last(num, unit);
        }),
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
                            if (index === 0) {
                                return dataLabel
                            }
                            // else if (index === points.idx.length) {
                            //     // show the end of the last period
                            //     return dataLabel
                            // } 
                            else if (index % Math.floor(size / 4) === 0) {
                                return dataLabel
                            } else {
                                return null
                            }
                        }
                    },
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}
