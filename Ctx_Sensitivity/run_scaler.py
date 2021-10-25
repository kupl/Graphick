#!/usr/bin/env python
import os
import shutil
import sys
from datetime import datetime, timedelta

ARTIFACT_ROOT = sys.path[0] # sys.path[0] is the directory containing this script
DOOP_HOME = os.path.join(ARTIFACT_ROOT, 'doop')
sys.path.append(os.path.join(DOOP_HOME, 'scripts'))
from dump_doop import dumpRequiredDoopResults
DOOP_CACHE = os.path.join(DOOP_HOME, 'cache')
DOOP_TEMP = ['out', 'last-analysis', 'tmp']
CLIENT_OUT = os.path.join(ARTIFACT_ROOT, 'output-client')
LAST_ANALYSIS = os.path.join(DOOP_HOME, 'last-analysis')

SCALER_HOME = os.path.join(ARTIFACT_ROOT, 'scaler')
SCALER_OUT = os.path.join(ARTIFACT_ROOT, 'output-scaler') #os.path.join(SCALER_HOME, 'out')
SCALER_CACHE = os.path.join(SCALER_HOME, 'cache')
SCALER_TST=30000000
graphick=False


ANALYSIS={
    'ci':'context-insensitive',
    'graph_ci':'context-insensitive',
    '1type':'1-type-sensitive',
    '2type':'2-type-sensitive+heap',
    's2obj':'selective-2-object-sensitive+heap+Data',
    'original_s2obj':'selective-2-object-sensitive+heap',
    's2obj':'selective-2-object-sensitive+heap',
    '2obj':'2-object-sensitive+heap',
    '2obj-Graphick':'2-object-sensitive+heap+Data',
    's2obj-Graphick':'selective-2-object-sensitive+heap+Data',
    'original_3obj':'3-object-sensitive+2-heap',
    '3obj':'3-object-sensitive+2-heap+Data',
    '2objOOPSLA17':'2-object-sensitive+heap+OOPSLA17',
    'original_2obj':'2-object-sensitive+heap',
    'scaler-pa':'scaler-sensitive+heap',
    'introA':'refA-2-object-sensitive+heap',
    'introB':'refB-2-object-sensitive+heap',
}

CLIENT={
    'Stats:Simple:PotentiallyFailingCast':'mayfailcasts',
    'Stats:Simple:PolymorphicCallSite':'polycalls',
    'Reachable':'reachmethods',
    'Stats:Simple:InsensCallGraphEdge':'calledges',
}

PROGRAM=[
    'luindex', 'lusearch', 'antlr', 'pmd', 'chart', 'eclipse', 'jedit', 'briss', 'soot', 'jython', 'findbugs',
    'pmdm','fop','checkstyle','JPC','bloat','xalan'
]


DACAPO=['chart', 'eclipse', 'jython', 'luindex', 'lusearch', 'antlr', 'pmdm', 'fop', 'bloat', 'xalan']

ALLOW_PHANTOM=['briss', 'eclipse', 'findbugs', 'jedit', 'pmd', 'soot', 'JPC', 'checkstyle']

