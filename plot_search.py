#!/bin/env python

import streamlit as st
import pandas as pd
import os
from class_distances import filter_word_lists
from wc import make_cloud_word

################################################################


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')
################################################################


def display_class(c):
    k = c['University']
    st.markdown(f'#### {k}')
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
        # try:
        #     # make_cloud_word("\n".join(c['Learning outcomes']))
        # except:
        #     pass


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

    value = ''
    if 'search' in params:
        value = params['search'][0]
    search = st.text_input('Search in all registered classes', value=value)
    if search == '':
        st.write("nothing to search...")
        return

    selected = pd.DataFrame()
    with st.spinner('Searching'):
        for uni, _classes in courses.items():
            sel = []
            df = filter_word_lists(_classes.copy())
            for i, c in df.iterrows():
                # st.write(c['Description'])
                if ' '.join(c['Description']).lower().find(search) != -1:
                    sel.append(_classes.iloc[i])
                elif c['Course Title'].lower().find(search.lower()) != -1:
                    sel.append(_classes.iloc[i])
            sel = pd.DataFrame(sel, columns=c.index)
            sel['University'] = uni
            selected = pd.concat([selected, sel])

    selected = selected.sort_values(['Year', 'Semester'])
    current_year = -1
    current_semester = ""
    is_changed = False
    for i, c in selected.iterrows():
        if current_year < c['Year']:
            current_year = c['Year']
            current_semester = ""
            is_changed = True
        if current_semester != c['Semester']:
            current_semester = c['Semester']
            is_changed = True
        if is_changed:
            st.markdown(
                f'<center> <h2>Year {current_year} - {current_semester}</h2></center>',
                unsafe_allow_html=True)
            is_changed = False
        display_class(c)


def main(params={}):
    _main(params)
