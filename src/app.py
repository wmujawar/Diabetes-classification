import os
from flask import Flask, request, render_template
from model import DiabetesModel

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data:
        return 'No data provided', 400, {'Content-Type': 'text/plain'}

    model = DiabetesModel()
    return model.predict(data)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=False)