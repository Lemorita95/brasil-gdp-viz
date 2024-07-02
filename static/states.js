/// to include current selected state data
window.onload = function () {
    const parsedUrl = new URL(window.location.href);

    state = parsedUrl.searchParams.get("stateInput")

    if (state == null) {
        state = 'Minas Gerais'
    } else {

    }

    document.getElementById('user-state').innerHTML = state;

}

// to plot line chart
fetch('/states_data').then(response => response.json()).then(function(estados){
    years = Object.keys(estados['estados'][state]);
    ranks = Object.values(estados['estados'][state]);

    // get data afrom app.py and customize it
    const data = {
        labels: years,
        datasets: [{
            label: 'Rank',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(0, 0, 0)',
            data: ranks,
        }]
    };

    // configuration of chart
    const config = {
        type: 'line',
        data: data,
        plugins: [ChartDataLabels],
        options: { 
            maintainAspectRatio: false, 
            normalized: true,
            scales: {
                x: {
                    display: true,
                    ticks: {
                        stepSize: 2,
                    }
                },
                y: {
                    min: 0,
                    max: 28,
                    display: true,
                    reverse: true,
                    ticks: {
                        stepSize: 1,
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    position: 'top',
                    text: 'Rank in Brazil by Value of GDP',
                    color: 'rgb(0, 0, 0)',
                    font: {
                        size: 14
                    },
                    padding: {
                        bottom: 20,
                    },
                },
                subtitle: {
                    display: false,
                    text: 'equivalence at current BRL-USD exchange rate',
                    font: {
                        style: 'italic'
                    }
                },
                datalabels: {
                    color: 'black',
                    align: 'top',
                }
            }
        }
    };

    // get chart element
    var context = document.getElementById('states-chart').getContext('2d');

    // create instance
    new Chart(
        context,
        config
    );

});