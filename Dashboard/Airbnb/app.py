from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv, find_dotenv
import os

import numpy as np
import pandas as pd

import pickle
import sqlalchemy as db
import plotly
import plotly.graph_objs as go
import json
import requests

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
	list_property_type = eval(os.getenv('list_property_type'))
	list_room_type = eval(os.getenv('list_room_type'))
	list_bathroom_type = eval(os.getenv('list_bathroom_type'))
	list_amenities = sorted(eval(os.getenv('list_amenities')))
	list_neighbourhood_names = eval(os.getenv('list_neighbourhood_names'))

	return render_template(
		'predict.html',

		list_neighbourhood_group = list_neighbourhood_group, 
		list_property_type = list_property_type,
		list_room_type = list_room_type,
		list_amenities = list_amenities,
		list_bathroom_type = list_bathroom_type,
		list_neighbourhood_names = list_neighbourhood_names
		)

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST':
		input = request.form

		input_columns = eval(os.getenv('list_column_input'))
		data = {k:input.get(k) for k in input_columns}

		numeric = ['accommodates', 'bedrooms', 'beds', 'price', 'minimum_nights', 
		'maximum_nights', 'availability_30', 'calculated_host_listings_count', 
		'total_bathrooms', 'latitude', 'longitude', 'calculated_host_listings_count_entire_homes', 
		'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms']
		boolean = ['instant_bookable']
		amenities = eval(os.getenv('list_amenities'))

		data['neighbourhood_group_cleansed'] = eval(input.get('neighbourhood'))[0]
		data['neighbourhood_cleansed'] = eval(input.get('neighbourhood'))[1]

		address = input.get('address')+ ', Singapore'
		params = {'q': address, 'apiKey': os.getenv('apiKey')}
		response = requests.get(os.getenv('heremaps'), params=params)
		data['latitude'] = response.json()['items'][0]['position']['lat']
		data['longitude'] = response.json()['items'][0]['position']['lng']

		for k in data:
			if k in numeric:
				data[k] = float(data[k])
			if k in amenities:
				data[k] = 0 if data[k] == None else 1
			if k in boolean:
				data[k] = True if data[k] == 'True' else False

		df_to_predict = pd.DataFrame()
		for k in input_columns:
			df_to_predict = df_to_predict.append(pd.DataFrame.from_dict({k: data[k]}, orient='index'))
		df_to_predict = df_to_predict.T.copy()

		with open('Models/'+'best_model.pkl', 'rb') as f:
			model = pickle.load(f)
		price_pred = model.predict(df_to_predict)

	return render_template(
		'result.html',
		data = data,
		price_pred = f'{price_pred[0]:.2f}',
		bg = np.random.choice(range(0,5))
		)

