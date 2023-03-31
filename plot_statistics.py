#!/bin/env python

from wc import make_cloud_word, stopwords
import numpy as np
import streamlit as st
from Levenshtein import distance
import pandas as pd
import os

################################################################
stopwords = set(stopwords.split('\n'))
stopwords.add('several')
# st.write(stopwords)


def filter_word_lists(df):

    def format_description(x):
        if not x:
            return x
        w_list = []
        for e in x:
            w_list += [e.strip() for e in e.split(' ') if e.strip() != '']

        def replace_punctuation(e):
            reps = '+-./%,:;_=?~1234567890()'
            for c in reps:
                e = e.replace(c, '')
            return e
        w_list = [replace_punctuation(e).lower() for e in w_list]
        w_list = [e for e in w_list if e != '']

        x = set(w_list)
        x = x-stopwords
        return x

    df['Description'] = df['Description'].apply(format_description)
    df['Learning outcomes'] = df['Learning outcomes'].apply(format_description)
    df['Pre-requisites'] = df['Pre-requisites'].apply(format_description)

    df = df.drop(columns=['URL', 'Degree'])
    return df

################################################################


def word_to_cloud_distance(word, cloud):
    if not cloud:
        return 5e15

    distances = []
    for w in cloud:
        distances.append(distance(word, w))
    return np.array(distances).min()
################################################################


def cloud_to_cloud_distances(cloud1, cloud2):
    if not cloud1:
        return 5e15
    distances = []
    for w in cloud1:
        distances.append(word_to_cloud_distance(w, cloud2))
    return np.mean(distances)

################################################################


def find_matching_classes(df1, df2, field='Description'):
    matching_classes = {}

    for i, _class1 in df1.iterrows():
        correlation = []
        for idx, _class2 in df2.iterrows():
            d = cloud_to_cloud_distances(
                _class1[field],
                _class2[field])
            if d < 50000:
                correlation.append((idx, d, _class2['Course Title']))
        correlation = pd.DataFrame(correlation, columns=[
                                   'original_index', 'Distance', 'Course Title'])
        correlation = correlation.sort_values(by=['Distance'])
        correlation = correlation.iloc[:4]
        matching_classes[i] = correlation
    return matching_classes

################################################################


def main():
    _filenames = os.listdir()

    _filenames = [e for e in _filenames if os.path.splitext(e)[1] == '.json']
    _filenames = [os.path.splitext(e)[0] for e in _filenames]
    _filenames = [os.path.splitext(e)[0]
                  for e in _filenames if not e.startswith('Master_')]

    option = st.selectbox(
        "Select the university", _filenames)

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
