#!/bin/env python

import streamlit as st
import plot_treemap_bachelor
import plot_treemap_master
import plot_all_match
import plot_best_match
import plot_per_class_match
import plot_search

st.set_page_config(layout="wide")
params = st.experimental_get_query_params()

if 'view' in params and params['view'][0] == 'tab_per_class':
    plot_per_class_match.main(params)
elif 'view' in params and params['view'][0] == 'tab_search':
    plot_search.main(params)

else:
    tab_explore, tab_match, tab_best_match, tab_per_class, tab_search = st.tabs(
        ["Explore", "Matching Classes",
         "Best Matches", "Per Class Match", "search"])

    with tab_explore:
        opt = st.radio('Choose Degree', options=['Bachelor', 'Master'])

        if opt == 'Bachelor':
            plot_treemap_bachelor.main()

        if opt == 'Master':
            plot_treemap_master.main()

    with tab_match:
        plot_all_match.main()

    with tab_best_match:
        plot_best_match.main()

    with tab_per_class:
        plot_per_class_match.main({})

    with tab_search:
        plot_search.main()
