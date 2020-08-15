#!/usr/bin/env python

'''Short summary here.
Longer docstring summary goes here.
'''

# import built-in modules below
import pickle
from tqdm import tqdm

# import own modules below
import Kaprekar as K

TIKZFILE = 'Attempt01.tex'

def write_preamble():
    preamble = '\n'.join([r'\documentclass[border=5mm]{standalone}',
                          r'\usepackage{tikz}',
                          r'\begin{document}',
                          r'\begin{tikzpicture}',
                          r'\usetikzlibrary{calc}',
                          r'\usetikzlibrary{backgrounds}'])
    with open(TIKZFILE, 'w') as tikzfile:
        tikzfile.write(preamble)

def write_ending():
    ending = '\n'.join([r'\end{tikzpicture}',
                        r'\end{document}'])
    with open(TIKZFILE, 'a') as tikzfile:
        tikzfile.write('\n'*3)
        tikzfile.write(ending)

def write_body():
    body = '\n'.join(tikz_code())
    with open(TIKZFILE, 'a') as tikzfile:
        tikzfile.write('\n'*3)
        tikzfile.write(body)


code_template_lines = [
    r'\node ({number}) at ({theta_coord}:{r_coord}pt) {{}};',
    r'\node ({number}) at ($(node cs:name={parent}) + ({theta_coord}:{r_coord}pt)$) {{}};',
    r'\filldraw[fill={color}] (node cs:name={number}) circle [radius=$({weight}+10)$pt];',
    r'\draw[color={parent_color}] ({number}) -- ({parent});']

def tikz_code() -> str:
    code = []
    counts_dict: Dict[int, int] = K.calculate_weights()
    sorted_counts = list(sorted(counts_dict.keys(), key=counts_dict.get, reverse = True))
    with open('database.pickle', 'rb') as dbfile:
        db = pickle.load(dbfile)
        for number in tqdm(sorted_counts):
            if db[number]['generation'] == 1:
                make_nodes = code_template_lines[0].format(**db[number])
                code.insert(0, make_nodes)
            elif db[number]['generation'] in [2,3,4]:
                make_nodes = code_template_lines[1].format(**db[number])
                code.append(make_nodes)
            else:
                continue
        for number in tqdm(sorted_counts):
            colors = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'black'}
            if db[number]['generation'] in [1,2,3,4]:
                draw_circles = code_template_lines[2].format(**db[number], color=colors[db[number]['generation']])
                draw_rays = code_template_lines[3].format(**db[number], parent_color=colors[db[db[number]['parent']]['generation']])
            else:
                continue
            code.extend([draw_rays, draw_circles])
    return code


write_preamble()
write_body()
write_ending()



