#!/bin/env python

import streamlit as st
import pandas as pd
import os
import yaml
from wc import make_cloud_word

################################################################


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')
################################################################


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
        make_cloud_word("\n".join(c['Description']))

    with col3:
        with st.expander('Outcomes&Prerequisites'):
            st.markdown('Learning Outcomes')
            st.markdown(format_description(c['Learning outcomes']))
            st.markdown('Prerequisites')
            st.markdown(format_description(c['Pre-requisites']))
        try:
            make_cloud_word("\n".join(c['Learning outcomes']))
        except:
            pass


def _main(params):
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if (not e.startswith('Master_')
                                          and not e.startswith('match_'))]

    with st.spinner('Loading'):
        if 'courses' not in st.session_state:
            courses = {}
            for uni in _filenames:
                try:
                    df = pd.read_json(uni+'.json')
                    courses[uni] = df
                except Exception:
                    st.error(
                        f"Matching tab should be executed once at least {uni}")
                    return
            st.session_state['courses'] = courses
    courses = st.session_state['courses']
    search = st.text_input('Search in all registered classes')
    st.write(search)
    return
    idx = 0
    if 'class' in params:
        c = params['class'][0]
        opts = list(options)
        if c in opts:
            idx = opts.index(c)

    option = st.selectbox(
        "Select the EPFL class", options, index=idx, format_func=_fmt,
        key="epfl_class_selector_stat")

    for k, v in courses_matches.items():
        c = v[option]
        display_class(k, c)
        st.markdown('---')


def main(params={}):
    _main(params)
