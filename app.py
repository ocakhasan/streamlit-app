import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fetch import *
from streamlit_folium import folium_static
import folium
import json

st.title('Corona Virus Statistics in Turkey')

DATA_URL = "https://raw.githubusercontent.com/ocakhasan/covid_data/master/turkey_covid.csv" 
CITIES_URL = "https://raw.githubusercontent.com/ocakhasan/covid_data/master/city_risks.csv"
GEOSON_DATA = "cities.json"

def barchart(values, labels):
    fig = go.Figure(data=[go.Pie(labels=labels,
                                values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(template='plotly_dark')

    return fig

@st.cache(allow_output_mutation=True)
def load_data(TTL=24*60*60):
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])
    cities = pd.read_csv(CITIES_URL)
    geo_str = json.dumps(json.load(open(GEOSON_DATA, 'r', encoding="utf-8"))) # harita verisi
    return data, cities, geo_str

# Load 10,000 rows of data into the dataframe.
df, cities, geo_str = load_data()


df['Active'] = df['Confirmed'] - df['Recovered'] - df['Death'] 
st.subheader('Raw data')
st.write(df)
# Notify the reader that the data was successfully loaded.


#Total Cases

st.subheader('Total Corona Virus Numbers in Turkey')

values=[df['Active'].iloc[-1], df['Recovered'].iloc[-1], df['Death'].iloc[-1]]
colors = ['gold', 'mediumturquoise', 'darkorange']
labels=['Active','Recovered','Deaths']
fig = barchart(values, labels)
st.plotly_chart(fig)


#Daily Cases
labels=['Confirmed','Recovered','Deaths']
st.subheader('Daily '+ str(df['Date'].iloc[-1].strftime("%Y/%m/%d")) +' Statistics')

values=[df['Daily_Confirmed'].iloc[-1], df['Daily_Recovered'].iloc[-1], df['Daily_Death'].iloc[-1]]

fig = barchart(values, labels)

st.plotly_chart(fig)

st.subheader("Risk Cases in the Map with colors")

m = folium.Map(location=[39.9208, 35], zoom_start=5.4,tiles="cartodbpositron")

scale = np.linspace(cities["risks"].min() - 1, cities["risks"].max() + 1, 6, dtype=int).tolist()
latitudes = cities['latitudes'].values
longitudes = cities['longitudes'].values
locations = list(zip(latitudes, longitudes))
cpth = folium.Choropleth(
            geo_data=geo_str, # harita verisi
            data=cities, # gostermek istedigimiz veri
            columns=['cities', 'risks'], # istenilen sutunlar
            fill_color='BuPu',
            key_on='feature.properties.name',
            legend_name="Number of cases per 100000 people").add_to(m)
    
cpth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], labels=False)
)
folium.LayerControl().add_to(m)
folium_static(m)

st.subheader("Risk Cases in the Map with Numbers")

m = folium.Map(location=[39.9208, 35], zoom_start=5.4,tiles="cartodbpositron")
for i in range(cities.shape[0]):
    folium.Circle(
        radius=cities.loc[i, 'risks'] * 100,
        location=[cities.loc[i, 'latitudes'], cities.loc[i, 'longitudes']],
        popup=cities.loc[i, 'cities']+ "-" + str(cities.loc[i, "risks"]), 
        color="#3186cc",
        fill=True,
        fill_color="#3186cc"
).add_to(m)
    
folium_static(m)



#Total Confirmed Cases
st.subheader("Confirmed Cases Over Time")
st.write("Let's see the how confirmed cases changed over time")

fig = px.bar(df,y='Confirmed',color_discrete_sequence=['#5DADE2'])
fig.update_layout(template='plotly_dark')


st.plotly_chart(fig)

#Daily Cases
st.subheader('Case Number in Each Day')

df['daily_confirmed_mean'] = df['Daily_Confirmed'].rolling(7).mean()
fig = go.Figure()

fig.add_trace(go.Scatter( y=df['Daily_Confirmed'],
                    mode='lines+markers',marker_color='blue',name='Daily Confirmed'))

fig.add_trace(go.Scatter( y=df['daily_confirmed_mean'],
                    mode='lines+markers',marker_color='red',name='7 Day Average'))
fig.update_layout(template='plotly_dark')

st.plotly_chart(fig)

#Total Death Cases
st.subheader('Total Death Cases')
fig = px.bar(df,y='Death',color_discrete_sequence=['#7D3C98'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Daily Death Cases
st.subheader('Death Numbers in Each Day')
df['daily_death_mean'] = df['Daily_Death'].rolling(7).mean()
fig = go.Figure()

fig.add_trace(go.Scatter( y=df['Daily_Death'],
                    mode='lines+markers',marker_color='blue',name='Daily Death Cases'))

fig.add_trace(go.Scatter( y=df['daily_death_mean'],
                    mode='lines+markers',marker_color='red',name='7 Day Average'))



fig.update_layout(template='ggplot2')
st.plotly_chart(fig)

#Test Numbers
st.subheader('Test Numbers in Each Day')
fig = px.bar(df,y='Test',color_discrete_sequence=['#5D6D7E'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Total Recovered Cases
st.subheader('Total Recovered Cases')
fig = px.bar(df,y='Recovered',color_discrete_sequence=['#5199FF'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Daily Recovered Cases
st.subheader('Recovered Numbers in Each Day')
df['daily_recovered_mean'] = df['Daily_Recovered'].rolling(7).mean()
fig = go.Figure()

fig.add_trace(go.Scatter( y=df['Daily_Recovered'],
                    mode='lines+markers',marker_color='blue',name='Daily Recovered Cases'))

fig.add_trace(go.Scatter( y=df['daily_recovered_mean'],
                    mode='lines+markers',marker_color='red',name='7 Day Average'))



fig.update_layout(template='ggplot2')
st.plotly_chart(fig)



#Corona Virus Statistics in Turkey
st.subheader('Corona Virus Statistics in Turkey')
fig = go.Figure()
fig.add_trace(go.Scatter( y=df['Confirmed'],
                    mode='lines+markers',marker_color='blue',name='Total Cases'))

fig.add_trace(go.Scatter(y=df['Recovered'],
                    mode='lines+markers',marker_color='green',name='Recovered Cases'))

fig.add_trace(go.Scatter( y=df['Death'],
                    mode='lines+markers',marker_color='red',name='Deaths Cases'))

fig.add_trace(go.Scatter( y=df['Active'],
                    mode='lines+markers',marker_color='#17202A',name='Active Cases'))

fig.update_layout(template='ggplot2')
st.plotly_chart(fig)

st.write("This is it. I will update every day.")