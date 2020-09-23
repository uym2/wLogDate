# About

wLogDate is a method for dating phylogenetic trees. Given a phylogeny and either sampling times for leaves or calibration points for internal nodes, wLogDate outputs a "dated" tree that conforms to the sampling times or calibration points. It can also work with no sampling time or calibration points where it would simply turn the tree into ultrametric, fixing its height to a given value. Its optimization criterion is to minimize the variance of the mutation rates in log scale (hence the term logDate). 

The algorithm is developed by Uyen Mai and Siavash Mirarab. The code is developed by Uyen Mai. 

#### Publication

Mai, Uyen, and Siavash Mirarab. “Log Transformation Improves Dating of Phylogenies.” Molecular Biology and Evolution, in press 2020

* Abstract appeared at RECOMB 2020


#### Contact
Please submit questions and bug reports as [issues](https://github.com/uym2/wLogDate/issues).


# Web-based GUI

A Galaxy-based web server with graphical user interface is available at http://wlogdate.com/

# Installation on your machine
The current latest release is v1.0.1. 

## For Windows users
We release executables for Windows users. The current stable release is v1.0.0, which can be [downloaded here](https://github.com/uym2/wLogDate/releases/download/v1.0.0/wldsetup-1.0.0.exe). Double click the exe file and follow the install wizard to setup wLogDate. 
After installation, restart your computer. Then open the cmd and run ```launch_wLogDate -h``` to see the commandline help of wLogDate.

## For MacOS and Linux users
You can install wLogDate using Anaconda, Pip, or from source code.

### Prerequisites:

You need to have:

* Python >= 3.6
* [Anaconda](https://www.anaconda.com/) would make the installation slightly easier. But [pip](https://pypi.org/project/pip/) (already installed with Python 3 >=3.4) would also work. 

### Install using Conda
First, add `bioconda` and `conda-forge` to your active channels.

```bash
   conda config --add channels conda-forge
   conda config --add channels bioconda
```

Now use `conda install` to install wLogDate

``` bash
   conda install -c uym2 wlogdate 
```  

### Install using Pip
wLogDate is available on the Python Package Index (PyPI). To install, use `pip` as follow

``` bash
   python3 -m pip install wlogdate 
```

### Install from source code
1. Download the source code.  
	* Either clone the repository to your machine 

	```bash
	   git clone https://github.com/uym2/wLogDate.git
	```

	* or simply download [this zip file](https://github.com/uym2/wLogDate/archive/master.zip) to your machine and unzip it in your preferred destination. 
2. To install, go to the wLogDate folder. 
	* If you have ```pip```, use
	```bash
	   python3 -m pip install .
	```
	* Otherwise, type
	``` bash
	   python3 setup.py install
	```
After installation, run:

```bash
launch_wLogDate.py -h
```
to see the commandline help of wLogDate.

# Usage
wLogDate accepts calibration points (hard constraints on divergence times) for internal nodes, sampling times at leaf nodes, and a mixture of the two. Below we give examples for the three most common use-cases. 

* All examples are given in [use_cases.zip](use_cases.zip) of this repository. 
	* If you cloned or downloaded the repository, go to the wLogDate folder and ```unzip use_cases.zip```. 
	* If you installed wLogDate using Anaconda or PyPI, download [use_cases.zip](https://github.com/uym2/wLogDate/edit/master/use_cases.zip) to your machine and unzip it before trying the examples.
	
Note: the examples below assume you are using Linux or MacOS. For Windows users who installed wLogDate using the installation wizard, change ```launch_wLogDate.py``` to ```launch_wLogDate``` in all commands in the examples below.

## Use case 1: Infer the unit ultrametric tree
If there is no calibration given, wLogDate will infer the unit (depth 1) ultrametric tree.

``` bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE>
```

We give an example in folder [use_cases/unit_time_tree](use_cases/unit_time_tree), inside which you can find the sampled input tree `input.nwk`.

```bash
   cd use_cases/unit_time_tree
   launch_wLogDate.py -i input.nwk -o output.nwk
```

The output tree is ```output.nwk```.

* It is an ultrametric tree and has depth (root-to-tip distance) 1.
* The relative divergence times of the internal nodes are annotated on the tree inside the square brackets with attribute `t`, as in, `[t=0.095]`.

## Use case 2: Infer the time tree from phylodynamics data
A typical use-case in virus phylogeny is to infer the time tree from a phylogram inferred from sequences and their sampling times (i.e. calibration points given at leaf nodes). wLogDate reads the calibration points or sampling times from an input file via the `-t` option.

```bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE> -t <SAMPLING_TIMES>
```

### 2.1. Complete sampling times
An example is given in the folder `use_cases/virus_all_samplingTime`. Starting from the base directory,

```bash
   cd use_cases/virus_all_samplingTime
```

Inside this folder you will find an input tree (`input.nwk`) and the input sampling times (`input.txt`).
In this example, we give wLogDate all the sampling times for all leaves (i.e. complete sampling times). 

### Sampling time / calibration time file 

* The sampling time file (`input.txt`) is a tab-delimited file, with one pair of species-time per line
* It must have two columns: the species names and the corresponding sampling times.


 For example, lines

```
000009  9.36668
000010  9.36668
000011  11.3667
000012  11.3667
```
show that leaves `000009` and `000010` are sampled at time 9.36668 while nodes `000011` and `000012` are sampled at time 11.3667. 

**Note:** These times are assumed to be forward; i.e, smaller values mean closer to the root of the tree. The top of the branch above the root is assumed to be 0.

Now, run:

```bash
   cd use_cases/virus_all_samplingTime
   launch_wLogDate.py -i input.nwk -o output.nwk -t input.txt
```
The output tree ```output.nwk``` 

* has branch lengths in time units and 
* divergence times annotated on every internal nodes using the `[t=9.55]` notation.

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
The `-k` flag (or `--keep`) is used to inform wLogDate that the tree already has unique internal node labels and that wLogDate should suppress the auto-labeling of internal nodes.

## Use case 3: Infer the time tree with calibration points given in backward time
For calibration points obtained from fossils, the calibration points are usually specified in backward time such as "million years ago" ("mya"). For these cases, wLogDate allows specification of backward time via the `-b` flag.

```bash
   launch_wLogDate.py -i <INPUT_TREE> -o <OUTPUT_TREE> -t <CALIBRATIONS> -b
```
Calibration points can be given in the same way as sampling times. 

* If the tree nodes are uniquely labeled, we can use the node labels to specify the internal nodes associated with the calibration points. 
* Alternatively, wLogDate allows the identification of a node as the Least Common Ancestor (LCA) of a set of species and allows optional label assignment to these calibration points. You may know LCA by their other name: MRCA. 

We give an example of the LCA specification in `use_cases/fossil_backward_time`. From the base directory, go to this example. 

```bash
   cd use_cases/fossil_backward_time
```

Because the input tree ```input.nwk``` does not have labels for internal nodes, we need to use LCA to specify calibration points. Here we use 4 calibration points in ```input.txt```: 

```
calib1=t1+t30+t40+t26 0.551
t27+t3 0.057
calib2=t24+t37 0.152
t46+t31+t48 2.699
```

An internal node is identified as the LCA of 2 or more species separated by `+`. Moreover, a name for this internal node can be optionally specified using `=`. In our example, the 4 calibration points are the LCAs of `(t1, t30, t40, and t26)`, `(t27 and t3)`, `(t24 and t37)`, and `(t46, t31, and t48)`, with two node labels `calib1` and `calib2` assigned to two of these nodes. Note that label assignments in ```input.txt``` override both the input tree's labels and automatic labeling of wLogDate.

```bash
   launch_wLogDate.py -i input.nwk -t input.txt -o output.nwk -b
```

With the `-b` flag, wLogDate understands the time as backward and enforces each parent node's divergence time to be larger (i.e. "older") than those of its children. 

The output tree ```output.nwk``` is ultrametric, has branch lengths in time units, and has divergence times annotated onto the internal nodes in backward time. 

* By default, the leaf nodes are set to present time (t = 0). You can adjust the leaf time using the `-f` option. 
* The output tree has internal node labels assigned arbitrarily by wLogDate, except for the two calibration points "calib1" and "calib2" assigned by user via `input.txt`.


# Other useful options

The following options are useful to explore:

* `-p 10` (or some other number) can be used to run the optimization problem 10 times instead of the default once, each starting from a different initial point. 
* `-s` can be used to set the seed number, to enable reproducible results. 
* `-l` can be used to set the length of the sequences from which the tree is inferred. Impacts the pseudocount used internally by wLogDate for super short branches.
* `-m` to adjust the maximum number of iterations of the internal optimizer. 
* `-z` to assign a value to zero length branches.
* `-r` and `-f` can be used to set the time at the root and the leaves. 
