# Singapore's Airbnb Price Predictor
<a href="http://sg-airbnb.yosiadityan.xyz/">
	<img src="https://img.shields.io/static/v1?label=Live%20Dashboard&message=Online&color=brightgreen&style=for-the-badge&logo=heroku">
</a>
<i><b>Click the badge to redirect to 
  <a href="http://sg-airbnb.yosiadityan.xyz/">
    live dashboard
  </a>
</b></i>

<br>

![alt text](https://images.unsplash.com/photo-1483070472046-4defb528eff3?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1350&q=80)
<span>Photo by <a href="https://unsplash.com/@lvnatikk?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Lily Banse</a> on <a href="https://unsplash.com/s/photos/singapore?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>

## Problem Statement
### COVID-19 Background
One year has passed since COVID-19 pandemic spread throughout the world, slowing down the economic growth in all parts of the world. Many countries applied lockdown as their measures to contain the spread of the virus, resulting in slump demand for tourism all over the world. But, recently some countries has lift the lockdown measures as their effort to suppressed the COVID-19 cases. Resulting in thriving economic post-pandemic and increasing demand for tourism.

### Why Singapore?
Singapore is one of those successful countries to fight against pandemic. They start to open their border for travellers and hopefully can revive its tourism industry as soon as possible. Singapore’s tourism industry itself is vital for Singapore as it makes 4.1% of their national GDP (2017).

As the tourism industry started to grow, one of the important thing the traveler will need is accommodation as a place to spend the night.

### About Airbnb
Aside from hotel, Airbnb is another choice for traveller to look for accomodation in their travel destination. Airbnb is an American vacation rental online marketplace company. Through the service, users can arrange lodging, primarily homestays, and tourism experiences or list their properties for rental. Airbnb does not own any of the listed properties; instead, it profits by receiving commission from each booking.

### Machine Learning as Solution
As the lockdown measure has been lifted and tourism demand increases, Singapore resident can rent their properties in Airbnb to gain extra income sources and help to boost the economic growth in their countries. But, choosing the right competitive price is difficult since there are so many factors to be considered and calculated.

Machine learning can help to do those calculations and predict the correct listing price for new host as accurate as possible. This model can also be helpful for former host to revalue their listing into new competitive price and also for traveller to plan their budget for accommodations suiting their needs.


## About Dataset
The dataset used for this project is downloaded from Inside Airbnb. The data behind the Inside Airbnb site is sourced from publicly available information from the Airbnb site. The data has been analyzed, cleansed and aggregated where appropriate to facilitate public discussion. The data that I will be using is Singapore’s Airbnb listing that is last scraped on December 29, 2020 and contains 4387 listing information. The dataset contains 4 CSV files, there are:

- Calendar (1.6M rows and 7 columns)
Listings availability information  in time series format

- Listings (4387 rows and 74 columns)
Detailed Listings data for Singapore

- Reviews (55 rows and 2 columns)
Detailed Review Data for listings in Singapore

- Neighbourhood (53984 rows and  6 columns)
Neighbourhood list for geofilter. Sourced from city or open source GIS files.

For prediction model building, we'll only use <b>Listings</b> file only.


Notes:
- Airbnb doesn't provide any column description for each file. Hence, the description for each column will be assumed based on its values and name


## Insights from Exploratory Data Analysis
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Dashboard/Airbnb/static/assets/img/portfolio/insight-3-map.png)
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Dashboard/Airbnb/static/assets/img/portfolio/insight-2-map.png)
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Dashboard/Airbnb/static/assets/img/portfolio/insight-5-plot.png)


## Dashboard Preview
### Home Page
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Assets/home.png)
### Problem Statement Page
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Assets/problems.png)
### Data Insight Page
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Assets/data.png)
### Prediction Page
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Assets/predict.png)
### Prediction Result Page
![alt text](https://github.com/yosiadityan/sg-airbnb/blob/master/Assets/result.png)