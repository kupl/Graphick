#!/usr/bin/env python
import os, sys
from collections import OrderedDict
from datetime import datetime, timedelta


ROOT = sys.path[0] # sys.path[0] is the directory containing this script

DOOP_DIR = os.path.join(ROOT, 'doop')
#DOOP_DIR = 'doop'
DOOP_LAST_DIR = os.path.join(DOOP_DIR, 'last-analysis')
DOOP_RESULTS_DIR = os.path.join(DOOP_DIR, 'results')
DOOP_OUTPUT_DIR = os.path.join(ROOT, 'output-client')
JARS_DIR = os.path.join(DOOP_DIR, 'jars')

MAHJONG_DIR = os.path.join(ROOT, 'mahjong')
#MAHJONG_DIR = 'mahjong' 
#MAHJONG_CP = os.path.join(MAHJONG_DIR, 'bin') +\
# ':' + os.path.join(MAHJONG_DIR, 'lib', 'guava-19.0.jar') +\
# ':' + os.path.join(MAHJONG_DIR, 'lib', 'sootclasses.jar')
#MAHJONG_OUTPUT_DIR = os.path.join(ROOT, 'output-mahjong')
#MAHJONG_MAIN = 'mahjong.main.DoopMain'

APP = [
  'antlr', 'fop', 'luindex', 'pmdm', 'bloat', 'chart',
  'xalan', 'lusearch', 'findbugs', 'JPC', 'findbugs','checkstyle',
   'pmd','eclipse','jedit','briss','soot','jython',
]

DACAPO = ['antlr', 'fop', 'luindex', 'pmdm', 'bloat', 'chart', 'xalan', 'lusearch', 'eclipse',]


CP = {
 'checkstyle':'checkstyle-5.7-all.jar',
 'jedit':'jedit.jar',
 'pmd':'pmd-core-5.3.2.jar',
 'JPC':'JPCApplication.jar',
 'findbugs':'findbugs.jar',
 'soot':'sootclasses-2.3.0.jar',
 'briss':'briss-0.9.jar',
}

MAIN={
 'pmd':'net.sourceforge.pmd.PMD',
 'soot':'soot.Main',
}


#PTA = OrderedDict()
#PTA['ci'] = 'context-insensitive'
#PTA['2cs'] = '2-call-site-sensitive+heap'
#PTA['2type'] = '2-type-sensitive+heap'
#PTA['3type'] = '3-type-sensitive+2-heap'
#PTA['2obj'] = '2-object-sensitive+heap'
#PTA['3obj'] = '3-object-sensitive+2-heap'

#UNSCALABLE = {
#'alloc_based':['bloat', 'chart', 'checkstyle', 'xalan', 'lusearch', 'JPC', 'findbugs', 'eclipse'],
#'mahjong':['bloat', 'chart', 'eclipse'],
#}

def getAppDir(app):
 if app in DACAPO:
  return os.path.join(JARS_DIR, 'dacapo')
 else:
  return os.path.join(JARS_DIR, app)

