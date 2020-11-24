from sys import argv
from logdate.logD_lib import random_timetree
from dendropy import Tree

tree = Tree.get_from_path(argv[1],'newick')
sampling_time = argv[2]

random_timetree(tree,sampling_time,1)