def make_plot(page):
	list_graphJSON = []

	# Price Distribution
	if page == 1:
		data = [go.Histogram(x=df_dict['listings']['price'])]
		layout = go.Layout(
			title_text='Price Distributions',
			title_x=0.5,
			xaxis_title_text='Price',
			yaxis_title_text='Count')
		result = {'data': data, 'layout': layout}
		graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)
		list_graphJSON.append(graphJSON)

	if page == 2:
		sankey_data = (df_dict['listings']
               .groupby(['neighbourhood_group_cleansed', 'neighbourhood_cleansed'])
               .agg(Count=('id', 'count'))).reset_index()
		neigh_group_map = {x:idx for idx, x in enumerate(sankey_data.neighbourhood_group_cleansed.unique())}
		colors = ["#ffbe0b","#fb5607","#8338ec","#ff006e","#3a86ff"]

		sankey_data['neigh_group'] = sankey_data.neighbourhood_group_cleansed.map(neigh_group_map)
		sankey_data['neigh'] = [x+5 for x in sankey_data.index.tolist()]
		sankey_data['neigh_colors'] = [colors[x] for x in sankey_data.neigh_group]

		data = go.Sankey(
			node = dict(pad=15, 
                thickness=20, 
                line=dict(color = "black", width = 0.5), 
                label=(sankey_data.neighbourhood_group_cleansed.unique().tolist() + 
                       sankey_data.neighbourhood_cleansed.unique().tolist()),
                customdata=(sankey_data.neighbourhood_group_cleansed.unique().tolist() + 
                            sankey_data.neighbourhood_cleansed.unique().tolist()),
                color=["#ffbe0b","#fb5607","#8338ec","#ff006e","#3a86ff"] + sankey_data.neigh_colors.tolist(),
                hovertemplate='%{customdata} has total listing of %{value}<extra></extra>',
               ),
			link = dict(source=sankey_data.neigh_group.tolist(), 
                target=sankey_data.neigh.tolist(), 
                value=sankey_data.Count.tolist(),
                customdata=(sankey_data.neighbourhood_group_cleansed.unique().tolist() + 
                            sankey_data.neighbourhood_cleansed.unique().tolist()),
                hovertemplate=('Neighbourhood Group: <b>%{source.customdata}</b><br />' + 
                               'Neighbourhood Name: <b>%{target.customdata}</b><br />')
               ))
		fig = go.Figure(data=[data])
		fig.update_layout(font_size=10, height=1000, 
		                  title_text='Number of Listings in Each Neighbourhood', title_x=0.5)
		list_graphJSON.append(fig.to_json())

	if page == 3:
		sankey_data = (df_dict['listings']
               .groupby(['neighbourhood_group_cleansed', 'neighbourhood_cleansed'])
               .agg(Count=('id', 'count'))).reset_index()
		neigh_group_map = {x:idx for idx, x in enumerate(sankey_data.neighbourhood_group_cleansed.unique())}
		colors = ["#ffbe0b","#fb5607","#ff006e","#8338ec","#3a86ff"]
		box_data = df_dict['listings']
		neigh_group_cm = {x:y for x,y in zip(neigh_group_map, colors)}
		fig = go.Figure()
		for idx, neigh_group in enumerate(box_data.neighbourhood_group_cleansed.unique()):
		    fig.add_trace(
		        go.Box(x=box_data[box_data.neighbourhood_group_cleansed == neigh_group]['price'], 
		               name=neigh_group, marker_color=neigh_group_cm[neigh_group])
		    )
		fig.update_layout(
		    title_text='Price Boxplot For Each Neighbourhood Group',
		    title_x=0.5,
		    xaxis_title_text='Price', 
		    xaxis_zeroline=False)
		list_graphJSON.append(fig.to_json())

		by_neigh = df_dict['listings'].groupby('neighbourhood_group_cleansed')

		fig = go.Figure()
		for neigh in ['West Region', 'East Region', 'Central Region', 'North-East Region', 'North Region'][::-1]:
		    fig.add_trace(go.Violin(x=by_neigh.get_group(neigh)['price'], 
		                            line_color=neigh_group_cm[neigh], 
		                            name=neigh, showlegend=False))

		fig.update_traces(orientation='h', side='positive', width=3, points=False)
		fig.update_layout(
		    xaxis_showgrid=False, 
		    xaxis_zeroline=False,  
		    title_text='Price Distribution For Each Neighbourhood Group',
		    title_x=0.5,
		    xaxis_title_text='Price')
		list_graphJSON.append(fig.to_json())

	if page == 4:
		by_room = df_dict['listings'].groupby('room_type')
		by_room_count = by_room.agg(Count=('id', 'count')).reset_index().sort_values('Count', ascending=False)
		data = go.Bar(x=by_room_count['room_type'], y=by_room_count['Count'], 
		              text=by_room_count['Count'], textposition='auto', 
		              marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
		layout = go.Layout(
		    title_text='Countplot For Room Type',
		    title_x=0.5)
		fig = go.Figure(data=data, layout=layout)
		list_graphJSON.append(fig.to_json())


		fig = go.Figure()
		for room in ['Entire home/apt', 'Private room', 'Hotel room', 'Shared room'][::-1]:
		    fig.add_trace(go.Violin(x=by_room.get_group(room)['price'], 
		                            name=room, showlegend=False))

		fig.update_traces(orientation='h', side='positive', width=3, points=False)
		fig.update_layout(
		    xaxis_showgrid=False, 
		    xaxis_zeroline=False,  
		    title_text='Price Distribution For Each Room Type',
		    title_x=0.5,
		    xaxis_title_text='Price')
		list_graphJSON.append(fig.to_json())


	return list_graphJSON

@app.route('/insights/<page>', methods=['GET'])
def portfolio_details(page):

	title = {
		1: 'Price Distributions',
		2: 'Listing Location',
		3: 'Price and Location',
		4: 'Price and Room Type',
		5: 'Price and Amenities',
		6: 'Lorem',
	}
	trivia = {
		1: '''<b>80%</b> of listings in Singapore (3498 out of 4372) is priced under <b>SGD200</b>''',
		2: '''<b>Kallang</b> is the neighbourhood with the most Airbnb listing in Singapore''',
		3: '''If you're travelling with limited budget to Singapore, try to look for Airbnb listing in <b>North East Region</b>! It has the lowest median price among other region''',
		4: '''Instead of Private Room, try to look for Hotel as they usually offer more convenience and has pretty much same price as Private room''',
		5: '''Check out the distribution table to help plan your budget by checking what amenities you want in your Airbnb and their median price''',
		6: 'Lorem',
	}
	explanation = {
		1: '''The Airbnb listings price in Singapore is heavily right-skewed with median of SGD114. The lowest listings price is SGD13 and the highest is SGD3000 or around <b>230 times</b> more expensive than the cheapest listings''',
		2: '''Central Region is the most populated neighbourhood group for Airbnb listings with <b>81.15%</b> listing in this area, followed by West Region and East Region with 6.31% and 5.63% of total listing respectively. For neighbourhood, Kallang is the neighbourhood with the most listing making up <b>13.61%</b> of total listing in Singapore''',
		3: '''<b>Central Region</b> has the highest median of listing's price in Singapore with median of SGD123. Central Region also the region with the most price variance in Singapore with maximum price of SGD3000 and minimum price of SGD15.''',
		4: '''Listing with room type of Entire home/apt is the second most common among other room types and with higher median price. This probably because there are different types of room/apt ranging from common one to luxurious one. The Private room and Hotel room has quite same distribution with not so different price median (SGD17 difference in median price). Shared room is the least common and the lowest median price, only SGD48.5.''',
		5: '''The table above shows price distribution for each amenities and its median price. <b>Baby and Children Equipments</b> amenities has the highest median price among all amenities. Sauna and Ski-in/Ski-out doesn't have price distribution graph since each only has one listing and quite surprisingly (at least to me), these two amenities has listing with relatively cheap price, SGD50 adn SGD30 respectively.''',
		6: '''Lorem''',
	}
	image = {
		1: ('',''),
		2: ('/static/assets/img/portfolio/insight-2-map.png', 'insight-2-map.html'),
		3: ('/static/assets/img/portfolio/insight-3-map.png', 'insight-3-map.html'),
		4: ('',''),
		5: ('/static/assets/img/portfolio/insight-5-plot.png',''),
		6: ('',''),
	}

	if 'html' in page:
		return render_template(page)
	else:
		list_plot = make_plot(int(page))

		return render_template(
			'insight.html',
			page=page,
			title=title[int(page)],
			list_plot=list(enumerate(list_plot)),
			trivia=trivia[int(page)],
			explanation=explanation[int(page)],
			image=image[int(page)]
		)

def get_data():
	engine = db.create_engine(os.getenv('db-uri'))
	meta = db.MetaData()
	meta.reflect(engine)
	df_dict = dict()

	with engine.connect() as con:
		for table in meta.tables.keys():
			query = db.select([meta.tables[table]])
			all_data = con.execute(query).fetchall()
			df_dict[table] = pd.DataFrame(all_data, columns=meta.tables[table].c.keys())

	return df_dict

if __name__ == '__main__':
	load_dotenv(find_dotenv())
	df_dict = get_data()
	app.run(debug=True, port=5000)