def getCmd(app,appDir):
  cmd = './run -jre1.6 -phantom '
  if app == 'pmdm':
    cmd += '-refl-log %s ' % os.path.join(appDir, 'pmd-refl.log')

  else:
    cmd += '-refl-log %s ' % os.path.join(appDir, app + '-refl.log')
  if app == 'briss':
    cmd += '-app %s ' % os.path.join(appDir, 'jai-core-1.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'bcmail-jdk15-1.46.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'bctsp-jdk15-1.46.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jai-imageio-1.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'bcprov-jdk15-1.46.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jai-core-1.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'itextpdf-5.2.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jai-codec-1.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jpedal-4.74b27.jar ')
 
  if app == 'soot':
    cmd += '-main soot.Main '
    cmd += '-l %s ' % os.path.join(appDir, 'coffer.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jasminclasses-2.3.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'java_cup.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'JFlex.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'pao.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'polyglot.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'pth.jar ')
 
  if app == 'pmd':
    cmd += '-main net.sourceforge.pmd.PMD '
    cmd += '-app %s ' % os.path.join(appDir, 'pmd-java-5.3.2.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'commons-lang3-3.3.2.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jaxen-1.1.4.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'pmd-core-5.3.2.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'commons-io-2.4.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'javacc-5.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jcommander-1.35.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'pmd-java-5.3.2.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'saxon-9.1.0.8.jar ')

  if app == 'jedit':
    cmd += '-l %s ' % os.path.join(appDir, 'jars/EditBuddy.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jars/PluginManager.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jars/Firewall.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jars/LatestVersion.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'jars/PluginManager.jar ')

  if app == 'findbugs':
    cmd += '-main edu.umd.cs.findbugs.FindBugs2 '
    cmd += '-app %s ' % os.path.join(appDir, 'coreplugin.jar')
    cmd += '-l %s ' % os.path.join(appDir, 'asm-3.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'asm-commons-3.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'asm-tree-3.0.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'bcel.jar ')
    cmd += '-l %s ' % os.path.join(appDir, 'dom4j-full.jar ')
  return cmd



def runPTA(pta,app):
  if pta == 'mahjong':
    cmd = './mahjong.py M-3obj {}'.format(app)
    os.system(cmd)
  elif pta == 'getGraph':
    cmd = './mahjong.py ci {}'.format(app)
    os.system(cmd)
    os.chdir(DOOP_DIR)
    query = 'bloxbatch -db last-analysis -query ReachableHeap | sort > ../{}-Nodes.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query FPG | sort > ../{}-FPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query IncomingFPGEdges | sort > ../{}-IncomingFPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query OutgoingFPGEdges | sort > ../{}-OutgoingFPGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query OAG | sort > ../{}-OAGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query IncomingOAGEdges | sort > ../{}-IncomingOAGEdges.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query OutgoingOAGEdges | sort > ../{}-OutgoingOAGEdges.facts'.format(app)
    os.system(query)

    query = 'bloxbatch -db last-analysis -query HeapMethodModifier | sort > ../{}-MethodModifier.facts'.format(app)
    os.system(query)
    query = 'bloxbatch -db last-analysis -query HeapMethodType | sort > ../{}-IncludingType.facts'.format(app)
    os.system(query)
    
    query = 'bloxbatch -db last-analysis -query ReachableHeapAllocation:Type | sort > ../{}-NodeType.facts'.format(app)
    os.system(query)
  elif pta == 'heuristic':
    cmd = './mahjong.py ci {}'.format(app)
    os.system(cmd)
    cmd = 'python process.py CanHeap.facts > doop/CanHeap.facts'
    os.system(cmd)
    os.chdir(DOOP_DIR)
    heapAbsCmd = 'python types_to_facts.py {} CanHeap.facts'.format(app)
    os.system(heapAbsCmd)
    appDir = getAppDir(app)
    cmd = getCmd(app,appDir)
    cmd += '-heap-abstraction HeapAbstraction.myfacts '.format(app)
    cmd += '3-object-sensitive+2-heap '
    if app in DACAPO:
      cmd += os.path.join(appDir, app + '.jar')
    else:
      cmd += os.path.join(appDir, CP[app])
    print cmd
    os.system(cmd)

  elif pta == 'principle':
    os.chdir(DOOP_DIR)
    appDir = getAppDir(app)
    cmd = getCmd(app,appDir) 
    cmd += '-principle context-insensitive '
    if app in DACAPO:
      cmd += os.path.join(appDir, app + '.jar')
    else:
      cmd += os.path.join(appDir, CP[app])
    os.system(cmd)
    query = 'bloxbatch -db last-analysis -query CandidateHeap | sort > CanHeap.facts'
    os.system(query)
    heapAbsCmd = 'python types_to_facts.py {} CanHeap.facts'.format(app)
    os.system(heapAbsCmd)
        
    cmd = getCmd(app,appDir) 
    cmd += '-heap-abstraction HeapAbstraction.myfacts '.format(app)
    cmd += '3-object-sensitive+2-heap '
    if app in DACAPO:
      cmd += os.path.join(appDir, app + '.jar')
    else:
      cmd += os.path.join(appDir, CP[app])
    os.system(cmd)


  elif pta == 'alloc_based':
    cmd = './mahjong.py 3obj '.format(app)
    os.system(cmd)
  else:
    os.chdir(DOOP_DIR)
    appDir = getAppDir(app)
    cmd = getCmd(app,appDir) 
    cmd_ci = ''
    cmd_ci += cmd
    cmd_ci += '-data context-insensitive '
    if app in DACAPO:
      if app == 'pmdm':
        cmd_ci += os.path.join(appDir, 'pmd.jar')
      else:
        cmd_ci += os.path.join(appDir, app + '.jar')
    else:
      cmd_ci += os.path.join(appDir, CP[app])
    print cmd_ci
    #sys.exit()
    os.system(cmd_ci)
    if pta == 'graphick':
      query = 'bloxbatch -db last-analysis -query CandidateHeap | sort > CanHeap.facts'
      os.system(query)
      heapAbsCmd = 'python types_to_facts.py {} CanHeap.facts'.format(app)
      os.system(heapAbsCmd)
    if pta == 'type_based': 
      heapAbsCmd = 'python types_to_facts.py {} Empty.facts'.format(app)
      os.system(heapAbsCmd)
    cmd += '-heap-abstraction HeapAbstraction.myfacts '.format(app)
    cmd += '3-object-sensitive+2-heap '
    if app in DACAPO:
      cmd += os.path.join(appDir, app + '.jar')
    else:
      cmd += os.path.join(appDir, CP[app])
    os.system(cmd)
    rm_cache = 'rm -r cache/*'
    os.system(rm_cache)
  

def run(args):
 pta = args[0] # args[0] should be a points-to analysis
 if args[1] == '-all':
  for app in APP:
   if not UNSCALABLE.has_key(pta) or app not in UNSCALABLE[pta]:
    runPTA(pta, app)
 else:
  runPTA(pta, args[1])

if __name__ == '__main__':
 run(sys.argv[1:])
