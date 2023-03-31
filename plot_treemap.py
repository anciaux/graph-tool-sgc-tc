#!/bin/env python

import streamlit as st
import plot_treemap_bachelor
import plot_treemap_master
import plot_statistics

st.set_page_config(layout="wide")

opt = st.radio('Choose Degree', options=['Bachelor', 'Master', 'Statistics'])

if opt == 'Bachelor':
    plot_treemap_bachelor.main()

if opt == 'Master':
    plot_treemap_master.main()

if opt == 'Statistics':
    plot_statistics.main()
