#!/usr/bin/env python
import os
import shutil
import sys

ARTIFACT_ROOT = sys.path[0] # sys.path[0] is the directory containing this script
DOOP_HOME = os.path.join(ARTIFACT_ROOT, 'doop')
sys.path.append(os.path.join(DOOP_HOME, 'scripts'))
from dump_doop import dumpRequiredDoopResults
DOOP_CACHE = os.path.join(DOOP_HOME, 'cache')
DOOP_RESULTS = os.path.join(DOOP_HOME, 'results')
DOOP_TEMP = ['out', 'last-analysis', 'tmp']
CLIENT_OUT = os.path.join(ARTIFACT_ROOT, 'output-client')
LAST_ANALYSIS = os.path.join(DOOP_HOME, 'last-analysis')

ZIPPER_HOME = os.path.join(ARTIFACT_ROOT, 'zipper')
ZIPPER_OUT = os.path.join(ARTIFACT_ROOT, 'output-zipper') #os.path.join(ZIPPER_HOME, 'out')
ZIPPER_CACHE = os.path.join(ZIPPER_HOME, 'cache')
ZIPPER_MODIFIED = False
ZIPPER_MODIFIED_SUFFIX = '-modified'

ANALYSIS={
    'ci':'context-insensitive',
    'introA-2obj':'refA-2-object-sensitive+heap',
    'introB-2obj':'refB-2-object-sensitive+heap',
    '2obj':'2-object-sensitive+heap',
    'introA-2type':'refA-2-type-sensitive+heap',
    'introB-2type':'refB-2-type-sensitive+heap',
    '2type':'2-type-sensitive+heap',
}

CLIENT={
    'Stats:Simple:PotentiallyFailingCast':'mayfailcasts',
    'Stats:Simple:PolymorphicCallSite':'polycalls',
    'Reachable':'reachmethods',
    'Stats:Simple:InsensCallGraphEdge':'calledges',
}

PROGRAM=[
    'jython', 'soot', 'pmd', 'briss', 'jedit',
    'eclipse', 'findbugs', 'luindex', 'lusearch','chart',
    #'batik', 'checkstyle', 'sunflow', 'findbugs', 'jpc',
    #'eclipse', 'chart', 'fop', 'xalan', 'bloat',
]

DACAPO=['chart', 'eclipse', 'jython', 'luindex', 'lusearch']

ALLOW_PHANTOM=['briss', 'eclipse', 'findbugs', 'jedit', 'pmd', 'soot']

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
}


TAMIFLEX={
    'briss':'jars/briss/briss-refl.log',
    'eclipse':'jars/dacapo/eclipse-refl.log',
    'findbugs':'jars/findbugs/findbugs-refl.log',
    'jedit':'jars/jedit/jedit-refl.log',
    'pmd':'jars/pmd/pmd-refl.log',
    'soot':'jars/soot/soot-refl.log',
}

CI_DB={
    'briss':'results/context-insensitive/jre1.6-phantom/briss-0.9.jar',
    'eclipse':'results/context-insensitive/jre1.6-phantom/eclipse.jar',
    'findbugs':'results/context-insensitive/jre1.6-phantom/findbugs.jar',
    'jedit':'results/context-insensitive/jre1.6-phantom/jedit.jar',
    'pmd':'results/context-insensitive/jre1.6-phantom/pmd-core-5.3.2.jar',
    'soot':'results/context-insensitive/jre1.6-phantom/sootclasses-2.3.0.jar',
}

FLOWS=[ 'Direct', 'Direct+Wrapped', 'Direct+Unwrapped', 'Direct+Wrapped+Unwrapped' ]

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
    if app in DACAPO:
        db = os.path.join(DOOP_HOME, 'results/context-insensitive/jre1.6/%s.jar' % app)
    else:
        db = os.path.join(DOOP_HOME, CI_DB[app])
    return db

