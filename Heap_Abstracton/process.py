#!/usr/bin/python
import sys


if __name__ == "__main__":
  fileName = sys.argv[1]


  with open(fileName, 'r') as f:
    data = [s.strip().split('  ') for s in f.read().splitlines()]

  invMth = {}
  data2 = [item[0] for item in data]
  data2.sort()

  for item in data2:
    print (item)


