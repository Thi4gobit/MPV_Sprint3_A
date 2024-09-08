from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import requests

app = Flask(__name__)
api = Api(
    app, version='1.0.0', 
    title='Cycling',
    description='App for register your workouts of cycling',
    doc='/'
)

# URL da API externa
EXTERNAL_API_URL = "http://127.0.0.1:8000/workouts"

# Modelo de Item para a documentação Swagger
item_model = api.model('Workout', {
    'id': fields.Integer(readonly=True),
    'duration': fields.String(required=True, description='Format: HH:MM:SS.'),
    'date': fields.Date(required=True, description='Format: AAAA:MM:YY.'),
    'kilometers': fields.Float(required=True, description='The length (km).'),
    'frequency': fields.Integer(required=False, description='The heart rate per minute.'),
    'kcal': fields.Integer(required=False, description='The energy spent (kcal).')
})

# Recurso para listar e criar itens
@api.route('/items')
class ItemList(Resource):
    @api.doc('list_items')
    @api.marshal_list_with(item_model)
    def get(self):
        """Lista todos os itens"""
        response = requests.get(f"{EXTERNAL_API_URL}/get")
        if response.status_code == 200:
            return response.json(), 200
        return {'error': 'Failed to fetch items'}, response.status_code

    @api.doc('create_item')
    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self):
        """Cria um novo item"""
        data = request.get_json()
        response = requests.post(EXTERNAL_API_URL, json=data)
        if response.status_code == 201:
            return response.json(), 201
        return {'error': 'Failed to create item'}, response.status_code


# Recurso para obter, atualizar e deletar itens específicos
@api.route('/items/<int:item_id>')
@api.response(404, 'Item not found')
@api.param('item_id', 'The item identifier')
class Item(Resource):
    @api.doc('get_item')
    @api.marshal_with(item_model)
    def get(self, item_id):
        """Obter um item específico"""
        response = requests.get(f"{EXTERNAL_API_URL}/{item_id}")
        if response.status_code == 200:
            return response.json(), 200
        return {'error': 'Item not found'}, 404

    @api.doc('update_item')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, item_id):
        """Atualiza um item existente"""
        data = request.get_json()
        response = requests.put(f"{EXTERNAL_API_URL}/{item_id}", json=data)
        if response.status_code == 200:
            return response.json(), 200
        return {'error': 'Item not found or failed to update'}, 404

    @api.doc('delete_item')
    @api.response(204, 'Item deleted')
    def delete(self, item_id):
        """Deleta um item"""
        response = requests.delete(f"{EXTERNAL_API_URL}/{item_id}")
        if response.status_code == 200:
            return {'message': 'Item deleted'}, 200
        return {'error': 'Item not found or failed to delete'}, 404


if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, jsonify, request
# import requests

# app = Flask(__name__)

# # URL da API externa
# EXTERNAL_API_URL = "http://127.0.0.1:8000/workouts"

# # Rota GET - Obter todos os itens ou um item específico da API externa
# @app.route('/get', methods=['GET'])
# def get_items():
#     response = requests.get(f"{EXTERNAL_API_URL}/get")
#     if response.status_code == 200:
#         return jsonify(response.json()), 200
#     return jsonify({"error": "Failed to fetch items"}), response.status_code

# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     response = requests.get(f"{EXTERNAL_API_URL}/{item_id}")
#     if response.status_code == 200:
#         return jsonify(response.json()), 200
#     return jsonify({"error": "Item not found"}), response.status_code

# # Rota POST - Criar um novo item na API externa
# @app.route('/items', methods=['POST'])
# def create_item():
#     data = request.get_json()
#     response = requests.post(EXTERNAL_API_URL, json=data)
#     if response.status_code == 201:
#         return jsonify(response.json()), 201
#     return jsonify({"error": "Failed to create item"}), response.status_code

# # Rota PUT - Atualizar um item existente na API externa
# @app.route('/items/<int:item_id>', methods=['PUT'])
# def update_item(item_id):
#     data = request.get_json()
#     response = requests.put(f"{EXTERNAL_API_URL}/{item_id}", json=data)
#     if response.status_code == 200:
#         return jsonify(response.json()), 200
#     return jsonify({"error": "Item not found or failed to update"}), response.status_code

# # Rota DELETE - Deletar um item na API externa
# @app.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     response = requests.delete(f"{EXTERNAL_API_URL}/{item_id}")
#     if response.status_code == 200:
#         return jsonify({"message": "Item deleted"}), 200
#     return jsonify({"error": "Item not found or failed to delete"}), response.status_code

# # Executa o servidor Flask
# if __name__ == '__main__':
#     app.run(debug=True)
