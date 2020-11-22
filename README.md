# Graphick

This is the artifact of our OOPLSA'20 paper "Learning Graph-based Heuristics for Pointer Analysis without Handcrafting Application-Specific Features". It aims to reproduce the Table 1,2,3, and 4.


We implemented Graphick on top Doop. Specifically, We used Graphick to generate context sensitivity heuristic on the artifact of Scaler which is a baseline graph-based context-sensitivity heuristic developed on Doop (Ctx_Sensitivity folder). We also used Graphick to generate heap abstraction heuristic on the artifact of Mahjong which is a baseline heap abstraction heuristic (Heap_Abstraction folder).


## Requirements

- A 64-bit Ubuntu system
- A Java 8 distribution
- A Python 2.x interpreter

Please set your `JAVA_HOME` environment variable to point to your Java installation directory.


### Installing Datalog Engine

To run the pointer analyzer DOOP, you need to install a LogicBlox engine for interpreting the Datalog rules used in DOOP. The download link and installation instructions of PA-Datalog can be found on [this page](http://snf-705535.vm.okeanos.grnet.gr/agreement.html) (We recommend `.deb` package installation).



### Reproducing the evaluation

To reproduce the evaulation results, please follow the manual (manual.pdf).
