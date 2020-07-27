# Installation

### Using Conda

If you have Anaconda, you can install wLogDate with conda install

``` bash
   conda install -c uym2 wlogdate 
```  

### From source code. 
1. Eeither 
	* clone the repository to your machine 
```bash
   git clone https://github.com/uym2/wLogDate.git
```
	* or simply download [this zip file](https://github.com/uym2/wLogDate/archive/master.zip) to your machine. 
2. To install, go to the wLogDate folder. 
	* If you have ```pip```, use
```bash
   pip install .
```
	* Otherwise, type
``` bash
   python setup.py develop
```

# Usage
wLogDate accepts calibration points (hard constraints on divergence times) for internal nodes, sampling times at leaf nodes, and a mixture of the two. Below we give examples for the three most common use-cases. All examples are given in [use_cases.zip](use_cases.zip) of this repository. If you cloned or downloaded the repository, go to the wLogDate folder and unzip ```use_cases.zip```. If you installed wLogDate using Anaconda, download [use_cases.zip](https://github.com/uym2/wLogDate/edit/master/use_cases.zip) to your machine and unzip it before trying the examples.

## Use case 1: Infer the unit ultrametric tree
If there is no calibrations given, wLogDate will infer the unit (depth 1) ultrametric tree.

``` bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE>
```

We give an example in folder [use_cases/unit_time_tree](use_cases/unit_time_tree), inside which you can find the sampled input tree `input.nwk`.

```bash
   cd use_cases/unit_time_tree
   launch_wLogDate.py -i input.nwk -o output.nwk
```
The output tree ```output.nwk``` is ultrametric and has depth (root-to-tip distance) 1. The relative divergence times of the internal nodes are annotated to the tree inside the square brackets.

## Use case 2: Infer the time tree from phylodynamics data
A typical use-case in virus phylogeny is to infer the time tree from a phylogram inferred from sequences and their sampling times (i.e. calibration points given at leaf nodes). wLogDate reads the calibration points / sampling times from an input file via the `-t` option.

```bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE> -t <SAMPLING_TIMES>
```

### 2.1. Complete sampling times
An example is given in the folder `use_cases/virus_all_samplingTime`, inside which you will find an input tree (`input.nwk`) and the input sampling times (`input.txt`). In this example, we give LogDate all the sampling times for all leaves (i.e. complete sampling times). The file `input.txt` has two columns, which are the species names and the corresponding sampling times.

```bash
   cd use_cases/virus_all_samplingTime
   launch_wLogDate.py -i input.nwk -o output.nwk -t input.txt
```
The output tree ```output.nwk``` has branch lengths in time units and divergence times annotated on every internal nodes.

### 2.2. Partial (missing) sampling times
wLogDate allows missing sampling times for the leaves, as long as there exists at least one pair of leaves with different sampling times. The usage of wLogDate is the same as in the case of complete sampling times. An example is given in the folder `use_cases/virus_some_samplingTime`. Here we give the sampling times for 52 species out of 110 in total.

```bash
   cd use_cases/virus_some_samplingTime/
   launch_wLogDate.py -i input.nwk -o output.nwk -t input.txt
```

### 2.3. Sampling times at internal nodes
wLogDate allows the sampling times to be given in both internal nodes and at leaves. An example is given in the folder `use_cases/virus_internal_smplTime`. In the example tree, each of the nodes (including leaf nodes and internal nodes) has a unique label. If the internal nodes have unique labeling, wLogDate allows the internal calibrations to be specified by their labels such as the leaves.

```bash
   cd use_cases/virus_internal_smplTime
   launch_wLogDate.py -i input.nwk -o output.nwk -t input.txt -k
```
The `-k` flag (or `--keep`) is used to announce wLogDate that the tree has already had unique labeling and to suppress the auto-label of wLogDate.

## Use case 3: Infer the time tree with calibration points given in backward time
For calibration points obtained from fossils, the calibration points are usually specified in backward time such as "million years ago" ("mya"). For your convenience, wLogDate allows specification of backward time via the `-b` flag.

```bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE> -t <CALIBRATIONS> -b
```
Calibration points can be given in the same way as sampling times. If the tree nodes are uniquely labeled, we can use the labels to specify the internal nodes associated with the calibration points. Alternatively, wLogDate allows the identification of a node as the LCA of a set of species and allows optional label assignment to these calibration points. We give an example in `use_cases/fossil_backward_time`.

Because the input tree ```input.nwk``` does not have labels for internal nodes, we need to use LCA to specify calibration points. Here we use 4 calibration points in ```input.txt```. An internal node is identified as the LCA of 2 or more species separated by "+" and its name can be optionally specified using "=". In our example, the 4 calibration points are the LCAs of (t1, t30, t40, and t26), (t27 and t3), (t24 and t37), and (t46, t31, and t48), with two node labels "calib1" and "calib2" assigned to (t1, t30, t40, and t26) and (t24 and t37), respectively. Note that label assignments in ```input.txt``` override both the input tree's labels and automatic labeling of wLogDate.

```bash
   cd use_cases/fossil_backward_time
   launch_wLogDate.py -i input.nwk -t input.txt -o output.nwk -b
```

With the `-b` flag, wLogDate understands the time as backward and enforces each parent node's divergence time to be larger (i.e. "older") than those of its children. The output tree ```output.nwk``` is ultrametric, has branch lengths in time units, and has divergence times annotated onto the internal nodes in backward time. By default, the leaf nodes are set to present time (t = 0). You can adjust the leaf time using the `-f` option. The output tree has internal node labels assigned arbitrarily by wLogDate, except for the two calibration points "calib1" and "calib2" assigned by user via `input.txt`.
