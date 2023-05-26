#!/bin/env python

from class_distances import find_matching_classes, filter_word_lists
import streamlit as st
import pandas as pd
import os

################################################################


def main():
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if not e.startswith('Master_')]

    option = st.selectbox(
        "Select the university", _filenames, key="unisersity_selector")

    df = pd.read_json(option+'.json')
    df_epfl = pd.read_json('EPFL.json')

    df = filter_word_lists(df)
    df_epfl = filter_word_lists(df_epfl)

    match = find_matching_classes(df_epfl, df)
    for k, m in match.items():
        st.markdown(
            f"*EPFL-match* for **{df_epfl.iloc[k]['Course Title']}** with *{option}* is ")
        st.dataframe(m)

    st.markdown('## Raw data')
    st.dataframe(df)
