#!/bin/env python

from class_distances import find_matching_classes, filter_word_lists
import streamlit as st
import pandas as pd
import os
import yaml

################################################################


def _main():
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if (not e.startswith('Master_')
                                          and not e.startswith('match_'))]

    option = st.selectbox(
        "Select the university", _filenames, key="unisersity_selector")

    try:
        with open(f'match_{option}.json', "r") as f:
            courses_matches = yaml.safe_load(f.read())
    except Exception:
        courses_matches = {}
    df = pd.read_json(option+'.json')
    df_epfl = pd.read_json('EPFL.json')

    df = filter_word_lists(df)
    df_epfl = filter_word_lists(df_epfl)

    match = find_matching_classes(df_epfl, df)
    for k, m in match.items():
        epfl_title = df_epfl.iloc[k]['Course Title']
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"*EPFL-match* for **{epfl_title}** with *{option}* is ")
            st.dataframe(m)
        with col2:
            options = list(m['Course Title'])
            if not options:
                st.write(f'no match for {epfl_title}')
                continue
            if epfl_title in courses_matches:
                sel = courses_matches[epfl_title]
            else:
                sel = options[0]
            selection = st.selectbox("Manual Matching",
                                     key=epfl_title+"_match_selectbox",
                                     options=options,
                                     index=options.index(sel))
            courses_matches[epfl_title] = selection
            scol1, scol2 = st.columns(2)
            _k = m[m["Course Title"] == selection].iloc[0]["original_index"]
            _class = df.iloc[_k]

            scol1.markdown(
                option + f" Year{_class['Year']} - {_class['Semester']}")
            scol1.markdown(f"({_class['ECTS']} ECTS) {selection}")

            _class = df_epfl.iloc[k]
            scol2.markdown(
                f"EPFL Year{_class['Year']} - {_class['Semester']}")
            scol2.markdown(f"({_class['ECTS']} ECTS) {epfl_title}")

            with st.expander("Keywords"):
                _col1, _col2 = st.columns(2)

                _class = df.iloc[_k]
                desc = _class["Description"]
                desc = "- " + "\n- ".join(desc)
                _col1.markdown(desc)

                _class = df_epfl.iloc[k]
                desc = _class['Description']
                desc = "- " + "\n- ".join(desc)
                _col2.markdown(desc)

    with open(f'match_{option}.json', "w") as f:
        f.write(yaml.safe_dump(courses_matches))

    st.markdown('## Raw data')
    st.dataframe(df)


def main():
    with st.spinner('Loading'):
        _main()
