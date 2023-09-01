#!/bin/env python

import streamlit as st
import pandas as pd
import os
import plotly.express as px
from class_distances import filter_word_lists
# from wc import make_cloud_word

################################################################


def format_description(x):
    if not x:
        return "Empty"
    return ('- ' + '\n- '.join(x)).replace(';', '\n')
################################################################


def display_class_summary(c):
    k = c['University']
    st.write(
        f"{k}: {c['Course Title']} ({c['ECTS']} ECTS, Year {c['Year']} {c['Semester']} {c['URL']}))")


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

    search = st.text_input(
        'Search in all registered bachelor classes', value=value)

    search_str = search
    summary = st.checkbox('show summary', value=False)

    search = search.split('+')
    search = [e.strip().lower() for e in search]
    search = list(set(search))

    selected = pd.DataFrame()
    with st.spinner('Searching'):
        for uni, _classes in courses.items():
            sel = []
            df = filter_word_lists(_classes.copy())
            for i, c in df.iterrows():
                for s in search:
                    # st.write(c['Description'])
                    if ' '.join(c['Description']).lower().find(s) != -1:
                        sel.append(_classes.iloc[i])
                    elif c['Course Title'].lower().find(s) != -1:
                        sel.append(_classes.iloc[i])
            sel = pd.DataFrame(sel, columns=c.index)
            sel['University'] = uni
            selected = pd.concat([selected, sel])

    selected = selected.sort_values(['Year', 'Semester'])

    with st.expander('Filter results'):
        if "removed" in params:
            removed = ','.join(params["removed"]).split(',')
        else:
            removed = []
        list_selected = list(selected['Course Title'])
        default = list(set(list_selected) - set(removed))
        confirmed = st.multiselect('Selected courses', options=list_selected,
                                   default=default)

        list_removed = set(list_selected) - set(confirmed)
        selected = selected[selected['Course Title'].isin(
            confirmed)].reset_index(drop=True)

        st.markdown(
            f'[permlink](/?view=tab_search&search={search_str.replace(" ", "%20")}&removed={",".join(list_removed).replace(" ", "%20")})')

    if not summary:
        selected['BA'] = (selected['Year']-1)*2 + \
            (selected['Semester'] == 'Spring') + 1

        plot = px.bar(selected, x='BA', color='University',
                      y='ECTS', barmode='group', text='Course Title')
        st.plotly_chart(plot, use_container_width=True)

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
            if not summary:
                st.markdown(
                    f'<center> <h2>Year {current_year} - {current_semester}</h2></center>',
                    unsafe_allow_html=True)
            is_changed = False
        if not summary:
            display_class(c)
        else:
            display_class_summary(c)


def main(params={}):
    _main(params)
