#!/bin/env python
################################################################
import graphviz
################################################################


def create_year_graph(year):

    graph = graphviz.Digraph(
        name=f'cluster_year{year}',
        body=["graph[style=bold];"])


infos = ['ID', 'Degree', 'Year', 'ECTS', "Semester"]

courses = set()

for i, e in enumerate(content):
    title = e['Course Title']
    if title in courses:
        raise RuntimeError(f'class {title} already registered')
    courses.add(title)
    year = e['Year']
    label = '{' + title + '|'
    for _i in infos:
        if _i in e:
            label += '\\n' + str(_i) + ': ' + str(e[_i])
    label += '}'

    dot = years[year-1]
    dot.node(title, label=label, URL=e['URL'])
    prereq = e["Pre-requisites"]
    if prereq:
        for p in prereq:
            print(title, p)
            dot.edge(p, title, style='dotted')

# check pre-req dependencies
for i, e in enumerate(content):
    prereq = e["Pre-requisites"]
    if prereq:
        for p in prereq:
            if p not in courses:
                print(f'pre-req class {p} not found in courses')

dot = graphviz.Digraph(
    comment='Bachelor',
    node_attr={'shape': 'record'},
    body='''
    rankdir=LR
    edge[fontname="Helvetica", fontsize="10",
    labelfontname="Helvetica", labelfontsize="10"]
    node[fontname="Helvetica", fontsize="10", shape=record]
    ''')

for y in years:
    dot.subgraph(y)

return dot