SCALABLE={
    'jython':'1type', 'soot':'1type',
    'pmd':'2type', 'briss':'2type', 'jedit':'2type', 'eclipse':'2type', 
    'pmd':'2obj', 'briss':'2obj', 'jedit':'2obj', 'eclipse':'2obj', 
    'findbugs':'2obj', 'chart':'2obj', 'luindex':'2obj', 'lusearch':'2obj','antlr':'2obj' 
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


CI_DB={
    'briss':'results/context-insensitive/jre1.6-phantom/briss-0.9.jar',
    'eclipse':'results/context-insensitive/jre1.6-phantom/eclipse.jar',
    'findbugs':'results/context-insensitive/jre1.6-phantom/findbugs.jar',
    'jedit':'results/context-insensitive/jre1.6-phantom/jedit.jar',
    'pmd':'results/context-insensitive/jre1.6-phantom/pmd-core-5.3.2.jar',
    'soot':'results/context-insensitive/jre1.6-phantom/sootclasses-2.3.0.jar',
    'JPC':'results/context-insensitive/jre1.6-phantom/JPCApplication.jar',
    'checkstyle':'results/context-insensitive/jre1.6-phantom/checkstyle-5.7-all.jar',
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

def getCIDB(app):
    if CI_DB.has_key(app):
        db = os.path.join(DOOP_HOME, CI_DB[app])
    else:
        db = os.path.join(DOOP_HOME, 'results/context-insensitive/jre1.6/%s.jar' % app)
    return db

def getPTACommand(app, analysis):
    cmd = './run -jre1.6 --cache --color '
    if analysis == 'graph_ci':
        cmd += '-graph '
    if analysis == '2objOOPSLA17':
        cmd += '-data '
    if app in ALLOW_PHANTOM:
        cmd += '--allow-phantom '
    if TAMIFLEX.has_key(app):
        cmd += '-tamiflex %s ' % TAMIFLEX[app]
    if MAIN.has_key(app):
        cmd += '-main %s ' % MAIN[app]
    cmd += '%s %s ' % (ANALYSIS[analysis], getCP(app))
    cmd += '| tee results/%s-%s.output' % (app, analysis)
    print 'cmd : {}'.format(cmd)
    return cmd

def getScalerPTACommand(app, analysis, scaler_file):
    suffix = '-TST%d' % SCALER_TST
    cmd = './run -jre1.6 --cache --color -scaler %s ' % scaler_file
    if app in ALLOW_PHANTOM:
        cmd += '--allow-phantom '
    if TAMIFLEX.has_key(app):
        cmd += '-tamiflex %s ' % TAMIFLEX[app]
    if MAIN.has_key(app):
        cmd += '-main %s ' % MAIN[app]
    cmd += '%s %s' % (ANALYSIS[analysis], getCP(app))
    cmd += '| tee results/%s-%s%s.output' % (app, analysis, suffix)
    print 'cmd : {}'.format(cmd)
    return cmd

def getScalerCommand(app, cidb):
    cmd = './scaler.sh -db %s ' % cidb
    cmd += '-cache %s -out %s ' % (SCALER_CACHE, SCALER_OUT)
    cmd += '-tst %d ' % SCALER_TST
    cmd += '-app %s ' % app
    # cmd += '| tee %s/%s%s.output' % (SCALER_OUT, app, SCALER_TST)
    scaler_file = os.path.join(SCALER_OUT,
     '%s-ScalerMethodContext-TST%s.facts' % (app, SCALER_TST))
    return cmd, scaler_file

def runDoop(cmd):
    cwd = os.getcwd()
    os.chdir(DOOP_HOME)
    os.system(cmd)
    os.chdir(cwd)

def writeClientResults(app, analysis, dbDir, outputDir):
    print 'Writing all detailed client results to %s ...' % outputDir
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    for query, name in CLIENT.items():
        if analysis == 'scaler-pa':
            analysis += '-TST%d' % SCALER_TST
        outputFile = os.path.join(outputDir, '%s-%s.%s' % (app, analysis, name))
        cmd = 'bloxbatch -db %s -query %s | sort > %s' % (dbDir, query, outputFile)
        os.system(cmd)

def runPTA(app, analysis):
    print 'Running ' + CYAN + BOLD + analysis + ' pointer analysis' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
    cmd = getPTACommand(app, analysis)
    runDoop(cmd)
    #writeClientResults(app, analysis, LAST_ANALYSIS, CLIENT_OUT)

def runScaler(app):
    cidb = getCIDB(app)
    if not os.path.isdir(cidb):
        print 'Running ' + CYAN + BOLD + 'pre-analysis (ci)' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
        cicmd = getPTACommand(app, 'ci')
        runDoop(cicmd)
        #writeClientResults(app, 'ci', LAST_ANALYSIS, CLIENT_OUT)
    print 'Time Start'
    beforeScaler = datetime.now()
    if not os.path.isdir(SCALER_CACHE):
        os.mkdir(SCALER_CACHE)
    dumpRequiredDoopResults(app, 'scaler', cidb, SCALER_CACHE)

    cwd = os.getcwd()
    os.chdir(SCALER_HOME)
    scaler_cmd, scaler_file = getScalerCommand(app, cidb)
    # if os.path.exists(scaler_file):
    #     print 'Scaler results already exist at %s' % scaler_file
    # else:
    #     if not os.path.isdir(SCALER_OUT):
    #         os.mkdir(SCALER_OUT)
    #     # print scaler_cmd
    #     os.system(scaler_cmd)
    if not os.path.isdir(SCALER_OUT):
        os.mkdir(SCALER_OUT)
    # print scaler_cmd
    os.system(scaler_cmd)
    os.chdir(cwd)
    afterScaler = datetime.now()
    print 'Time End'
    print 'Accurate Scaler time: {}'.format(afterScaler - beforeScaler)
    return scaler_file

def runScalerPTA(app, analysis):
    scaler_file = runScaler(app)
    scaler_PTA_cmd = getScalerPTACommand(app, analysis, scaler_file)
    print 'Running ' + CYAN + BOLD + 'Scaler-guided pointer analysis' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
    # print scaler_PTA_cmd
    runDoop(scaler_PTA_cmd)
    #writeClientResults(app, analysis, LAST_ANALYSIS, CLIENT_OUT)

def setTST(tst):
    global SCALER_TST
    if tst[-1] in ['M', 'm']:
        SCALER_TST = int(tst[:-1]) * 1000000
    else:
        SCALER_TST = int(tst)

def clean(clean_all=True):
    def remove(path):
        if os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path, ignore_errors=True)
    
    def cleanDir(path):
        os.system('rm -rf %s/*' % path)

    remove(DOOP_CACHE)
    remove(SCALER_CACHE)
    if clean_all:
        for d in DOOP_TEMP + [SCALER_OUT, CLIENT_OUT]:
            remove(os.path.join(DOOP_HOME, d))
        for d in [os.path.join(DOOP_HOME, 'results')]:
            cleanDir(d)

def runAll(app):
    runPTA(app, 'ci')
    runPTA(app, SCALABLE[app])
    runScalerPTA(app, 'scaler-pa')
    runPTA(app, 'introA')
    if app != 'jython' and app != 'briss':
        runPTA(app, 'introB')

def run(args):
    if args[0] == '-clean':
        clean()
    elif args[0] == '-clean-cache':
        clean(False)
    elif args[0] == '-all' and len(args) == 1:
        for p in PROGRAM:
            runAll(p)
            # clean(False)
    else:
        analysis = args[0]
        app = args[1]
        if len(args) >= 4 and args[2] == '-tst':
            setTST(args[3])
        if analysis == '-all':
            runAll(app)
        elif analysis == 'scaler':
            if app == '-all':
                for p in PROGRAM:
                    runScaler(p)
            else:
                runScaler(app)
        elif analysis == 'scaler-pa':
            runScalerPTA(app, analysis)
        else:
            runPTA(app, analysis)

if __name__ == '__main__':
    run(sys.argv[1:])