def getPTACommand(app, analysis):
    cmd = './run -jre1.6 --cache --color '
    if app in ALLOW_PHANTOM:
        cmd += '--allow-phantom '
    #if app not in DACAPO:
    #    cmd += '--allow-phantom '
    if TAMIFLEX.has_key(app):
        cmd += '-tamiflex %s ' % TAMIFLEX[app]
    if MAIN.has_key(app):
        cmd += '-main %s ' % MAIN[app]
    cmd += '%s %s ' % (ANALYSIS[analysis], getCP(app))
    cmd += '| tee results/%s-%s.output' % (app, analysis)
    return cmd

def runPTA(app, analysis):
    print 'Running ' + CYAN + BOLD + analysis + ' pointer analysis' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
    cmd = getPTACommand(app, analysis)
    runDoop(cmd)
    writeClientResults(app, analysis, LAST_ANALYSIS, CLIENT_OUT)

def runDoop(cmd):
    cwd = os.getcwd()
    os.chdir(DOOP_HOME)
    if not os.path.isdir(DOOP_RESULTS):
        os.mkdir(DOOP_RESULTS)
    os.system(cmd)
    os.chdir(cwd)

def getZipperCommand(app, cidb, zipper_flows=None):
    suffix = ''
    cmd = './zipper.sh -db %s ' % cidb
    cmd += '-cache %s -out %s ' % (ZIPPER_CACHE, ZIPPER_OUT)
    cmd += '-app %s ' % app
    if ZIPPER_MODIFIED:
        cmd += '-express '
        suffix = ZIPPER_MODIFIED_SUFFIX
    if zipper_flows is not None:
        cmd += '-flow %s ' % zipper_flows
        suffix += '-' + zipper_flows
    # cmd += '| tee %s/%s%s.output' % (ZIPPER_OUT, app, suffix)
    # cmd += '> %s/%s%s.output' % (ZIPPER_OUT, app, suffix)
    zipper_file = os.path.join(ZIPPER_OUT,
     '%s-ZipperPrecisionCriticalMethod%s.facts' % (app, suffix))
    return cmd, zipper_file

def getZipperPTACommand(app, analysis, zipper_file, zipper_flows=None):
    suffix = ''
    if ZIPPER_MODIFIED:
        suffix = ZIPPER_MODIFIED_SUFFIX
    if zipper_flows is not None:
        suffix += '-' + zipper_flows
    cmd = './run -jre1.6 --cache --color -zipper %s ' % zipper_file
    if app in ALLOW_PHANTOM:
        cmd += '--allow-phantom '
    #if app not in DACAPO:
    #    cmd += '--allow-phantom '
    if TAMIFLEX.has_key(app):
        cmd += '-tamiflex %s ' % TAMIFLEX[app]
    if MAIN.has_key(app):
        cmd += '-main %s ' % MAIN[app]
    cmd += '%s %s ' % (ANALYSIS[analysis], getCP(app))
    cmd += '| tee results/%s-zipper-%s%s.output' % (app, analysis, suffix)
    return cmd

def runZipper(app, zipper_flows=None):
    cidb = getCIDB(app)
    if not os.path.isdir(cidb):
        print 'Running ' + CYAN + BOLD + 'pre-analysis (ci)' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
        cicmd = getPTACommand(app, 'ci')
        runDoop(cicmd)
        writeClientResults(app, 'ci', LAST_ANALYSIS, CLIENT_OUT)
    else:
        print 'Using cached pre-analysis results ...'
    if not os.path.isdir(ZIPPER_CACHE):
        os.mkdir(ZIPPER_CACHE)
    dumpRequiredDoopResults(app, 'zipper', cidb, ZIPPER_CACHE)

    cwd = os.getcwd()
    os.chdir(ZIPPER_HOME)
    zipper_cmd, zipper_file = getZipperCommand(app, cidb, zipper_flows)
    if not os.path.isdir(ZIPPER_OUT):
        os.mkdir(ZIPPER_OUT)
    # print zipper_cmd
    os.system(zipper_cmd)
    os.chdir(cwd)
    return zipper_file

