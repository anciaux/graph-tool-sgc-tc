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


def _main():
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
                f" (Year {lab['Year']} - {lab['Semester']})")

    option = st.selectbox(
        "Select the EPFL class", options, format_func=_fmt,
        key="epfl_class_selector_stat")

    for k, v in courses_matches.items():
        c = v[option]
        display_class(k, c)
        st.markdown('---')


def main():
    with st.spinner('Loading'):
        _main()
