import bottle
import json
import bellman_ford
import httplib
import sys

EPS = sys.float_info.epsilon

# TODO check bottle production, test parallel requests with sleep

# Redis-like persistence
CURRENCY = {}

# GET /currencies
@bottle.get('/currencies')
def currencies():
    bottle.response.content_type = 'application/json'
    return json.dumps(CURRENCY)

# GET /currency/{symbol}
@bottle.get('/currency/<symbol>/<to>')
def currency_get_rate(symbol, to):
    bottle.response.content_type = 'application/json'
    if symbol in CURRENCY and to in CURRENCY[symbol]:
        return json.dumps(CURRENCY[symbol][to])
    else:
        bottle.abort(404, "Currency not found: " + symbol)


# GET /currency/{symbol}
@bottle.get('/currency/<symbol>')
def currency_get(symbol):
    bottle.response.content_type = 'application/json'
    if symbol in CURRENCY:
        return json.dumps(CURRENCY[symbol])
    else:
        bottle.abort(404, "Currency not found: " + symbol)


# GET /sequence
@bottle.get('/sequence')
def sequence_get():
    """
    Returns the shortest sequence of exchanges that yield a profit greater than 1.00% based upon the
    current set of currency exchange rates, as well as the actual profit percentage in JSON format.
    {
        "profit_percent": 1.25,
        "sequence": ["EUR", "USD", "RUB"]
    }
    """
    bottle.response.content_type = 'application/json'
    # TODO check if the matrix is valid

def bad_exchange_rate(x):
    return type(x) not in [int, float] or x <= 0.0


# POST /currency/{symbol}
@bottle.post('/currency/<symbol>')
def currency_post(symbol):
    """
    Add a new exchange, but filter all wrong currencies.
    Better to get inconsistent matrix, don't fix it on fly.
    """
    # TODO ask, why you can't PUT 
    # TODO validate
    # TODO check symbol is urlencoded/decoded
    if symbol in CURRENCY:
        bottle.abort(409, "Resource already exists: " + symbol)
        return
    new_currency = json.load(bottle.request.body)
    if type(new_currency) is not dict:
        bottle.abort(400, "new currency is not dict ")
        return
    for k,v in new_currency.items():
        if type(k) is not str or bad_exchange_rate(v):
            bottle.abort(400, "new currency has a wrong format")
            return
    if symbol in new_currency and new_currency[symbol] != 1.0:
        bottle.abort(400, "new currency has a wrong format")
        return
    # all checks are done
    new_currency[symbol] = 1.0
    CURRENCY[symbol] = dict((k,float(v)) for k,v in new_currency.items())
    # TODO If a resource has been created on the origin server,
    # the response SHOULD be 201 (Created) and contain an entity
    # which describes the status of the request and refers to the new resource,
    # and a Location header (see section 14.30).


# PUT /currency/{symbol}/{to}
@bottle.put('/currency/<symbol>/<to>')
def currency_put(symbol, to):
    """
    PUT updates or creates currency exchange rate.
    """
    new_rate = json.load(bottle.request.body)
    if bad_exchange_rate(new_rate):
        bottle.abort(400, "new exchange rate is not float")
    if symbol == to and new_rate != 1.0:
        bottle.abort(400, "new currency has a wrong format")
        return
    CURRENCY[symbol] = CURRENCY.get(symbol, dict())
    CURRENCY[symbol][to] = float(new_rate)


# https://openexchangerates.org/api/latest.json?app_id=b3e659bdc86440b18f9fa1860eec014e


APP_ID = "b3e659bdc86440b18f9fa1860eec014e"

def load_from_csv(path):
    """ This function doesn't parse quotes """
    global CURRENCY
    CURRENCY = dict()
    f = open(path)
    columns = map(lambda x: x.strip(), f.readline().split(",")[1:])
    for line in f:
        tmp = line.split(",")
        rates = map(float, tmp[1:])
        symbol = tmp[0].strip()
        CURRENCY[symbol] = dict(zip(columns, rates))
        assert CURRENCY[symbol][symbol] == 1.0
    print CURRENCY


def main():
    
    # for more complicated we should use https://github.com/kennethreitz/requests
    # TODO check status is 2xx
    # conn = httplib.HTTPSConnection("openexchangerates.org")
    # conn.request("GET", "/api/latest.json?app_id=" + APP_ID)
    # response = conn.getresponse()
    # print response.status, response.reason

    # Load from json if network is not available
    # response = open('rates.json')
    # data = json.load(response)
    # print data["base"]

    load_from_csv("rates.csv")

    # start server
    bottle.run(host='localhost', port=8080)



if __name__ == '__main__':
    main()







