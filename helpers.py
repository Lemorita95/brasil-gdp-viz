import csv
import datetime
import pytz
import requests
import urllib
import uuid
import numpy as np

from flask import request, render_template

def money(value):
    """ format value with 2 decimal points and thousands separator """
    return f"{value:,.2f}"

def percentage(value):
    """ format value with 2 decimal points and thousands separator """
    return f"{value:.2%}"

def brl_dolar(symbol = 'BRLUSD=X'):
    """ Look up quote for symbol. """
    """  default use is to get brl-usd exchange rate """

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        price = round(float(quotes[-1]["Adj Close"]), 6)
        return {"price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None


def include_header(cur):
    """ 
    function to include column names AFTER cursor.execute 
    RETURN value as a LIST OF DICTS in 
    {column_name1: data1, column_name2:data2, ...} format,
    for each row
    """

    # get data rows from cursor execute
    data = cur.fetchall()

    # get corresponding column for each row
    headers = [description[0] for description in cur.description]

    # initialize empty list that will be returned
    result = []

    # loop though each row returned from EXECUTE SELECT
    for d in data:
        # create a new dict for each row
        x = {}

        # loop through each column
        for n in range(len(headers)):
            # add key: value pair for each row
            x.update({headers[n]: d[n]})
            
        # add dict row at resulting list
        result.append(x)

    # return list of dicts
    return result

def bad_request(code=400):
    """Render message as an apology to user."""

    return render_template("bad_request.html", code=code)


def get_svg(id_org, org='state'):
    
    if org == 'state':
        url = f"https://servicodados.ibge.gov.br/api/v3/malhas/estados/{id_org}?formato=image/svg+xml&qualidade=maxima"
    elif org == 'city':
        url = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{id_org}?formato=image/svg+xml&qualidade=maxima"
    else:
        return False

    return requests.get(url, verify=False).text
