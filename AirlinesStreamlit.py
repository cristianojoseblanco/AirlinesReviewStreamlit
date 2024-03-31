import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import streamlit as st

pio.templates.default = "plotly_dark"

df = pd.read_csv('airlines_reviews.csv')

df['Review Date'] = pd.to_datetime(df['Review Date'])

dict_month = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 
              'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

dict_month_2 = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 
                8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

df['Month'] = df['Month Flown'].apply(lambda x: dict_month.get(x.split(' ')[0]))
df['Year'] = df['Month Flown'].apply(lambda x: x.split(' ')[1])

st.set_page_config(layout='wide')


year = st.sidebar.selectbox('Year', 
                            np.sort(df['Year'].unique())
                            )

month = st.sidebar.selectbox('Month', 
                            np.sort(df['Month'].unique())
                            )

airline = st.sidebar.selectbox('Airline', 
                            df['Airline'].unique()
                            )

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6, col7 = st.columns(3)
col8, col9, col10 = st.columns(3)


df_filtered_month = df[(df['Year']==year) & 
                       (df['Month']==month)]

df_filtered_airline = df[(df['Airline']==airline) & 
                         (df['Year']==year) & 
                         (df['Month']==month)]

df_filtered_year_airline = df[(df['Year']==year) &
                              (df['Airline']==airline)].groupby('Month')['Overall Rating'].mean()

df_filtered_year_not_airline = df[(df['Year']==year) &
                                  (df['Airline']!=airline)].groupby('Month')['Overall Rating'].mean()


fig_box_Overall_Rating = px.box(
    df_filtered_month, 
    x='Airline', 
    y='Overall Rating',
    color='Airline',
    color_discrete_map={i:'#6666ff' if i==airline else '#0000b2' for i in df_filtered_month['Airline'].unique()},
    title='Airlines Ratings Comparison ({}, {})'.format(dict_month_2.get(month), year)
    )
col1.plotly_chart(fig_box_Overall_Rating, use_container_width=True)

fig_pie = px.pie(
    df_filtered_month, 
    names='Airline', 
    color='Airline', 
    color_discrete_map={i:'#6666ff' if i==airline else '#0000b2' for i in df_filtered_month['Airline'].unique()},
    opacity=0.85,
    hole=0.5,
    title='Airlines Flights Reviewed({}, {})'.format(dict_month_2.get(month), year)
    )
col2.plotly_chart(fig_pie, use_container_width=True)

fig_line = go.Figure(layout_title_text='Mean Overall Rating by Review in {}'.format(year))

fig_line.add_trace(
    go.Scatter(x=df_filtered_year_airline.index, 
               y=df_filtered_year_airline.values,
               name='{}'.format(airline),
               line= dict(color='#6666ff')
               ))

fig_line.add_trace(
    go.Scatter(x=df_filtered_year_not_airline.index, 
               y=df_filtered_year_not_airline.values,
               name='Other companies',
               line= dict(color='#0000b2')
               ))

if (month in df_filtered_year_airline) & (month in df_filtered_year_not_airline):
    if df_filtered_year_airline.get(key=month) > df_filtered_year_not_airline.get(key=month):
        fig_line.add_trace(
            go.Scatter(x=[month, month], 
                    y=[df_filtered_year_airline.get(key=month), df_filtered_year_not_airline.get(key=month)],
                    mode = 'lines',
                    line = dict(shape = 'linear', 
                                color = '#006600', 
                                dash = 'dot'),
                    name='Positive Delta Rating (+{:.1f})'.format(df_filtered_year_airline.get(key=month)-
                                                               df_filtered_year_not_airline.get(key=month))
                    ))
    else:
        fig_line.add_trace(
            go.Scatter(x=[month, month], 
                    y=[df_filtered_year_airline.get(key=month), df_filtered_year_not_airline.get(key=month)],
                    mode = 'lines',
                    line = dict(shape = 'linear', 
                                color = '#e50000', 
                                dash = 'dot'),
                    name='Negative Delta Rating ({:.1f})'.format(df_filtered_year_airline.get(key=month)-
                                                              df_filtered_year_not_airline.get(key=month))
                    ))

fig_line.update_xaxes(tickmode='linear')
col3.plotly_chart(fig_line)

fig_hist_Staff_Service = px.histogram(
    df_filtered_airline, 
    x='Staff Service', 
    title='Staff Service',
    color_discrete_sequence=['#6666ff']
    )
fig_hist_Staff_Service.update_layout(bargap=0.1)
col5.plotly_chart(fig_hist_Staff_Service, use_container_width=True)

fig_hist_Food_Beverages = px.histogram(
    df_filtered_airline, 
    x='Food & Beverages', 
    title='Food & Beverages',
    color_discrete_sequence=['#6666ff']
    )
fig_hist_Food_Beverages.update_layout(bargap=0.1)
col6.plotly_chart(fig_hist_Food_Beverages, use_container_width=True)

fig_hist_Inflight_Entertainment = px.histogram(
    df_filtered_airline, 
    x='Inflight Entertainment', 
    title='Inflight Entertainment',
    color_discrete_sequence=['#6666ff']
    )
fig_hist_Inflight_Entertainment.update_layout(bargap=0.1)
col7.plotly_chart(fig_hist_Inflight_Entertainment, use_container_width=True)

fig_hist_Value_For_Money = px.histogram(
    df_filtered_airline, 
    x='Value For Money',
    title='Value For Money',
    color_discrete_sequence=['#6666ff']
    )
fig_hist_Value_For_Money.update_layout(bargap=0.1)
col8.plotly_chart(fig_hist_Value_For_Money, use_container_width=True)

fig_hist_Seat_Comfort = px.histogram(
    df_filtered_airline,
    x='Seat Comfort', 
    title='Seat Comfort',
    color_discrete_sequence=['#6666ff']
    )
fig_hist_Seat_Comfort.update_layout(bargap=0.1)
col9.plotly_chart(fig_hist_Seat_Comfort, use_container_width=True)

fig_bar = px.bar(
    df_filtered_airline, 
    x='Class',
    title='Class',
    color_discrete_sequence=['#6666ff']
    )
col10.plotly_chart(fig_bar, use_container_width=True)
