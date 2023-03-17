#!/bin/env python

import sys
import streamlit as st
import plotly.express as px
import pandas as pd
import os
# from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")
_filenames = os.listdir()

_filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
_filenames = [os.path.splitext(e)[0] for e in _filenames]

st.markdown('# Cursus explorator')

option = st.selectbox(
    "Select the university", _filenames)

df = pd.read_json(option+'.json')
raw_df = pd.read_json(option+'.json')


def convertYear(x):
    if x == 0:
        return 'Any Year'
    return 'Year'+str(x)


df['Year'] = df['Year'].apply(convertYear)


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')


df['Description'] = df['Description'].apply(format_description)

df.insert(0, 'Title',
          df.apply(lambda x: x['Course Title'] +
                   '<br>ECTS:' + str(x['ECTS']), axis=1))


fig = px.treemap(df, path=[px.Constant("all"),
                           'Degree', 'Year', 'Semester', 'Title'], values='ECTS',
                 # hover_name='Course Title',
                 # hover_data=['Description']
                 )
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
# fig.show()


# selected_item = plotly_events(fig, click_event=True, hover_event=False)
# print(selected_item)
st.plotly_chart(fig, use_container_width=True)


st.markdown('# Course details')
selected_course = st.selectbox('', df['Course Title'].sort_values())

selected_info = df.loc[df['Course Title'] == selected_course]
st.markdown('### ECTS: ' + str(selected_info['ECTS'].iloc[0]))
st.markdown('### Period: ' +
            selected_info['Year'].iloc[0] + ' ' +
            selected_info['Semester'].iloc[0])

st.markdown('### URL: [fiche de cours](' +
            str(selected_info['URL'].iloc[0]) + ')')
st.markdown('## Description')
st.markdown(selected_info['Description'].iloc[0])
st.markdown('## Learning Outcomes')
st.markdown(format_description(selected_info['Learning outcomes'].iloc[0]))

st.markdown('## Prerequisites')
st.markdown(format_description(selected_info['Pre-requisites'].iloc[0]))

st.markdown('## Raw data')
st.dataframe(raw_df)
