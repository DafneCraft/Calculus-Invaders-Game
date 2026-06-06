from Limits import LimitGenerator
from Derivate import DerivativeGenerator
from Integral import IntegralGenerator

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite cualquier origen (ajústalo después)

@app.route('/limite', methods=['GET'])
def generar_limite():
    dificultad = request.args.get('dificultad', 'facil')
    if dificultad not in ['facil', 'medio', 'dificil']:
        return jsonify({'error': 'Dificultad inválida'}), 400
    try:
        problema = LimitGenerator.generate_problem(dificultad)
        return jsonify(problema)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/derivada', methods=['GET'])
def generar_derivada():
    dificultad = request.args.get('dificultad', 'facil')
    if dificultad not in ['facil', 'medio', 'dificil']:
        return jsonify({'error': 'Dificultad inválida'}), 400
    try:
        problema = DerivativeGenerator.generate_problem(dificultad)
        return jsonify(problema)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/integral', methods=['GET'])
def generar_integral():
    dificultad = request.args.get('dificultad', 'facil')
    if dificultad not in ['facil', 'medio', 'dificil']:
        return jsonify({'error': 'Dificultad inválida'}), 400
    try:
        problema = IntegralGenerator.generate_problem(dificultad)
        return jsonify(problema)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)