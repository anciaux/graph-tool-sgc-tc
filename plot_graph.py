#!/bin/env python
################################################################
import json
import os
import subprocess
import argparse
from create_graph import create_graph
################################################################

parser = argparse.ArgumentParser(description='CursusDraw')
parser.add_argument('input_filename', type=str,
                    help="Json file with cursus information")
parser.add_argument('--infos', type=str,
                    default='',
                    help="Json file with cursus information")
parser.add_argument('--output', '-o', type=str, default='',
                    help="File to produce")
parser.add_argument('--show_prereq', action='store_true',
                    help="Requests to show pre-requisites as edges")

arguments = parser.parse_args()
filename = arguments.input_filename
output = arguments.output
if output == '':
    input_basename, ext = os.path.splitext(filename)
    output = input_basename + '.pdf'
    output = output.replace(' ', '_')
output_basename, ext = os.path.splitext(output)
infos = arguments.infos.split(',')
infos = [e for e in infos if e.strip() != '']
print(output_basename)
################################################################

txt = open(filename).read()
content = json.loads(txt)
dot = create_graph(content, infos, show_prereq=arguments.show_prereq)

dot.save(f'{output_basename}.dot')

cmd = f'dot -T{ext[1:]} -o{output} {output_basename}.dot'
print(cmd)
subprocess.call(cmd, shell=True)
