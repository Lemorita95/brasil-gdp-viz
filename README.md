# BRAZIL GDP

My final project for CS50.

This displays GDP data from IBGE (Brazilian Institute of Geography and Statistics) at a **Country**, **State** and **City** level.

#### Video Demo:  [Youtube](https://youtu.be/RC94eA_uXYc)

## Description

#### **Static Folder**

[index.js](static/index.js)
This file contains the **JavaScript** for *Index Route*. 

It is used to fetch data from "/country_data" app Endpoint and displays it as a bar chart.

It also contains the script to change the currency of values displayed.

[states.js](static/states.js)
This file contains the **JavaScript** for *States Route*. 

It contains the script to change the header and set default value for state displayed.

It is used to fetch data from "/states_data" app Endpoint and displays it as a line chart. 

[cities.js](static/cities.js)
This file contains the **JavaScript** for *Cities Route*.

It fetches data from "/states_data" app Endpoint together with "/cities_data" app Endpoint to both the dependent state-city filter and line charts.

It also contains the script to change the header and set default value for state displayed.

[style.css](static/styles.css)
This file contains the **CSS** for *HTML Tags*.

#### **Templates Folder**
[layout.html](templates/layout.html)
This file contains the **HTML** for *Routes Layout*.

Its *head tag* contains the default meta configuration, Bootstrap link, Page Icon, CSS link and Jinja placeholders to specific style for each route.

Its *body tag* contains the navigation pane, Jinja placeholder for content and footer with external links to data providers and social medias.

[bad_request.html](templates/bad_request.html)
This file contains the **HTML** for *Invalid Input Within Route*.

Extended content for layout.html with a default error message.

[index.html](templates/index.html)
This file contains the **HTML** for *Index Route*.

Extended content for layout.html. It also contains links to Chart.js and JavaScript file.

Its main tag contains buttons to change chart, a header, a canvas for bar chart and a table.

Chart data are gathered from "/country_data" app Endpoint with JavaScript.

Table data are passed from the Route "/" with Jinja and Flask.

[states.html](templates/states.html)
This file contains the **HTML** for *States Route*.

Extended content for layout.html. It also contains links to Chart.js, Chart.js datalabels plugin and JavaScript file.

Its main tag contains a dropdown filter, a header, a canvas for line chart, a SVG image and a table.

Chart data are gathered from "/states_data" app Endpoint with JavaScript.

Table data and SVG data are passed from the Route "/states" with Jinja and Flask.

[cities.html](templates/cities.html)
This file contains the **HTML** for *Cities Route*.

Extended content for layout.html. It also contains links to Chart.js and JavaScript file.

Its main tag contains two dropdown filters, a header and two canvas for line chart.

State filter data are gathered from "/states_data" app Endpoint with JavaScript.

City filter data and Chart data are gathered from "/cities_data" app Endpoint with JavaScript.

#### **[app.py](app.py)**
This file contains the **Python** Script for the *Application*.

It uses Flask Framework.

The file contains some third party libraries and some functions defined at helpers.py. It is also defined Custom Jinja filters based on functions at helpers.py.

before_request and after_request decorators are used to handle the open and close action for Database connection by the moment when a request is made.

"/" Route queries information at ibge.db to display at html page through Jinja.

"/states" Route questies information at ibge.db to display at html page through Jinja. An server-side input validation is made. SVG image are displayed at html page through Jinja.

"/cities" Route does an server-side input validation. All information displayed on page are made with [cities.js](static/cities.js).

'/states_data' and '/cities_data' Endpoints query information at ibge.db to be fetched by JavaScript.

#### **[cli.txt](cli.txt)**
This file contains the Commmand-Line-Interface codes used to create SQL Schemas and to run Application.

#### **[helpers.py](helpers.py)**
This file contains user-defined functions to be used at app.py.

money() and percentage() are formatting functions.

brl_dolar() looks for BRL-USD exchange rates at Yahoo Finance API.

include_headers() eases to use of queried information from SQLite in Jinja by arranging the information in a LIST of DICTS.

bad_request() renders the template for invalid user input within routes.

get_svg() looks for SVG image at IBGE API.

#### [ibge.db](ibge.db)
This file contains the Database from IBGE API data.

#### [queries.sql](queries.sql)
This file contains the SQL Queries used at app.py.

#### [requirements.txt](requirements.txt)
This file contains the Python Libraries used at app.py and helpers.py.