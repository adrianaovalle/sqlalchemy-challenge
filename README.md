# SQLAlchemy Challenge
The following work presents the analysis of temperatures in Honololu, Hawai for a trip planed between July 10-26.

## Climate Analysis and Exploration

## Data Inspection
There are 2 tables available: Measurement and Station.
* Measurement table contains: Precipitation (prcp), station, temperature (tobs), date and id. It has 19,550 rows.
* Station table contains: station, id, elevation, name, longitude and latitude. It has 9 rows.

The last date of available data is: 2017/08/23.

The following plot presents the last 12 months of precipitation data in Honolulu, HI.

![Figure](Images/Image1.png)


The histogram below presents the results for station USC00519281 for temperatures in the last 12 months of data.


![Figure](Images/Image2.png)

The plot below present the ranges of temperatures between the dates of 2017-07010 and 2017-07-26.


![Figure](Images/Image3.png)

The plot below presents the daily normals for the dates between 2017-07010 and 2017-07-26.


![Figure](Images/Image4.png)

## Climate App

Six API routes were created:
* /api/v1.0/
* /api/v1.0/precipitation
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/start
* /api/v1.0/start/end
