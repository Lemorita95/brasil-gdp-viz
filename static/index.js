// fetch data to plot graph
fetch('/country_data').then(response => response.json()).then(function(grafico){
    labels = grafico['labels'];
    values = grafico['data'];
    values_usd = grafico['data_usd'];


    // get data afrom app.py and customize it
    const data = {
        labels: labels,
        datasets: [{
            label: 'Value (TBRL)',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(0, 0, 0)',
            data: values,
        }]
    };

    // configuration of chart
    const config = {
        type: 'bar',
        data: data,
        options: { 
            maintainAspectRatio: false, 
            normalized: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'in Trillion BRL',
                    color: 'rgb(0, 0, 0)',
                    font: {
                        size: 14
                    }
                },
                subtitle: {
                    display: false,
                    text: 'equivalence at current BRL-USD exchange rate',
                    font: {
                        style: 'italic'
                    }
                }
            }
        }
    };

    // get chart element
    var context = document.getElementById('country-chart').getContext('2d');

    // create instance
    const myChart = new Chart(
        context,
        config
    );

    // style and change data from graph when asked to display in BRL
    document.getElementById("country-change-brl").addEventListener("click", function() {
        myChart.data.datasets[0].backgroundColor = 'rgb(13, 110, 253)';
        myChart.data.datasets[0].label = "Value (TBRL)";
        myChart.data.datasets[0].data = values;
        myChart.options.plugins.title.text = 'in Trillion BRL';
        myChart.options.plugins.subtitle.display = false;
        myChart.update();
    });

    // style and change data from graph when asked to display in USD
    document.getElementById("country-change-usd").addEventListener("click", function() {
        myChart.data.datasets[0].backgroundColor = 'rgb(25, 135, 84)';
        myChart.data.datasets[0].label = "Value (TUSD)";
        myChart.data.datasets[0].data = values_usd;
        myChart.options.plugins.title.text = 'in Trillion USD';
        myChart.options.plugins.subtitle.display = true;
        myChart.update();
    });

})