import os, sys
from collections import OrderedDict
from datetime import datetime, timedelta


for i in range(96):
  cmd = 'bloxbatch -db doop/last-analysis -query Feature{} | sort > features/Feature{}-Nodes.facts'.format(i,i)
  os.system(cmd)









