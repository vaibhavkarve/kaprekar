#!/usr/bin/env python

'''Short summary here.
Longer docstring summary goes here.
'''

# import built-in modules below
import pickle
from tqdm import tqdm
from typing import Tuple, List, Dict

# import own modules below
import Kaprekar as K

TIKZFILE = 'Attempt03.tex'
MAX_GENS = 7


with open('database.pickle', 'rb') as dbfile:
    db = pickle.load(dbfile)

descendants_ = K.descendants()
code_template_lines = [
    r'\node[scale=0.1] ({number}) at ({theta_coord}:{r_coord}pt) {{}};',
    r'\filldraw[fill=red] (node cs:name={number}) circle [radius=10pt];',
    r'\draw[color={color}] ({number}) to [out={theta}, in={parent_theta}] ({parent});']
    

def generate_preamble():
    preamble = '\n'.join([r'\documentclass[border=1in]{standalone}',#r'\usepackage[paperheight=200in,paperwidth=200in,margin=1in,heightrounded]{geometry}',
                          r'\usepackage{tikz}',
                          r'\usetikzlibrary{calc}',
                          r'\usetikzlibrary{arrows.meta}'
                          r'\begin{document}',
                          r'\definecolor{a}{RGB}{0,154,202}',
                          r'\definecolor{b}{RGB}{255,205,178}',
                          r'\definecolor{c}{RGB}{246,178,162}',
                          r'\definecolor{d}{RGB}{230,152,155}',
                          r'\definecolor{e}{RGB}{181,131,140}',
                          r'\definecolor{f}{RGB}1{09,104,118}',
                          r'\centering',
                          r'\topskip0pt',
                          r'\vspace*{\fill}',
                          r'\begin{tikzpicture}'])
    return preamble

def generate_ending():
    ending = '\n'.join([r'\end{tikzpicture}',
                        r'\vspace*{\fill}',
                        r'\end{document}'])
    return ending

def generate_body():
    body = '\n'.join(tikz_code())
    return body


def find_correct_order() -> Dict[int, List[int]]:
    correct_order = {1: [0, 6174]}
    for _ in range(MAX_GENS-1):
        j = max(correct_order.keys())
        correct_order[j+1] = []
        for number in correct_order[j]:
            siblings = sorted(descendants_[number])
            siblings = filter(lambda x: x!=number, siblings)
            correct_order[j+1].extend(siblings)
    return correct_order

correct_order = find_correct_order()
counts_dict: Dict[int, int] = K.calculate_weights()


def radius_and_theta(number) -> Tuple[int, int]:
    if number == 0:
        return 20, 35
    if number == 6174:
        return 10, 180
    radii = {2: 120, 3: 194, 4: 314, 5: 508, 6: 821, 7: 1328, 8: 2148, 9: 3475}
    gen_number = db[number]['generation']
    radius = radii[gen_number]/2
    theta = 360/len(correct_order[gen_number])*correct_order[gen_number].index(number)
    return radius, theta


def colors(number):
    gen = db[number]['generation']
    choice = {1: 'a', 2: 'a', 3: 'b', 4: 'c', 5: 'd',
              6: 'e', 7:'f'}
    choice = ['black' for i in range(10)]
    return choice[gen]

def tikz_code() -> str:
    code = []
    fill_nodes = []
    for number in tqdm(range(10_000)):
        if db[number]['generation'] > MAX_GENS:
            continue
        radius, theta = radius_and_theta(number)
        make_nodes = code_template_lines[0].format(number=number, r_coord = radius, theta_coord = theta)
        code.append(make_nodes)
    for gen in tqdm(correct_order.keys()):
        for number in tqdm(correct_order[gen]):
            theta = radius_and_theta(number)[1]
            parent_theta = radius_and_theta(db[number]['parent'])[1]
            draw_rays = code_template_lines[2].format(number=number,
                                                      color=colors(number),
                                                      parent=db[number]['parent'],
                                                      theta=theta + 90,
                                                      parent_theta=parent_theta)
            code.append(draw_rays)#, draw_circles])
    return code + fill_nodes


with open(TIKZFILE, 'w') as tikzfile:
    tikzfile.write(generate_preamble())
    tikzfile.write('\n'*3)
    tikzfile.write(generate_body())
    #tikzfile.write(r'\filldraw[fill=red] (node cs:name=0) circle [radius=2pt];')
    #tikzfile.write(r'\filldraw[fill=red] (node cs:name=6174) circle [radius=2pt];')
    tikzfile.write('\n'*3)
    tikzfile.write(generate_ending())
print()


