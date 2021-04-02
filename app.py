import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fetch import *

st.title('Corona Virus Statistics in Turkey')

DATA_URL = "https://raw.githubusercontent.com/ocakhasan/covid_data/master/turkey_covid.csv" 

def barchart(values, labels):
    fig = go.Figure(data=[go.Pie(labels=labels,
                                values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(template='plotly_dark')

    return fig

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Load 10,000 rows of data into the dataframe.
df = load_data()


df['Active'] = df['Confirmed'] - df['Recovered'] - df['Deaths'] 
st.subheader('Raw data')
st.write(df)
# Notify the reader that the data was successfully loaded.


#Total Cases

st.subheader('Total Corona Virus Numbers in Turkey')

values=[df['Active'].iloc[-1], df['Recovered'].iloc[-1], df['Deaths'].iloc[-1]]
colors = ['gold', 'mediumturquoise', 'darkorange']
labels=['Active','Recovered','Deaths']
fig = barchart(values, labels)
st.plotly_chart(fig)


#Daily Cases
labels=['Confirmed','Recovered','Deaths']
st.subheader('Daily '+ str(df['Date'].iloc[-1]) +' Statistics')

values=[df['Confirmed'].iloc[-1] -df['Confirmed'].iloc[-2], df['Recovered'].iloc[-1] - df['Recovered'].iloc[-2], df['Deaths'].iloc[-1] -df['Deaths'].iloc[-2]]

fig = barchart(values, labels)

st.plotly_chart(fig)

#Total Confirmed Cases
st.subheader("Confirmed Cases Over Time")
st.write("Let's see the how confirmed cases changed over time")

fig = px.bar(df,x='Date',y='Confirmed',color_discrete_sequence=['#5DADE2'])
fig.update_layout(template='plotly_dark')


st.plotly_chart(fig)

#Daily Cases
st.subheader('Case Number in Each Day')
df['New_Cases'] = df['Confirmed'] - df['Confirmed'].shift(1)
fig = px.bar(df,x='Date',y='New_Cases',color_discrete_sequence=['#1E8449'])
fig.update_layout(template='plotly_dark')

st.plotly_chart(fig)

#Total Death Cases
st.subheader('Total Death Cases')
fig = px.bar(df,x='Date',y='Deaths',color_discrete_sequence=['#7D3C98'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Daily Death Cases
st.subheader('Death Numbers in Each Day')
df['New_Deaths'] = df['Deaths'] - df['Deaths'].shift(1)
fig = px.bar(df,x='Date',y='New_Deaths',color_discrete_sequence=['#E67E22'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Test Numbers
st.subheader('Test Numbers in Each Day')
fig = px.bar(df,x='Date',y='Tests',color_discrete_sequence=['#5D6D7E'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Total Recovered Cases
st.subheader('Total Recovered Cases')
fig = px.bar(df,x='Date',y='Recovered',color_discrete_sequence=['#5199FF'])
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig)

#Daily Recovered Cases
st.subheader('Recovered Numbers in Each Day')
df['Recovered_Day'] = df['Recovered'] - df['Recovered'].shift(1)
fig = px.bar(df,x='Date',y='Recovered_Day',color_discrete_sequence=['#C0392B'])
fig.update_layout(template='ggplot2')
st.plotly_chart(fig)

#Tested Positive versus Negative
st.subheader('Tested People vs Positive Cases')
fig = go.Figure(data=[
go.Bar(name='Tested', y=df['Date'], x=df['Tests'], orientation='h'),
go.Bar(name='Positive', y=df['Date'], x=df['New_Cases'], orientation='h')])
fig.update_layout(barmode='stack',width=900, height=600)
st.plotly_chart(fig)

#Corona Virus Statistics in Turkey
st.subheader('Corona Virus Statistics in Turkey')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Confirmed'],
                    mode='lines+markers',marker_color='blue',name='Total Cases'))

fig.add_trace(go.Scatter(x=df['Date'], y=df['Recovered'],
                    mode='lines+markers',marker_color='green',name='Recovered Cases'))

fig.add_trace(go.Scatter(x=df['Date'], y=df['Deaths'],
                    mode='lines+markers',marker_color='red',name='Deaths Cases'))

fig.add_trace(go.Scatter(x=df['Date'], y=df['Active'],
                    mode='lines+markers',marker_color='#17202A',name='Active Cases'))

fig.update_layout(template='ggplot2')
st.plotly_chart(fig)

st.write("This is it. I will update every day.")