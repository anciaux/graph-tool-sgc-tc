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
        "Select the university", _filenames, key="unisersity_selector_stat")

    try:
        with open(f'match_{option}.json', "r") as f:
            courses_matches = yaml.safe_load(f.read())
    except Exception:
        st.error("Matching tab should be executed once at least")
        return

    df = pd.read_json(option+'.json')
    df_epfl = pd.read_json('EPFL.json')

    sorted_match = {}

    for epfl_title, other_title in courses_matches.items():
        epfl_class = df_epfl[df_epfl["Course Title"] == epfl_title].iloc[0]
        epfl_year = epfl_class['Year']
        epfl_semester = epfl_class['Semester']
        other_class = df[df["Course Title"] == other_title].iloc[0]

        if epfl_year not in sorted_match:
            sorted_match[epfl_year] = {}
        if epfl_semester not in sorted_match[epfl_year]:
            sorted_match[epfl_year][epfl_semester] = []

        sorted_match[epfl_year][epfl_semester].append(
            (epfl_class, other_class))

    def plot_class(layout, title, year, semester, ects):
        layout.markdown(f"**{title}**, Year{year}-{semester} ({ects} ECTS)")

    hide = st.checkbox("Show only mismatches")

    def are_classes_different(classes):
        cols = st.columns(len(classes))
        ref_class = classes[0]
        ref_title = ref_class['Course Title']
        ref_year = ref_class['Year']
        ref_semester = ref_class['Semester']
        ref_ects = ref_class['ECTS']

        for c, col in zip(classes[1:], cols[1:]):
            title = c['Course Title']
            year = c['Year']
            semester = c['Semester']
            ects = c['ECTS']

            if year != ref_year:
                year = f":red[{year}]"
            if semester != ref_semester:
                semester = f":red[{semester}]"
            if ects != ref_ects:
                ects = f":red[{ects}]"

            if year == ref_year and semester == ref_semester and ects == ref_ects and hide:
                return

            plot_class(col, option + " " + title, year, semester, ects)
        plot_class(cols[0], 'EPFL-' + ref_title,
                   ref_year, ref_semester, ref_ects)

        with st.expander('description', expanded=False):
            cols = st.columns(len(classes))
            for c, col in zip(classes[:], cols[:]):
                col.markdown('- ' + '\n - '.join(c['Description']))

    for year, semesters in sorted_match.items():
        for semester, matches in semesters.items():
            st.markdown(f'### Year {year} - {semester} Semester')
            for classes in matches:
                are_classes_different(classes)
                st.markdown('---')


def main():
    with st.spinner('Loading'):
        _main()
