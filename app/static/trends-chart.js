function showTrends(chartId, titleText, data) {
    var ctx = document.getElementById(chartId);
    var data = {
        labels: data.xValues,
        datasets: [
            {
                label: "Traffic in MB",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: data.yValues,
                spanGaps: false,
            }
        ]
    };
    var scatterChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: titleText
            }
        }
    });
}
