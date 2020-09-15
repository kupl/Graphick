import sys


if __name__ == '__main__':
    candidates = set()
    facts = sys.argv[1]
    
    pre_lines = [line.rstrip('\n') for line in open(facts)]
    for i,val in enumerate(pre_lines):
        candidates.add(val.replace("  ",""))

    f = open(("Oracle.facts"),'w')
    for i, val in enumerate(candidates):
        data = val + '\n'
        f.write(data)
    f.close





