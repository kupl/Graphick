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
MAHJONG_CP = os.path.join(MAHJONG_DIR, 'bin') +\
 ':' + os.path.join(MAHJONG_DIR, 'lib', 'guava-19.0.jar') +\
 ':' + os.path.join(MAHJONG_DIR, 'lib', 'sootclasses.jar')
MAHJONG_OUTPUT_DIR = os.path.join(ROOT, 'output-mahjong')
MAHJONG_MAIN = 'mahjong.main.DoopMain'


APP = [
  'antlr', 'fop', 'luindex', 'pmdm', 'bloat', 'chart',
  'xalan', 'lusearch', 'findbugs', 'JPC', 'findbugs','checkstyle',
   'pmd','eclipse','jedit','briss','soot','jython',
]


DACAPO = ['antlr', 'fop', 'luindex', 'pmdm', 'bloat', 'chart', 'xalan', 'lusearch', 'eclipse','jython']


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

PTA = OrderedDict()
PTA['ci'] = 'context-insensitive'
PTA['2cs'] = '2-call-site-sensitive+heap'
PTA['2type'] = '2-type-sensitive+heap'
PTA['3type'] = '3-type-sensitive+2-heap'
PTA['2obj'] = '2-object-sensitive+heap'
PTA['3obj'] = '3-object-sensitive+2-heap'

UNSCALABLE = {
'2cs':['eclipse'],
'M-2cs':['eclipse'],
'3type':['findbugs', 'eclipse'],
'2obj':['findbugs', 'eclipse'],
'3obj':['bloat', 'chart', 'checkstyle', 'xalan', 'lusearch', 'JPC', 'findbugs', 'eclipse'],
'M-3obj':['bloat', 'chart', 'eclipse'],
}

CLIENT = {
 'Stats:Simple:PotentiallyFailingCast':'mayfailcast',
 'Stats:Simple:PolymorphicCallSite':'polycall',
 'Stats:Simple:AllCallGraphEdge':'calledge',
}

RESET  = '\033[0m'
CYAN   = '\033[36m'
RED    = '\033[91m'
YELLOW = '\033[33m'
WHITE  = '\033[37m'
GREEN  = '\033[32m'
BOLD = '\033[1m'

def runDoop(pta, app):
 if pta.startswith('M-'):
  withMahjong = True
  pta = pta[2:]
 else:
  withMahjong = False
 if pta in PTA.keys():
  analysis = PTA[pta]
 else:
  analysis = pta
 execDoop(analysis, withMahjong, app)

def execDoop(analysis, withMahjong, app):
 appDir = getAppDir(app)
 cmd = './run -jre1.6 -phantom '
 if app == 'pmd':
  cmd += '-refl-log %s ' % os.path.join(appDir, 'pmd-refl.log')
 elif app == 'jython':
  cmd = cmd
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
 
 if app == 'findbugs':
  cmd += '-main edu.umd.cs.findbugs.FindBugs2 '
  cmd += '-app %s ' % os.path.join(appDir, 'coreplugin.jar')
  cmd += '-l %s ' % os.path.join(appDir, 'asm-3.0.jar ')
  cmd += '-l %s ' % os.path.join(appDir, 'asm-commons-3.0.jar ')
  cmd += '-l %s ' % os.path.join(appDir, 'asm-tree-3.0.jar ')
  cmd += '-l %s ' % os.path.join(appDir, 'bcel.jar ')
  cmd += '-l %s ' % os.path.join(appDir, 'dom4j-full.jar ')
 if withMahjong:
  heapabs = os.path.join(MAHJONG_OUTPUT_DIR, app + '-HeapAbstraction.facts')
  if not os.path.isfile(heapabs):
   runMahjong(app)
  cmd += '-heap-abstraction %s ' % heapabs
 cmd += '%s ' % analysis
 if app in DACAPO:
  if app == 'pmdm':
   cmd += os.path.join(appDir, 'pmd.jar')
  else:
   cmd += os.path.join(appDir, app + '.jar')
 else:
  cmd += os.path.join(appDir, CP[app])
 print '==========================================================='
 if withMahjong:
  anaStr = 'Mahjong-Based ' + analysis
 else:
  anaStr = analysis
 anaName = getAnalysisShortName(analysis, withMahjong)
 if anaStr == anaName:
  print 'Running ' + CYAN + BOLD + anaStr + RESET + ' points-to analysis for ' +\
   CYAN + BOLD + app + RESET + ' ...'
 else:
  print 'Running ' + anaStr + ' points-to analysis ' +\
   CYAN + BOLD + '(' + anaName + ')' + RESET + ' for ' +\
   CYAN + BOLD + app + RESET + ' ...'
 print 'cmd: {}'.format(cmd)
 os.system(cmd)
 
 #print 'Writing all detailed client results to %s ...' % DOOP_OUTPUT_DIR
 #if not os.path.exists(DOOP_OUTPUT_DIR):
 # os.makedirs(DOOP_OUTPUT_DIR)
 #writeClientResult(anaName, app, DOOP_LAST_DIR, DOOP_OUTPUT_DIR)
 
 print '==========================================================='
 print
 
