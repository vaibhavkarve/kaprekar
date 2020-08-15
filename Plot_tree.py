#!/usr/bin/env python
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from Kaprekar import k_star, make_tree
from anytree import Node, RenderTree
from pickle import load, dump

#root = make_tree()
#dump(root, open('Tree2.p', 'wb'))
root = load(open('Tree2.p', 'rb'))

def scores(root) -> Dict[int, int]:
    score = {i: 0 for i in range(10000)}
    for i in root.descendants:
        score[i.name] = len(i.descendants)
    return score

score = scores(root)
#print(sorted(score.items(), key=lambda kv: kv[1], reverse=True)[0:200])
#print(score[8532])
print([(i, score[i.name]) for i in root.children[1].children])

#def coordinates(root) -> Dict[int, Tuple[int, int, int]]:
#    score : Dict[int, int] = scores(root)
#    for i in range
