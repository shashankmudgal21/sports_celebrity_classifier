from flask import Flask, request, jsonify,render_template
import util

app = Flask(__name__, template_folder='./UI', static_folder='./UI')

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/classify', methods= ['GET', 'POST'])
def classify_img():
    image_data = request.form['image_data']
    
    response = jsonify(util.classify_img(image_data))
    response.headers.add('Access-Control-ALlow-Origin', '*')
    return response



if __name__ == '__main__':
    util.load_model()
    app.run(debug=True)
    