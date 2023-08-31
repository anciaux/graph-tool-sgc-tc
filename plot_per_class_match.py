#!/bin/env python

import streamlit as st
import pandas as pd
import os
import yaml
import plotly.express as px
# from wc import make_cloud_word

################################################################


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')
################################################################


def display_class_summary(k, c):
    st.write(
        f"{k}: {c['Course Title']} ({c['ECTS']} ECTS, Year {c['Year']})")  # {c['Semester']} {c['URL']})")


def display_class(k, c):
    st.markdown(f'## {k}')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('Title: ' + c['Course Title'])
        st.markdown('ECTS: ' + str(c['ECTS']))
        st.markdown('Period: Year ' +
                    str(c['Year']) + ' ' +
                    c['Semester'])

        st.markdown('URL: [fiche de cours](' +
                    str(c['URL']) + ')')
    with col2:
        with st.expander('Description'):
            st.markdown(format_description(c['Description']))
        # make_cloud_word("\n".join(c['Description']))

    with col3:
        with st.expander('Outcomes&Prerequisites'):
            st.markdown('Learning Outcomes')
            st.markdown(format_description(c['Learning outcomes']))
            st.markdown('Prerequisites')
            st.markdown(format_description(c['Pre-requisites']))
        try:
            pass
            # make_cloud_word("\n".join(c['Learning outcomes']))
        except:
            pass


def _main(params):
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if (not e.startswith('Master_')
                                          and not e.startswith('match_'))]

    _filenames.remove('EPFL')
    courses_matches = {}
    for uni in _filenames:
        try:
            with open(f'match_{uni}.json', "r") as f:
                match = yaml.safe_load(f.read())
                df = pd.read_json(uni+'.json')
                courses_matches[uni] = {}
                for k, v in match.items():
                    courses_matches[uni][k] = df[df['Course Title']
                                                 == v].iloc[0]
        except Exception:
            st.error(f"Matching tab should be executed once at least {uni}")
            return

    df_epfl = pd.read_json('EPFL.json')
    options = df_epfl.sort_values(by=['Year', 'Semester', 'Course Title'])[
        'Course Title']

    def _fmt(opt):
        lab = df_epfl[df_epfl['Course Title'] == opt].iloc[0]
        return (f"{lab['Course Title']}"
                f" (Year {lab['Year']} - {lab['Semester']} - {lab['ECTS']} ECTS)")

    idx = 0
    if 'class' in params:
        c = params['class'][0]
        opts = list(options)
        if c in opts:
            idx = opts.index(c)

    option = st.selectbox(
        "Select the EPFL class", options, index=idx, format_func=_fmt,
        key="epfl_class_selector_stat")

    summary = st.checkbox('show summary', value=False)

    courses_matches['EPFL'] = {option: df_epfl[df_epfl['Course Title']
                                               == option].iloc[0]}

    found = pd.DataFrame()
    for k, v in courses_matches.items():
        c = v[option]
        c['University'] = k
        c = pd.DataFrame([c], columns=c.index)
        found = pd.concat([found, c])

    if not summary:
        found['BA'] = (found['Year']-1)*2 + \
            (found['Semester'] == 'Spring') + 1

        plot = px.bar(found, x='BA', color='University',
                      y='ECTS', barmode='group', text='Course Title')
        st.plotly_chart(plot, use_container_width=True)

    for k, v in courses_matches.items():
        c = v[option]
        if summary:
            display_class_summary(k, c)
        else:
            display_class(k, c)
            st.markdown('---')


def main(params):
    with st.spinner('Loading'):
        _main(params)
