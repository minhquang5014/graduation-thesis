from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button-click', methods=['POST'])
def button_click():
    return jsonify({'message': 'Button clicked!'})

if __name__ == '__main__':
    app.run(debug=True)
