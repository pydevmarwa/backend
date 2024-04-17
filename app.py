from flask import Flask, jsonify
from flask_restx import Api, Resource


app = Flask(__name__)
api = Api(app)

# Dictionnaire pour stocker les piles
stacks = {}

# Liste des opérandes
operands = ["+", "-", "*", "/"]

# Endpoint pour lister tous les opérandes
@api.route('/rpn/op')
class OperandsResource(Resource):
    @api.doc('list_operands')
    def get(self):
        """Liste tous les opérandes disponibles"""        
        return jsonify(operands)

# Endpoint pour appliquer un opérande à une pile
@api.route('/rpn/op/<operand>/stack/<string:stack_id>')
class OperateOnStackResource(Resource):
    @api.doc('operate_on_stack')
    def post(self, stack_id):
        """Applique un opérande à une pile spécifique"""        
        if stack_id not in stacks or len(stacks[stack_id]) < 2:
            return jsonify({'error': 'Invalid stack or not enough values'}), 400

        second_value = stacks[stack_id].pop()
        first_value = stacks[stack_id].pop()

        if operand == '+':
            stacks[stack_id].append(first_value + second_value)
        elif operand == '-':
            stacks[stack_id].append(first_value - second_value)
        elif operand == '*':
            stacks[stack_id].append(first_value * second_value)
        elif operand == '/':
            if second_value == 0:
                return jsonify({'error': 'Division by zero'}), 400
            stacks[stack_id].append(first_value / second_value)
        else:
            return jsonify({'error': 'Invalid operand'}), 400

        return jsonify({'message': 'Operation performed'})

@api.route('/rpn/stack')
class StackResource(Resource):
# Endpoint pour lister toutes les piles disponibles
    @api.doc('list_stacks')
    def get(self):
        """Liste toutes les piles disponibles"""
        return jsonify(list(stacks.keys()))

# Endpoint pour créer une nouvelle pile
    @api.doc('create_stack')
    def post(self):
        """Crée une nouvelle pile"""
        stack_id = len(stacks) + 1
        stacks[stack_id] = []
        return jsonify({'stack_id': stack_id, 'message': 'Stack created'})

# Endpoint pour obtenir une pile spécifique
@api.route('/rpn/stack/<int:stack_id>')
class SpecificStackResource(Resource):
    @api.doc('get_stack')
    def get(self, stack_id):
        """Obtient une pile spécifique"""
        if stack_id not in stacks:
            return jsonify({'error': 'Stack not found'}), 404
        return jsonify(stacks[stack_id])

# Endpoint pour supprimer une pile spécifique
    @api.doc('delete_stack')
    def delete(self, stack_id):
        """Supprime une pile spécifique"""
        if stack_id not in stacks:
            return jsonify({'error': 'Stack not found'}), 404
        del stacks[stack_id]
        return jsonify({'message': 'Stack deleted'})

# Endpoint pour ajouter une nouvelle valeur à une pile
    @api.doc('push_value_to_stack')
    def put(self, stack_id):
        """Ajoute une nouvelle valeur à une pile spécifique"""        
        if stack_id not in stacks:
            return jsonify({'error': 'Stack not found'}), 404
        stacks[stack_id].append(int(request.json['value']))
        return jsonify({'message': 'Value pushed'})

if __name__ == '__main__':
    app.run(debug=True)