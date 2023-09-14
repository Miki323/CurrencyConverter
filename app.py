from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Currency Converter API',
          description='A simple currency converter REST API')

# URL сервиса, который предоставляет текущие курсы валют
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'

# Определяем модель данных для запроса
conversion_model = api.model('Conversion', {
    'from': fields.String(required=True, description='From currency code'),
    'to': fields.String(required=True, description='To currency code'),
    'value': fields.Float(required=True, description='Amount to convert')
})

# Параметры запроса для метода GET
get_parser = api.parser()
get_parser.add_argument('from', type=str, required=True, help='From currency code', location='args')
get_parser.add_argument('to', type=str, required=True, help='To currency code', location='args')
get_parser.add_argument('value', type=float, default=1, help='Amount to convert', location='args')


@api.route('/api/rates')
class CurrencyConversion(Resource):
    @api.expect(get_parser)
    def get(self):
        """
        Convert currency based on provided values
        """
        args = get_parser.parse_args()
        from_currency = args['from']
        to_currency = args['to']
        value = args['value']

        # Получаем текущие курсы валют с внешнего сервиса
        import requests
        response = requests.get(CURRENCY_API_URL)
        data = response.json()
        rates = data.get('rates', {})

        if from_currency not in rates or to_currency not in rates:
            return {"error": "Invalid currency"}, 400

        # Выполняем конвертацию валюты
        converted_value = (value / rates[from_currency]) * rates[to_currency]

        return {"result": round(converted_value, 2)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
