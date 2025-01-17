from flask import Flask, request
from flask_restx import Api, Resource, fields
import requests
from datetime import datetime, date


# EXTERNAL_API_URL = "http://localhost:8000/workouts"
EXTERNAL_API_URL = "http://django:8000/workouts"

app = Flask(__name__)
api = Api(
    app, version='1.0.0',
    title='Cycling - 5000',
    description='App for register your workouts of cycling',
    doc='/',
    default='Workout',
    default_label='Cycling'
)
item_model = api.model('Workout', {
    'id': fields.Integer(readonly=True),
    'date': fields.Date(required=True, description='Format: AAAA:MM:YY.', default=date.today()),
    'time_of_the_day': fields.String(required=False, description='Format: HH:MM.', default=f"{datetime.now().strftime("%H:%M:%S")}"),
    'city': fields.String(required=False, description='', default='Rio de Janeiro'),
    'state': fields.String(required=False, description='', default='RJ'),
    'kilometers': fields.Float(required=True, description='The length (km).', default=10.00),
    'duration': fields.String(required=True, description='Format: HH:MM:SS.', default='01:00:00'),
    'frequency': fields.Integer(required=False, description='The heart rate per minute.', default=150),
    'kcal': fields.Integer(required=False, description='The energy spent (kcal).', default=600),
    # 'temperature': fields.Float(required=False, description='Format: HH:MM.', example=None),
    'speed': fields.Float(readonly=True)
})


@api.route('/forecast/<string:city_name>/<string:uf>')
class Forecast(Resource):
    @api.doc(description='Get weather forecast')
    def get(self, city_name, uf):
        """Gets weather forecast"""
        KEY = 'b4a3ccab'
        response = requests.get(f"https://api.hgbrasil.com/weather?key={KEY}&city_name={city_name},{uf}&date={date.today()}&mode=all&fields=only_results,city_name,forecast,max,min,date")
        if response.status_code == 200:
            return response.json(), 200
        return {'error': 'Failed to fetch forecast'}, response.status_code
    

@api.route('/items')
class ItemList(Resource):
    @api.doc(description='List all items')
    def get(self):
        """Lists all items"""
        response = requests.get(f"{EXTERNAL_API_URL}/get")
        if response.status_code == 200:
            return response.json(), 200
        return {'error': 'Failed to fetch items'}, response.status_code


@api.route('/new')
class ItemNew(Resource):
    @api.doc(description='Create a new item')
    @api.expect(item_model)
    def post(self):
        """Creates a new item"""
        data = request.get_json()
        response = requests.post(f"{EXTERNAL_API_URL}/post", json=data)
        if response.status_code == 200:
            return response.json(), 200
        return response.json(), response.status_code


@api.route('/update/<int:pk>')
class ItemUpdate(Resource):
    @api.doc(description='Update an existing item')
    @api.expect(item_model)
    def patch(self, pk):
        """Updates an existing item"""
        data = request.get_json()
        response = requests.patch(f"{EXTERNAL_API_URL}/update/{pk}", json=data)
        if response.status_code == 200:
            return response.json(), 200
        return response.json(), response.status_code


@api.route('/delete/<int:pk>')
class ItemDelete(Resource):
    @api.doc(description='Delete an item')
    def delete(self, pk):
        """Deletes an item"""
        response = requests.delete(f"{EXTERNAL_API_URL}/delete/{pk}")
        if response.status_code == 200:
            return response.json(), 200
        return response.json(), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
