#!/usr/bin/python

from collections import defaultdict
import os, sys, re, subprocess, tempfile, json, pickle, random, time
from heap_merge_strategies import heap_partition
from heap_merge_strategies import strategy_type_allocsite_keyword
from heap_merge_strategies import strategy_partial_allocsite_keyword

ROOT = sys.path[0]
last_analyses = os.path.join(ROOT,'last-analysis')

def db_query(db, query):
    rslt = []
    query = query.replace('$', '\\$')

    with tempfile.TemporaryFile() as fp:
        bloxbatch = subprocess.Popen(['bloxbatch', '-db', db, '-query', query], stdout = fp, stderr = subprocess.PIPE)
        _, stderrdata = bloxbatch.communicate()
        if bloxbatch.returncode != 0:
            print ('Error: {}'.format(bloxbatch.returncode))
            print (stderrdata)
            sys.exit(1)
        else:
            fp.seek(0)
            for line in fp:
                rslt.append(line.strip().split(', '))
    return rslt


if __name__ == '__main__':
    pgm = sys.argv[1]
    types_filename = sys.argv[2]
    print (pgm)
    with open(types_filename, 'r') as f:
        types = [t.strip() for t in f.read().splitlines()]
    #print (types)
    
    obj_type_query = '_[obj]=type<-HeapAllocation:Type[obj]=type,Stats:Simple:InsensVarPointsTo(obj,_).'
    obj_query = '_(obj)<-Stats:Simple:InsensVarPointsTo(obj,_).'
    heap_type_map = {}
    type_heaps_map = defaultdict(set)
    
    #db = os.path.join(last_analyses, pgm)
    db = last_analyses
    answer = db_query(db, obj_type_query)
        
    for item in answer:
        heap_type_map[item[0]] = item[1]
        type_heaps_map[item[1]].add(item[0])
    
    all_heaps = set([item[0] for item in db_query(db, obj_query)])
    typed_heaps = set(heap_type_map.keys())
    untyped_heaps = all_heaps.difference(typed_heaps)
    
    #print 'Untyped heaps: {}'.format(untyped_heaps)

    for heap in untyped_heaps:
        heap_type_map[heap] = heap
        type_heaps_map[heap] = heap


    heap_merge_func = strategy_partial_allocsite_keyword(heap_type_map, types)
    #heap_merge_func = strategy_type_allocsite_keyword(heap_type_map, types)
    filename = heap_partition(heap_type_map.keys(), heap_merge_func, pgm)
