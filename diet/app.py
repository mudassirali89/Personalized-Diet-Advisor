from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)

# Load the dataset
def load_dataset():
    dataset = {}
    with open('disease_food.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            disease = row['disease'].lower()
            food = row['food'].lower()
            allowed = row['allowed'].lower() == 'yes'
            if disease not in dataset:
                dataset[disease] = {}
            dataset[disease][food] = allowed
    return dataset

dataset = load_dataset()

@app.route('/')
def index():
    diseases = list(dataset.keys())
    return render_template('index.html', diseases=diseases)

@app.route('/check_food', methods=['POST'])
def check_food():
    disease = request.form['disease'].lower()
    food = request.form['food'].lower()
    if disease in dataset and food in dataset[disease]:
        allowed = dataset[disease][food]
        return jsonify({'allowed': allowed})
    else:
        return jsonify({'allowed': False, 'message': 'No information available for this disease or food item'})

if __name__ == '__main__':
    app.run(debug=True)
