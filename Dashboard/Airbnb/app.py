from flask import Flask, render_template, request
from dotenv import load_dotenv, find_dotenv
import os

import numpy as np
import pandas as pd


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
	list_neighbourhood_group = eval(os.getenv('list_neighbourhood_group'))
	list_neighbourhood = eval(os.getenv('list_neighbourhood'))
	list_property_type = eval(os.getenv('list_property_type'))
	list_room_type = eval(os.getenv('list_room_type'))
	list_bathrooms_type = eval(os.getenv('list_bathrooms_type'))
	list_amenities = sorted(eval(os.getenv('list_amenities')))

	return render_template(
		'predict.html',

		list_neighbourhood_group = list_neighbourhood_group, 
		list_neighbourhood = list_neighbourhood,
		list_property_type = list_property_type,
		list_room_type = list_room_type,
		list_amenities = list_amenities,
		list_bathrooms_type = list_bathrooms_type
		)

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST':
		input = request.form

		input_columns = eval(os.getenv('list_column_input'))
		data = {k:input.get(k) for k in input_columns}

		numeric = ['accommodates', 'bedrooms', 'beds', 'price', 'minimum_nights', 
		'maximum_nights', 'availability_30', 'calculated_host_listings_count', 
		'total_bathrooms']
		amenities = eval(os.getenv('list_amenities'))

		for k in data:
			if k in numeric:
				data[k] = float(data[k])
			if k in amenities:
				data[k] = 0 if data[k] == None else 1

		df_to_predict = pd.DataFrame()
		for k in input_columns:
			df_to_predict = df_to_predict.append(pd.DataFrame.from_dict({k: data[k]}, orient='index'))
		df_to_predict = df_to_predict.T

	return render_template(
		'result.html',
		data = df_to_predict.columns,
		price_pred = 1000,
		bg = np.random.choice(range(0,5))
		)

@app.route('/portfolio-details/<page>', methods=['GET'])
def portfolio_details(page):
	
	return render_template(
		f'insight-{page}.html'
		)

@app.route('/map/<page>', methods=['GET'])
def show_map(page):
	return render_template(f'insight-{page}-map.html')


if __name__ == '__main__':
	load_dotenv(find_dotenv())
	app.run(debug=True, port=5000)