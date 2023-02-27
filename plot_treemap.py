import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_json('TU Delft.json')
print(df.columns)

df['Year'] = df['Year'].apply(lambda x: 'Year'+str(x))
df['Description'] = df['Description'].apply(
    lambda x: ('<br>' + '<br>'.join(x)).replace(';', '<br>'))

df.insert(0, 'Title', df.apply(
    lambda x: x['Course Title'] + '<br>ECTS:' + str(x['ECTS']),  axis=1))
fig = px.treemap(df, path=[px.Constant("all"),
                           'Degree', 'Year', 'Semester', 'Title'], values='ECTS',
                 hover_name='Course Title',
                 hover_data=['Description']
                 )
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
# fig.show()

st.plotly_chart(fig)
