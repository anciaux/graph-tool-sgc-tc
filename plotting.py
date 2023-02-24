#!/bin/env python
################################################################
import json
import graphviz
import subprocess
import argparse
import sys
################################################################

parser = argparse.ArgumentParser(description='CursusDraw')
parser.add_argument('input_filename', type=str,
                    help="Json file with cursus information")

arguments = parser.parse_args()
filename = arguments.input_filename

################################################################

txt = open(filename).read()
content = json.loads(txt)


def create_graph(title):
    return graphviz.Digraph(name=title, body=["graph[style=bold];"])


years = [create_graph('cluster_year1'), create_graph(
    'cluster_year2'), create_graph('cluster_year3')]

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

dot.save('test.dot')
subprocess.call('dot -Tpdf -o test.pdf test.dot', shell=True)