def runZipperPTA(app, analysis, zipper_flows=None):
    global ZIPPER_MODIFIED
    origin = ZIPPER_MODIFIED
    if analysis[-1] == '*':
        ZIPPER_MODIFIED = True
        pta = analysis[:-1].split('-')[1]
    else:
        pta = analysis.split('-')[1]
    zipper_file = runZipper(app, zipper_flows)
    zipper_PTA_cmd = getZipperPTACommand(app, pta, zipper_file, zipper_flows)
    print 'Running ' + CYAN + BOLD + 'Zipper-guided pointer analysis' + RESET +\
        ' for ' + CYAN + BOLD + app + RESET + ' ...'
    # print zipper_PTA_cmd
    runDoop(zipper_PTA_cmd)
    writeClientResults(app, analysis, LAST_ANALYSIS, CLIENT_OUT, zipper_flows)
    # recover ZIPPER_MODIFIED
    ZIPPER_MODIFIED = origin

def writeClientResults(app, analysis, dbDir, outputDir, zipper_flows=None):
    print 'Writing all detailed client results to %s ...' % outputDir
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if zipper_flows is not None:
        analysis += '-%s' % zipper_flows
    analysis = analysis.replace('*', ZIPPER_MODIFIED_SUFFIX)
    for query, name in CLIENT.items():
        outputFile = os.path.join(outputDir, '%s-%s.%s' % (app, analysis, name))
        cmd = 'bloxbatch -db %s -query %s | sort > %s' % (dbDir, query, outputFile)
        os.system(cmd)

def runAllPTA(app):
    runPTA(app, 'ci')
    runPTA(app, '2obj')
    runZipperPTA(app, 'zipper-2obj')
    runPTA(app, 'introA-2obj')
    runPTA(app, 'introB-2obj')
    if app == 'bloat':
        runZipperPTA(app, 'zipper-2obj*')

def runAllFlows(app, analysis, run_default=True):
    if app != 'batik':
        runZipperPTA(app, analysis, 'Direct')
    runZipperPTA(app, analysis, 'Direct+Wrapped')
    if app != 'batik':
        runZipperPTA(app, analysis, 'Direct+Unwrapped')
    if run_default:
        runZipperPTA(app, analysis, 'Direct+Wrapped+Unwrapped')

def runAppendixAllPTA(app):
    runPTA(app, 'ci')
    runPTA(app, '2type')
    runZipperPTA(app, 'zipper-2type')
    runPTA(app, 'introA-2type')
    runPTA(app, 'introB-2type')

def clean(clean_all=True):
    def remove(path):
        if os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path, ignore_errors=True)

    remove(DOOP_CACHE)
    remove(ZIPPER_CACHE)
    if clean_all:
        for d in DOOP_TEMP + [DOOP_RESULTS, CLIENT_OUT, ZIPPER_OUT]:
            remove(os.path.join(DOOP_HOME, d))

def run(args):
    if args[0] == '-clean':
        clean()
    elif args[0] == '-clean-cache':
        clean(False)
    elif args[0] == '-all' and len(args) == 1:
        for p in PROGRAM:
            runAllPTA(p)
            runAllFlows(p, 'zipper-2obj', False)
            # clean(False)
    elif args[0] == '-appendix':
        for p in PROGRAM:
            runAppendixAllPTA(p)
    else:
        analysis = args[0]
        app = args[1]
        if len(args) >= 4 and args[2] == '-flow':
            if args[3] not in FLOWS and args[3] != '-all':
                raise Exception('Unknown -flow argument: %s' % args[3])
            zipper_flows = args[3]
        else:
            zipper_flows = None
        if analysis == '-all':
            runAllPTA(app)
        elif analysis.startswith('zipper-'):
            if zipper_flows == '-all':
                runAllFlows(app, analysis)
            else:
                runZipperPTA(app, analysis, zipper_flows)
        elif analysis == 'zipper':
            if zipper_flows == '-all':
                for flow in FLOWS:
                    runZipper(app, flow)
            else:
                runZipper(app, zipper_flows)
        else:
            runPTA(app, analysis)

if __name__ == '__main__':
    run(sys.argv[1:])
