#!/bin/env python

from wc import make_cloud_word
from class_distances import find_matching_classes
import streamlit as st
import plotly.express as px
import pandas as pd
import os
################################################################


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')
################################################################


def plot_course_detail(df, selected_course):

    selected_info = df.loc[df['Course Title'] == selected_course]
    st.markdown('### Title: ' + str(selected_info['Course Title'].iloc[0]))
    st.markdown('### ECTS: ' + str(selected_info['ECTS'].iloc[0]))
    st.markdown('### Period: ' +
                selected_info['Year'].iloc[0] + ' ' +
                selected_info['Semester'].iloc[0])

    st.markdown('### URL: [fiche de cours](' +
                str(selected_info['URL'].iloc[0]) + ')')
    st.markdown('## Description')
    col, _ = st.columns(2)
    with col:
        make_cloud_word(selected_info['Description'].iloc[0])
    st.markdown(selected_info['Description'].iloc[0])
    st.markdown('## Learning Outcomes')
    st.markdown(format_description(selected_info['Learning outcomes'].iloc[0]))
    st.markdown('## Prerequisites')
    st.markdown(format_description(selected_info['Pre-requisites'].iloc[0]))


################################################################


def main():
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if (not e.startswith('Master_')
                                          and not e.startswith('match_'))]

    st.markdown('# Cursus explorator')

    option = st.selectbox(
        "Select the university", _filenames)

    df_epfl = pd.read_json('EPFL.json')
    df = pd.read_json(option+'.json')

    raw_df = pd.read_json(option+'.json')

    df['Year'] = df['Year'].apply(lambda x: 'Year'+str(x))
    df['Description'] = df['Description'].apply(format_description)

    df_epfl['Year'] = df_epfl['Year'].apply(lambda x: 'Year'+str(x))
    df_epfl['Description'] = df_epfl['Description'].apply(format_description)

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

    match = find_matching_classes(df.copy(), df_epfl.copy())
    # for k, m in match.items():
    #     st.markdown(f"# {df.iloc[k]['Course Title']}")
    #     st.dataframe(m, use_container_width=True)

    match_result = st.empty()
    match_result.markdown("## Searching closest EPFL class")

    col, col_EPFL = st.columns(2)
    with col:
        st.markdown(f'### {option} Course details')
        selected_course = st.selectbox('', df['Course Title'].sort_values())
        plot_course_detail(df, selected_course)

    with col_EPFL:
        st.markdown("### Closest EPFL classes")
        for k, m in match.items():
            if df.iloc[k]['Course Title'] == selected_course:
                selected_epfl_course = st.selectbox('', m['Course Title'])

                m = m.drop(columns='original_index')
                m = m.rename(
                    columns={'Number Match': "Number of matching words"})
                with match_result.container():
                    st.markdown(
                        f'# Classes Matching {option}-{selected_course}')
                    st.dataframe(m)

                plot_course_detail(df_epfl, selected_epfl_course)

    st.markdown('## Raw data')
    st.dataframe(raw_df)
