#!/bin/env python

import streamlit as st
import plot_treemap_bachelor
import plot_treemap_master
import plot_all_match
import plot_statistics

st.set_page_config(layout="wide")

tab_explore, tab_match, tab_statistics = st.tabs(
    ["Explore", "Matching Classes", "Statistics"])

with tab_explore:
    opt = st.radio('Choose Degree', options=['Bachelor', 'Master'])

    if opt == 'Bachelor':
        plot_treemap_bachelor.main()

    if opt == 'Master':
        plot_treemap_master.main()

with tab_match:
    plot_all_match.main()

with tab_statistics:
    plot_statistics.main()
