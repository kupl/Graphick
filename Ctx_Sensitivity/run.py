#!/usr/bin/env python
import os
import shutil
import sys
from datetime import datetime, timedelta

ARTIFACT_ROOT = sys.path[0] # sys.path[0] is the directory containing this script
DOOP_HOME = os.path.join(ARTIFACT_ROOT, 'doop')
DOOP_CACHE = os.path.join(DOOP_HOME, 'cache')




PROGRAM=[
    'luindex', 'lusearch', 'antlr', 'pmd', 'chart', 'eclipse', 'jedit', 'briss', 'soot', 'jython', 'findbugs',
    'pmdm','fop','checkstyle','JPC','bloat','xalan'
]

DACAPO=['chart', 'eclipse', 'jython', 'luindex', 'lusearch', 'antlr', 'pmdm', 'fop', 'bloat', 'xalan']

ALLOW_PHANTOM=['briss', 'eclipse', 'findbugs', 'jedit', 'pmd', 'soot', 'JPC', 'checkstyle']

UNSCALABLE={
    '2objh':['jython','soot','pmd','briss','jedit','eclipse'],
    'zipper':['jython','soot','pmd','briss','jedit','eclipse'],
    'graphick':['jython','soot'],
    'data':['soot'],
}

MAIN={
    'pmd':'net.sourceforge.pmd.PMD',
    'soot':'soot.Main',
}


CP={
    'briss':'jars/briss/briss-0.9.jar',
    'findbugs':'jars/findbugs/findbugs.jar',
    'jedit':'jars/jedit/jedit.jar',
    'pmd':'jars/pmd/pmd-core-5.3.2.jar',
    'soot':'jars/soot/sootclasses-2.3.0.jar',
    'JPC':'jars/JPC/JPCApplication.jar',
    'checkstyle':'jars/checkstyle/checkstyle-5.7-all.jar',
}



TAMIFLEX={
    'briss':'jars/briss/briss-refl.log',
    'eclipse':'jars/dacapo/eclipse-refl.log',
    'antlr':'jars/dacapo/antlr-refl.log',
    'findbugs':'jars/findbugs/findbugs-refl.log',
    'jedit':'jars/jedit/jedit-refl.log',
    'pmd':'jars/pmd/pmd-refl.log',
    'soot':'jars/soot/soot-refl.log',
    'JPC':'jars/JPC/JPC-refl.log',
    'checkstyle':'jars/checkstyle/checkstyle-refl.log',
}





RESET  = '\033[0m'
CYAN   = '\033[36m'
BOLD = '\033[1m'

def getCP(app):
    if CP.has_key(app):
        return CP[app]
    elif app in DACAPO:
        return 'jars/dacapo/%s.jar' % app
    else:
        raise Exception('Unknown application: %s' % app)



def getZipperCommand(app):
    cmd = './run-zipper.py -jre1.6 --cache --color '
    if app in ALLOW_PHANTOM:
        cmd += '--allow-phantom '
    if TAMIFLEX.has_key(app):
        cmd += '-tamiflex %s ' % TAMIFLEX[app]
    if MAIN.has_key(app):
        cmd += '-main %s ' % MAIN[app]
    cmd += '2-object-sensitive+heap %s ' %  getCP(app)
    return cmd



def runPTA(pta,app):
  if pta == 'insens':
    cmd = './run_scaler.py ci {}'.format(app)
    os.system(cmd) 

  elif pta == 'getGraph':
    cmd = './run_scaler.py ci {}'.format(app)
    os.system(cmd) 
    
    query = 'bloxbatch -db doop/last-analysis -query ReachableHeap | sort > {}-Nodes.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query FPG | sort > {}-FPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query IncomingFPGEdges | sort > {}-IncomingFPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query OutgoingFPGEdges | sort > {}-OutgoingFPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query OAG | sort > {}-OAGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query IncomingOAGEdges | sort > {}-IncomingOAGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query OutgoingOAGEdges | sort > {}-OutgoingOAGEdges.facts'.format(app)
    os.system(query)

    query = 'bloxbatch -db doop/last-analysis -query HeapMethodModifier | sort > {}-MethodModifier.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db doop/last-analysis -query HeapMethodType | sort > {}-IncludingType.facts'.format(app)
    os.system(query)
    
    query = 'bloxbatch -db doop/last-analysis -query ReachableHeapAllocation:Type | sort > {}-NodeType.facts'.format(app)
    os.system(query)


  elif pta == 'heuristic':
    cmd = 'python process.py CanHeap2obj.facts > doop/CanHeap2obj.facts'
    os.system(cmd)
    cmd = 'python process.py CanHeap2type.facts > doop/CanHeap2type.facts'
    os.system(cmd)
    cmd = 'python process.py CanHeap1type.facts > doop/CanHeap1type.facts'
    os.system(cmd)
    cmd = './run_scaler.py 2obj-Graphick {}'.format(app)
    os.system(cmd)

  elif pta == 'scaler':
    cmd = './run_scaler.py scaler-pa {}'.format(app)
    os.system(cmd) 
  elif pta == 'data':
    clean()
    cmd = './run_scaler.py 2objOOPSLA17 {}'.format(app)
    os.system(cmd) 
  elif pta == '2objh':
    cmd = './run_scaler.py 2obj {}'.format(app)
    os.system(cmd) 
  elif pta == 'graphick':
    cmd = './run_scaler.py graph_ci {}'.format(app)
    os.system(cmd) 
    cmd = './query.sh'
    os.system(cmd) 
    cmd = './run_scaler.py 2obj-Graphick {}'.format(app)
    os.system(cmd) 
  elif pta == 'zipper':
    os.chdir(DOOP_HOME)
    cmd = getZipperCommand(app)
    os.system(cmd) 
    
def clean():
  cmd = './run_scaler.py -clean'
  os.system(cmd)
 


def run(args):
  start = datetime.now()
  pta = args[0]
  if args[0] == '-clean':
    clean()
  elif args[1] == '-all':
    for app in PROGRAM:
      if not UNSCALABLE.has_key(pta) or app not in UNSCALABLE[pta]:
        runPTA(pta, app)
        clean()
  else:
    runPTA(pta,args[1])
  end = datetime.now()
  print 'taken time: {}'.format(end-start)

if __name__ == '__main__':
    run(sys.argv[1:])
