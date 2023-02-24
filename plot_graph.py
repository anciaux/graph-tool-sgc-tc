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
                    default='ID,Degree,Year,ECTS,Semester',
                    help="Json file with cursus information")
parser.add_argument('--output', '-o', type=str, default='test.pdf',
                    help="Json file with cursus information")


arguments = parser.parse_args()
filename = arguments.input_filename
output = arguments.output
output_basename, ext = os.path.splitext(output)
print(output_basename)
################################################################

txt = open(filename).read()
content = json.loads(txt)
dot = create_graph(content)

dot.save(f'{output_basename}.dot')

cmd = f'dot -T{ext[1:]} -o{output} {output_basename}.dot'
print(cmd)
subprocess.call(cmd, shell=True)
