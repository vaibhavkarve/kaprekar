#!/usr/bin/env python
from typing import List, Dict, Tuple, Iterable, Callable, IO
from collections import defaultdict
#from anytree import Node, RenderTree
import csv
from time import time
import pickle
from tqdm import tqdm

SCALE: float = 1/100*3
WEIGHT_SCALE: float = 1/100*2


def number_to_digits(n: int, length=4) -> List[int]:
    digit_list: List[int] = [int(digit) for digit in str(n)]
    return digit_list + [0]*(length - len(digit_list))

def digits_to_number(digit_list: Iterable[int]) -> int:
    return int(''.join(str(digit) for digit in digit_list))

def k(n: int, length=4) -> int: # parent
    sorted_digits: List[int] = sorted(number_to_digits(n, length=length))
    ascending_number: int = digits_to_number(sorted_digits)
    descending_number: int = digits_to_number(reversed(sorted_digits))
    return descending_number - ascending_number

parent: Callable[[int], int] = k # Just an alias

def k_path(n: int) -> List[int]: # Ancestors
    seen_numbers: List[int] = [n]
    next_number: int = k(n)
    while next_number not in seen_numbers:
        seen_numbers.append(next_number)
        next_number = k(next_number)
    return seen_numbers

def calculate_weights() -> Dict[int, int]:
    # Each k_path contributes unity to the weight for each member of the path.
    counts_dict : Dict[int, int] = defaultdict(int)
    for source in range(10_000):
        for member in k_path(source):
            counts_dict[member] += 1
    return counts_dict

def descendants(counts_dict: Dict[int, int] = calculate_weights()) -> Dict[int, int]:
    sorted_counts = sorted(counts_dict.keys(), key=counts_dict.get, reverse = True)
    descendants_: Dict[int, List[int]] = defaultdict(list)
    for number in sorted_counts:
        descendants_[parent(number)].append(number)
    return descendants_
    

def generation(number: int) -> int:
    return len(k_path(number))

def generation_internal_ordering() -> Dict[int, List[int]]:
    # TODO: I am not sure why this matters!
    generation_members: Dict[int, List[int]] = defaultdict(list)
    for number in range(10_000):
        generation_members[generation(number)].append(number)
    return generation_members

generation_internal_ordering_: Dict[int, List[int]]
generation_internal_ordering_ = generation_internal_ordering()

def index_within_generation(number: int) -> int:
    # TODO: I am not sure why this number matters!
    return generation_internal_ordering_[generation(number)].index(number)


def r_coord(number: int, counts_dict: Dict[int, int] = calculate_weights()) -> float:
    # Relative to parent node
    if generation(number) == 1:
        absolute_positions: List[float] = {0: 0, 6174: 25_000} # Where should 0 and 6174 be placed?
        return absolute_positions[number]*SCALE
    
    separation: float = counts_dict[number]
    radius: float = counts_dict[number] + counts_dict[parent(number)] + separation
    return radius*SCALE


def theta_coord(number: int, descendants_: Dict[int, List[int]] = descendants()) -> float:
    # Relative to parent node
    if generation(number) == 1:
        return 0
    siblings: List[int] = descendants_[parent(number)]
    if descendants_[number]:
        siblings = list(filter(lambda x: descendants_[x], siblings))
        siblings = list(filter(lambda x: generation(x) != 1, siblings))
    else:
        siblings = list(filter(lambda x: not descendants_[x], siblings))
    angle: float = theta_coord(parent(number), descendants_) + 360*siblings.index(number)/len(siblings)
    return angle % 360

def create_csv_database() -> None:
    counts_dict: Dict[int, int] = calculate_weights()
    descendants_: Dict[int, List[int]] = descendants()
    def weight(number: int) -> float:
        return counts_dict[number]*WEIGHT_SCALE

    db: IO[str]
    with open('database.csv', 'w', newline='') as db:
        dbwriter = csv.writer(db, delimiter=',')
        sorted_counts = sorted(counts_dict.keys(), key=counts_dict.get, reverse = True)
        dbwriter.writerow(['number',
                           'generation',
                           'index_within_generation',
                           'parent',
                           'r_coord',
                           'theta_coord',
                           'weight'])
        for number in tqdm(sorted_counts):
            dbwriter.writerow([number,
                               generation(number),
                               index_within_generation(number),
                               parent(number),
                               r_coord(number, counts_dict),
                               theta_coord(number, descendants_),
                               weight(number)])
            print(number)
    return None

def pickle_database() -> None:
    counts_dict: Dict[int, int] = calculate_weights()
    descendants_: Dict[int, List[int]] = descendants()
    def weight(number: int) -> float:
        return counts_dict[number]*WEIGHT_SCALE

    database_dictionary = {}
    fields = ['number', 'generation', 'index_within_generation',
              'parent', 'r_coord', 'theta_coord', 'weight']
    for number in tqdm(range(10_000)):
        database_dictionary[number] = dict(zip(fields, [number,
                                       generation(number),
                                       index_within_generation(number),
                                       parent(number),
                                       r_coord(number, counts_dict),
                                       theta_coord(number, descendants_),
                                       weight(number)]))
    with open('database.pickle', 'wb') as picklefile:
        pickle.dump(database_dictionary, picklefile, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    pickle_database()

#create_csv_database()
'''
def make_tree():
    seen = {}
    table1 : Iterator[List[int]] = map(k_star, range(10000))
    table2 : List[List[int]]     = [i[::-1] for i in table1]
    
    root = Node('root')
    for row in table2:
        parent = root
        for entry in row:
            if entry in seen:
                parent = seen[entry]
            else:
                parent = Node(entry, parent = parent)
                seen[entry] = parent
    return root


#root = make_tree()
#with open('Tree.txt', 'w') as writefile:
#    for pre, fill, node in RenderTree(root):
#        writefile.write("%s%s\n" % (pre, node.name))
'''
'''
for i in range(0, 10000):    
    if k_star(i)[-1] != 6174:
        print(i, k_star(i))
'''


'''G = nx.Graph()
for n in range(0, 10000):
    for v in k_star(n)[1:]:
        G.add_edge(n, v)
    print(n)
nx.draw(G)
plt.show()

def write_radii_to_file(maximum: int = 10000):
    counts = calculate_counts(maximum)
    with open('Radii.p', 'w') as writefile:
        for i in counts:
            if i[1]>1:
                writefile.write('{0} {1}\n'.format(i[0], i[1]))



'''