def getAppDir(app):
 if app in DACAPO:
  return os.path.join(JARS_DIR, 'dacapo')
 else:
  return os.path.join(JARS_DIR, app)

def getAnalysisShortName(analysis, withMahjong):
 if withMahjong:
  pre = 'M-'
 else:
  pre = ''
 for pta, ana in PTA.items():
  if ana == analysis:
   return pre + pta
 else:
  return pre + analysis

def writeClientResult(anaName, app, dbDir, outputDir):
 for query, name in CLIENT.items():
  outputFile = os.path.join(outputDir, '%s-%s.%s' % (app, anaName, name))
  cmd = 'bloxbatch -db %s -query %s | sort > %s' % (dbDir, query, outputFile)
  #print cmd
  os.system(cmd)

def runMahjong(app):
 # run context-insensitive points-to analysis
 execDoop('context-insensitive', False, app)
 # execute Mahjong to build the new heap abstraction
 print 'Time start' 
 beforeMahjong = datetime.now()
 execMahjong(DOOP_LAST_DIR, DOOP_RESULTS_DIR, app, MAHJONG_OUTPUT_DIR)
 afterMahjong = datetime.now()
 print 'Time End' 
 #print 'Accruate Mahjong: {}'.format(afterMahjong-beforeMahjong) 

def execMahjong(dbPath, cachePath, app, outPath):
 cmd = 'java -Xmx128g -cp %s ' % MAHJONG_CP
 cmd += ' %s' % MAHJONG_MAIN
 cmd += ' -db %s' % dbPath
 cmd += ' -cache %s' % cachePath
 cmd += ' -app %s' % app
 cmd += ' -out %s' % outPath
 
 print 'Running ' + CYAN + BOLD + 'Mahjong' + RESET + ' for ' +\
  CYAN+ BOLD + app + RESET + ' ...'
 if not os.path.exists(outPath):
  os.makedirs(outPath)
 #print cmd + '\n'
 os.system(cmd)
 print

def run(args):
 os.chdir(DOOP_DIR)
 if args[0] == '-all':
  run(['mahjong', '-all'])
  for app in APP:
   for pta in PTA.keys():
    for a in [pta, 'M-' + pta]:
     if not UNSCALABLE.has_key(a) or app not in UNSCALABLE[a]:
      runDoop(a, app)
 elif args[0] == 'mahjong':
  if args[1] == '-all':
   apps = APP
  else:
   apps = args[1:]
  for app in apps:
   runMahjong(app)
 else:
  pta = args[0] # args[0] should be a points-to analysis
  if args[1] == '-all':
   for app in APP:
    if not UNSCALABLE.has_key(pta) or app not in UNSCALABLE[pta]:
     runDoop(pta, app)
  else:
   runDoop(pta, args[1])

if __name__ == '__main__':
 run(sys.argv[1:])
