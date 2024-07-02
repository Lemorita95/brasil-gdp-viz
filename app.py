from flask import Flask, render_template, request, session, g
from flask_session import Session

import sqlite3

from helpers import money, percentage, brl_dolar, include_header, bad_request, get_svg


# Configure application
app = Flask(__name__)


# Custom filters
app.jinja_env.filters["money"] = money
app.jinja_env.filters["percentage"] = percentage


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# to open the connection with database after any request
# save at a global variable g to use in any route
@app.before_request
def before_request():
    # create connection with databse
    con = sqlite3.connect('ibge.db')
    g.db = con


# to close connection after request and not leave connection open
@app.after_request
def after_request(response):
    if g.db is not None:
        g.db.close()
    return response


@app.route("/")
def index():

    # create database cursor
    cur = g.db.cursor()

    # query
    query = "WITH q AS (WITH cte AS (SELECT g.year, (SUM(g.valor)/ 1e12) as valor FROM gdp as g GROUP BY g.year ORDER BY g.year ASC) SELECT LAG(cte.year, 1, 0) OVER (ORDER BY cte.year) || ' -> ' || cte.year AS years, LAG(cte.year, 1, 0) OVER (ORDER BY cte.year) AS LAG_year, (cte.valor / (LAG(cte.valor, 1, 0) OVER (ORDER BY cte.year))) - 1 AS gain FROM cte ) SELECT q.years, q.gain FROM q WHERE q.LAG_year != 0;"

    # query for result
    cur.execute(query)

    # function defined at helpers.py to FETCHALL and INCLUDE COLUMN names
    gain = include_header(cur)

    return render_template("index.html", gain=gain)


@app.route("/states", methods=["GET"])
def states():

    # create database cursor
    cur = g.db.cursor()

    # query for result and store in variable
    query_states = "SELECT id, name FROM states ORDER BY name ASC"
    cur.execute(query_states)
    states = include_header(cur)

    # query for result and store in variable
    query_gdp = "with q as (SELECT s.id AS state_id, s.shortname AS state_short, s.name AS state_name, g.year, SUM(g.valor) AS valor FROM gdp AS g LEFT JOIN cities AS c on g.cities_id = c.id LEFT JOIN states AS s on c.states_id = s.id GROUP BY s.id, s.shortname, s.name, g.year ORDER BY s.id ASC, g.year ASC) SELECT q.state_id, q.state_name, q.year, q.valor, (q.valor / SUM(q.valor) OVER (PARTITION BY q.year)) AS year_share FROM q"
    cur.execute(query_gdp)
    gdp = include_header(cur)
    
    # retrieve user input
    user_state = request.args.get("stateInput")

    # set default value
    if not user_state:
        user_state_id = '31'
        user_state = [x['name'] for x in states if x['id'] == user_state_id][0]

    # consider user input and validate
    try:
        user_state_id = [x['id'] for x in states if x['name'] == user_state][0]
    except IndexError:
        return bad_request(code=404)

    #filter gdp_share by current state selection
    gdp = [x for x in gdp if x['state_id'] == user_state_id]

    svg = get_svg(user_state_id, org = 'state')

    return render_template("states.html", states=states, gdp=gdp, svg=svg)


@app.route("/cities", methods=["GET"])
def cities():

    """ alterar procura por nome por procura por ID boa vista dando problema """

    # create database cursor
    cur = g.db.cursor()

    # query for result and store in variable
    query_states = "SELECT c.id, c.name FROM cities c ORDER BY c.name ASC;"
    cur.execute(query_states)
    cities = include_header(cur)

        # retrieve user input
    user_city = request.args.get("citiesInput")

    # set default value
    if not user_city:
        user_city_id = '3169307'
        user_city = [x['name'] for x in cities if x['id'] == user_city_id][0]

    # consider user input and validate
    try:
        user_city_id = [x['id'] for x in cities if x['name'] == user_city][0]
    except IndexError:
        return bad_request(code=404)

    return render_template("cities.html")


# ENDPOINT to get data to display country chart
@app.route('/country_data')
def country_data():
    # create database cursor
    cur = g.db.cursor()

    # query
    query = "SELECT g.year, (SUM(g.valor)/ 1e12) as valor FROM gdp as g GROUP BY g.year ORDER BY g.year ASC"

    # query for result
    cur.execute(query)

    # function defined at helpers.py to FETCHALL and INCLUDE COLUMN names
    country = include_header(cur)

    # get labels, data from GDP to plot and arrange as JSON
    result = {
        'labels': [x['year'] for x in country],
        'data': [x['valor'] for x in country],
        'data_usd': [brl_dolar()['price'] * x['valor'] for x in country]
    }

    return result


# ENDPOINT to get data from states
@app.route('/states_data')
def states_data():
    # create database cursor
    cur = g.db.cursor()

    # query
    query = "with q as (SELECT s.id AS state_id, s.shortname AS state_short, s.name AS state_name, g.year, SUM(g.valor) AS valor FROM gdp AS g LEFT JOIN cities AS c on g.cities_id = c.id LEFT JOIN states AS s on c.states_id = s.id GROUP BY s.id, s.shortname, s.name, g.year ORDER BY s.id ASC, g.year ASC) SELECT q.*, RANK() OVER (PARTITION BY q.year ORDER BY q.valor DESC) AS rank FROM q;"

    # query for result
    cur.execute(query)

    # function defined at helpers.py to FETCHALL and INCLUDE COLUMN names
    states = include_header(cur)

    data = dict()
    # get labels, data from STATES and arrange as JSON
    for y in states:
        try:
            data[y['state_name']].update({y['year']: y['rank']})
        except KeyError:
            data[y['state_name']] = {}
            data[y['state_name']].update({y['year']: y['rank']})

    result = {'estados': data}

    return result


# ENDPOINT to get data from cities
@app.route('/cities_data')
def cities_data():
    # create database cursor
    cur = g.db.cursor()

    # query for gdp data and store in a variable
    query_gdp = "SELECT c.id as city_id, c.name as city_name, g.year, g.valor FROM gdp AS g LEFT JOIN cities AS c on g.cities_id = c.id;"
    cur.execute(query_gdp)
    cities = include_header(cur)

    data_gdp = dict()
    # get labels, data from STATES and arrange as JSON
    for y in cities:
        try:
            data_gdp[y['city_name']].update({y['year']: y['valor']})
        except KeyError:
            data_gdp[y['city_name']] = {}
            data_gdp[y['city_name']].update({y['year']: y['valor']})

    # query for gdp data and store in a variable
    query_population = "SELECT p.year, p.valor, c.name AS city_name, c.id FROM population p LEFT JOIN cities c on p.cities_id = c.id ORDER BY p.year ASC;"
    cur.execute(query_population)
    population = include_header(cur)

    data_population = dict()
    # get labels, data from STATES and arrange as JSON
    for y in population:
        try:
            data_population[y['city_name']].update({y['year']: y['valor']})
        except KeyError:
            data_population[y['city_name']] = {}
            data_population[y['city_name']].update({y['year']: y['valor']})


    # query for city-state names
    query_city_state = "SELECT c.id, c.name, s.name AS state_name FROM cities c LEFT JOIN states s ON c.states_id = s.id ORDER BY c.name ASC, s.name ASC;"
    cur.execute(query_city_state)
    cities_state = include_header(cur)

    result = {'gdp': data_gdp, 'population': data_population, 'cities': cities_state}

    return result


if __name__ == '__main__':
    app.run(debug=True)