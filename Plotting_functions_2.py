#!/usr/bin/env python

'''Short summary here.
Longer docstring summary goes here.
'''

# import built-in modules below
import pickle
from tqdm import tqdm

# import own modules below
import Kaprekar as K

TIKZFILE = 'Attempt02.tex'

def write_preamble():
    preamble = '\n'.join([r'\documentclass{article}',
                          r'\usepackage[paperheight=28in,paperwidth=28in,margin=1in,heightrounded]{geometry}',
                          r'\usepackage{tikz}',
                          r'\usetikzlibrary{calc}',
                          r'\usetikzlibrary{backgrounds}',
                          r'\usetikzlibrary{arrows.meta}'
                          r'\begin{document}',
                          r'\centering',
                          r'\topskip0pt',
                          r'\vspace*{\fill}',
                          r'\begin{tikzpicture}'])

    with open(TIKZFILE, 'w') as tikzfile:
        tikzfile.write(preamble)

def write_ending():
    ending = '\n'.join([r'\end{tikzpicture}',
                        r'\vspace*{\fill}',
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
    r'\filldraw[fill={color}] (node cs:name={number}) circle [radius={weight}pt];',
    r'\draw[-Triangle Cap, line width = {thickness}, color={parent_color}] ({number}) to [out={theta}, in={parent_theta}]({parent});']


def tikz_code() -> str:
    code = []
    counts_dict: Dict[int, int] = K.calculate_weights()
    sorted_counts = list(sorted(counts_dict.keys(), key=counts_dict.get, reverse = True))
    radii = {1: 0, 2: 120, 3: 300, 4: 700, 5: 1000, 6: 1200}
    with open('database.pickle', 'rb') as dbfile:
        db = pickle.load(dbfile)
        new_thetas = {number: 360*(db[number]['index_within_generation'])/len(K.generation_internal_ordering_[db[number]['generation']]) 
                        for number in range(10_000)}

        for number in tqdm(sorted_counts):
            if db[number]['generation'] >= 5:
                continue
            r: float = radii[db[number]['generation']]
             
            make_nodes = code_template_lines[0].format(number=number, theta_coord=new_thetas[number], r_coord=r)
            code.append(make_nodes)

        generational_order = K.generation_internal_ordering_[4] + K.generation_internal_ordering_[3] + K.generation_internal_ordering_[2]
        for number in tqdm(generational_order):
            colors = {1: 'red', 2: 'black', 3: 'green', 4: 'blue'}
            #thicknesses = {4: 0.4, 3: 0.8, 2: 1.6}
            thickness = max(db[number]['weight']/20, 0.4)
            if db[number]['generation'] in [2,3,4]:
                draw_circles = code_template_lines[1].format(**db[number], color=colors[db[number]['generation']])
                draw_rays = code_template_lines[2].format(number=number,
                                                          parent_color=colors[db[db[number]['parent']]['generation']],
                                                          thickness = thickness,
                                                          parent=db[number]['parent'],
                                                          theta=new_thetas[number] + 180,
                                                          parent_theta=new_thetas[db[number]['parent']])
            else:
                continue
            code.append(draw_rays)#, draw_circles])
    return code


write_preamble()
write_body()
write_ending()



