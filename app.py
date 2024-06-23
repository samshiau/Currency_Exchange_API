from flask import Flask, request, jsonify

app = Flask(__name__)

class CurrencyExchangeService:
    def __init__(self, exchange_rates):
        self.exchange_rates = exchange_rates

    def convert(self, source, target, amount):
        return amount * self.exchange_rates[source][target]


exchange_rates = {  #using dict for faster lookup and ease of maintenance
    "TWD": {"TWD": 1, "JPY": 3.669, "USD": 0.03281},
    "JPY": {"TWD": 0.26956, "JPY": 1, "USD": 0.00885},
    "USD": {"TWD": 30.444, "JPY": 111.801, "USD": 1},
}

currency_exchange_service = CurrencyExchangeService(exchange_rates)  #injection of dependency offering flexibility


@app.route('/exchange', methods=['GET'])
def exchange():

    #getting the query parameters
    source = request.args.get('source')
    target = request.args.get('target')
    amount = request.args.get('amount')

    if not source or not target or not amount: #checking if the query parameters are missing
        return jsonify({"msg": "error", "error": "Missing query parameters"}), 400
    
    if source not in exchange_rates or target not in exchange_rates[source]: #checking if the currency code is TWD, JPY, or USD
        return jsonify({"msg": "error", "error": "Invalid currency code"}), 400

    try:   #checking if the value of amount is a number and remove comma if exists
        amount = float(amount.replace(',', ''))  #allowing comma as thousand separator
    except ValueError:  
        return jsonify({"msg": "error", "error": "Invalid amount format"}), 400

    if amount < 0: #checking if the value of amount is negative
        return jsonify({"msg": "error", "error": "Negative amount"}), 400

    try:  #calling the conversion method
        result = CurrencyExchangeService.convert(source, target, amount)
    except ValueError as e:
        return jsonify({"msg": "error", "error": str(e)}), 400
    
    result = round(result, 2)  #rounding the result to 2 decimal places
    result_with_comma = "{:,}".format(result) #adding comma as thousand separator
    result_final = result_with_comma.rstrip('0').rstrip('.') #removing trailing zeros and dot
    
    return jsonify({"msg": "success", "amount": result_final})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
