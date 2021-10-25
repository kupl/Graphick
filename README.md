# Graphick

This is the implementation of our OOPLSA'20 paper "Learning Graph-based Heuristics for Pointer Analysis without Handcrafting Application-Specific Features". It aims to reproduce the Table 1, 2, 3, 4 and 6.


We implemented Graphick on top Doop. Specifically, We used Graphick to generate context sensitivity heuristic on the artifact of Scaler which is a baseline graph-based context-sensitivity heuristic developed on Doop (Ctx_Sensitivity folder). We also used Graphick to generate heap abstraction heuristic on the artifact of Mahjong which is a baseline heap abstraction heuristic (Heap_Abstraction folder).

#### Table of Contents

* [Getting-Started Guide](#Getting-Started-Guide)
  * [Requirements](#Requirements)
  * [Setup Instruction](#Setup-Instruction)
  * [Verifying Installation](#Verifying-Installation)
  * [Reproducing the evaluation](#Reproducing-the-evaluation)
* [Artifact](#Artfact)

## Getting-Started Guide

## Requirements

- A 64-bit Ubuntu system
- A Java 8 distribution
- A Python 2.x interpreter

Please set your `JAVA_HOME` environment variable to point to your Java installation directory.

### Setup Instruction

### Installing Datalog Engine

Running Doop Framework requires Datalog engine that computes new facts from initial facts and inference rules given by Doop framework. Please execute the following command in your terminal to make sure your system has one of them.

```
$ bloxbatch -help
```

If you need to install Datalog engine, please visit [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html). The page provides a deb package of an academic version of LogicBlox v3 engine. (We recommend `.deb` package installation)

### Verifying Installation

Verifying installation is very easy. You can check the installation by running the following command:

```
Ctx_Sensitivity$ ./run.py graphick luindex
```

You will see the results as follows:

```
Running graph_ci pointer analysis for luindex ...
...
Pointer analysis START
analysis timne: 23.49
Pointer analysis FINISH
...
logid graph heuristic ...
elapsed timne: 14.46s
...
Running 2obj-Graphick pointer analysis for luindex ...
...
Pointer analysis START
analysis time: 34.94s
Pointer analysis FINISH
...
#may-fail casts           297
#poly calls               682
#call edge                29,045
```

The results say that

- The program to be analyzed is luindex
- This analysis first run context-insensitive analysis to produce a garph to use Graphick and then do the main analysis 2obj-Graphick
- The pre-analysis took 23.49 seconds
- The main analysis took 34.94 seconds
- The results for each client (may-fail casts, poly v-calls, call-graph-edges)


### Reproducing the evaluation

Following the instruction below reproduces Table 1, 2, 3, 4, and 6. The command for running pointer analysis is as follows:

```
./run.py <analysis> <pgm>
```

If your current directory is "Ctx_Sensitivity", <analysis> can be one of the following analyses:

```
graphick, scaler, zipper, data, 2objh, insens, s2objh, graphick_sobj.
```
The above command will reproduce Table 1, 2, or 6. If you are in "Heap_Abstraciton",  <analysis> can be:
```
graphick, mahjong, allos_based, type_based.
```

<pgm> can be a program in our evaluation:
```
luindex, lusearch, antlr, pmd, fop, chart, bloat, pmdm, eclipse, xalan, JPC, checkstyle, findbugs, soot, jython, briss, jedit
  ```
For example, if you want to analyze antlr with Graphick, type:
```
$./run.py graphick antlr
```
 
 
 ## Artfact

VirtualBox Image

We've archived a ready-to-run version of our implementation in zenodo([Link](https://zenodo.org/record/4040341#.X7pZ1a6RWpc)).
