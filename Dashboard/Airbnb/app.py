from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/problems', methods=['GET'])
def problems():
	return render_template('problems.html')

@app.route('/data', methods=['GET'])
def data():
	return render_template('data.html')

@app.route('/predict/<result>', methods=['GET', 'POST'])
def predict(result=False):
	neigh_group = ['Central Region', 'East Region', 'West Region', 'North-East Region']
	neigh = ['Orchard', 'Marina Bay', 'Bedok']
	property_type = ['House', 'Hotel']
	room_type = ['Room1', 'Room2']
	bedroom = ['bedroom1']
	bed = ['bed1']
	amenities = ['TV', 'AC', 'BBQ', 'Baby and Children Equipment', 'Ski-in/Ski-out', 'Whaser', 'Beachfront']

	return render_template(
		'predict.html',

		neigh_group = neigh_group, 
		neigh = neigh,
		property_type = property_type,
		room_type = room_type,
		bedroom = bedroom,
		bed = bed,
		amenities = amenities
		)

@app.route('/check_form', methods=['GET', 'POST'])
def check_form():
	if request.method == 'POST':
		data = request.form
		print(data)
		print(data)
		print(data)
		print(data)
	return render_template(
		'check_form.html',
		data = data)

@app.route('/portfolio-details', methods=['GET'])
def portfolio_details():
	
	return render_template(
		'portfolio-details.html'
		)


if __name__ == '__main__':
	app.run(debug=True, port=5000)