/// states dropdown
fetch('/states_data').then(response => response.json()).then(function(estados){
    STATES = Object.keys(estados['estados']);
    
    let html = '';

    // set default state
    html += `<option disabled selected value="">State</option>`

    for (s of STATES) {
        html += `<option value="${s}">${s}</option>`;
    }

    document.getElementById('citiesStateInput').innerHTML = html;
})

/// to include current selected city data
window.onload = function () {
    const parsedUrl = new URL(window.location.href);

    city = parsedUrl.searchParams.get("citiesInput")

    if (city == null) {
        city = 'Três Corações'
    } else {

    }

    document.getElementById('user-cities').innerHTML = city;
}

// to plot chart
fetch('/cities_data').then(response => response.json()).then(function(cidades){

    // to update cities selection
    function update_cities_input() {
        
        // get current state selection
        let val = document.getElementById('citiesStateInput').value
        
        // cities select
        CITIES = cidades['cities'];
    
        let html = '';
    
        // set default state
        html += `<option disabled selected value="">City</option>`;
    
        for (c of CITIES) {
    
                c_ = c['name']
                c_s = c['state_name']
    
                if (c_s == val) {
                    html += `<option value="${c_}">${c_}</option>`;            
                }
        }
    
        document.getElementById('citiesInput').innerHTML = html;
    }

    // get current context
    var activities = document.getElementById("citiesStateInput");

    // activities.addEventListener("click", function() {
    //     var options = activities.querySelectorAll("option");
    //     var count = options.length;
    //     if(typeof(count) === "undefined" || count < 2)
    //     {
    //         update_cities_input();
    //     }
    // });

    // update cities list when a change occures in the states input
    activities.addEventListener("change", function() {
        update_cities_input();
    });


    // TOP CHART
    rotulos_top = Object.keys(cidades['gdp'][city]);
    valores_top = Object.values(cidades['gdp'][city]);

    // get data afrom app.py and customize it
    const data_top = {
        labels: rotulos_top,
        datasets: [{
            label: 'Value in BRL',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(0, 0, 0)',
            data: valores_top,
        }]
    };

    // configuration of chart
    const config_top = {
        type: 'line',
        data: data_top,
        options: { 
            maintainAspectRatio: false, 
            normalized: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'City GDP',
                    color: 'rgb(0, 0, 0)',
                    font: {
                        size: 14
                    }
                }
            }
        }
    };


    // get chart element
    var context_top = document.getElementById('cities-chart').getContext('2d');

    // create instance
    const myTopChart = new Chart(
        context_top,
        config_top
    );


    // BOTTOM CHART
    rotulos_bot = Object.keys(cidades['population'][city]);
    valores_bot = Object.values(cidades['population'][city]);

    // get data afrom app.py and customize it
    const data_bot = {
        labels: rotulos_bot,
        datasets: [{
            label: 'Population',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(0, 0, 0)',
            data: valores_bot,
        }]
    };

    // configuration of chart
    const config_bot = {
        type: 'line',
        data: data_bot,
        options: { 
            maintainAspectRatio: false, 
            normalized: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'City Census',
                    color: 'rgb(0, 0, 0)',
                    font: {
                        size: 14
                    }
                }
            }
        }
    };


    // get chart element
    var context_bot = document.getElementById('cities-population-chart').getContext('2d');

    // create instance
    const myBotChart = new Chart(
        context_bot,
        config_bot
    );

});