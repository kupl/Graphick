import os

def heap_partition(heaps, merge_func, jar):
  merged_heaps = set([])
  #heapabstraction_filename = os.path.abspath(jar + '-HeapAbstraction.myfacts')  
  heapabstraction_filename = os.path.abspath('HeapAbstraction.myfacts')
  with open(heapabstraction_filename, 'w') as f:
      for heap in heaps:
          mergedHeap = merge_func[heap]
          merged_heaps.add(mergedHeap)
          f.write(heap + '\t' + mergedHeap + '\n')
  print ('Total merged heaps: {}'.format(len(merged_heaps)))
  print ('{} is written.'.format(heapabstraction_filename))
  return heapabstraction_filename

  
def strategy_type(obj_type_map):
  print ('Strategy: type')
  type_objset_map = {}
  for item in obj_type_map.keys():
      typ = obj_type_map[item]
      if typ in type_objset_map:
          type_objset_map[typ].append(item)
      else:
          type_objset_map[typ] = [item]
  print ('Total types: {}'.format(len(type_objset_map.keys())))
  
  rst = {}
  for obj in obj_type_map.keys():
    rst[obj] = type_objset_map[obj_type_map[obj]][0]
  return rst


def strategy_allocsite_type_keyword(obj_type_map, keywords):
    print ('Default: allocsite, keywords: type, keywords: {}'.format(keywords))

    keytype_rep_map = {}
    rst = {}

    for obj in obj_type_map.keys():
        if obj_type_map[obj] in keywords:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
        else:
            rst[obj] = obj
    return rst

def strategy_partial_allocsite_keyword(obj_type_map, keywords):
    print ('allocsites : {}'.format(len(keywords)))

    keytype_rep_map = {}
    rst = {}

    for obj in obj_type_map.keys():
        if obj in keywords:
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
    return rst


def strategy_type_allocsite_keyword(obj_type_map, keywords):
    print ('Default: type, keywords: allocsite, keywords: {}'.format(len(keywords)))

    keytype_rep_map = {}
    rst = {}

    for obj in obj_type_map.keys():
        if obj_type_map[obj] in keywords:
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
    return rst


def strategy_type_allocsite_keyword_new(obj_type_map, type_objs_map, keywords):
    def get_rep_of_type(typ):
        objs = list(type_objs_map[typ])
        if len(objs) == 1:
            rep = objs[0]
        else:
            _objs = [obj for obj in objs if not(obj.startswith('<reflective') and not(obj.startswith('<reified')))]
            if len(_objs) == 0:
                rep = 'self'
            else:
                rep = _objs[0]
        return rep
    
    print ('NEW Default: type, keywords: allocsite, keywords: {}'.format(len(keywords)))


def strategy_type_allocsite_keyword_exception2(obj_type_map, keywords, exception):
    print ('Default: type, keywords: allocsite, keywords: {}, exceptions: {}'.format(len(keywords), exception))

    keytype_rep_map = {}
    rst = {}
    
    _keywords = keywords.union(set([exception]))
    
    for obj in obj_type_map.keys():
        #if obj_type_map[obj] in keywords or obj in exceptions:
        if obj_type_map[obj] in _keywords:
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
            
    return rst


def strategy_type_allocsite_keyword_exception(obj_type_map, keywords, exceptions):
    print ('Default: type, keywords: allocsite, keywords: {}, exceptions: {}'.format(len(keywords), exceptions))

    keytype_rep_map = {}
    rst = {}

    for typ in type_objs_map.keys():
        keytype_rep_map[typ] = get_rep_of_type(typ)

    for obj in obj_type_map.keys():
        if obj_type_map[obj] in keywords:
            rst[obj] = obj
        else:
            if obj.startswith('<reified') or obj.startswith('<reflective'):
                rst[obj] = obj
            else:
                rep = keytype_rep_map[obj_type_map[obj]]
                if rep != 'self':
                    rst[obj] = rep
                else:
                    rst[obj] = obj
    sum_of_exceptions = reduce(lambda s1, s2: s1.union(s2), exceptions)

    for obj in obj_type_map.keys():
        if obj in sum_of_exceptions:
            continue
        #if obj_type_map[obj] in keywords or obj in exceptions:
        if obj_type_map[obj] in keywords:
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
    
    for exc in exceptions:
        for obj in exc:
            rst[obj] = list(exc)[0]
    return rst


def strategy_type_allocsite_keyheap(obj_type_map, keyheaps):
    print ('Default: type, keywords: allocsite, keyheaps: {}'.format(len(keyheaps)))

    keytype_rep_map = {}
    rst = {}

    for obj in obj_type_map.keys():
        if obj in keyheaps:
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
    return rst


def strategy_type_allocsite_keyword_mahjong (jar, obj_type_map, keywords):
    print ('Default: type, keywords: allocsite. Apply mahjong if necessary')
    print (keywords)
    
    mahjong_map = {}
    with open('{}-HeapAbstraction.facts'.format(jar), 'r') as f:
        lines = [s.strip().split('\t') for s in f.read().splitlines()]
        for line in lines:
            mahjong_map[line[0]] = line[1]

    type_reps_map = {}
    for obj in mahjong_map.keys():
        type_of_obj = obj_type_map[obj]
        if type_of_obj not in type_reps_map.keys():
            type_reps_map[type_of_obj] = set([mahjong_map[obj]])
        else:
            type_reps_map[type_of_obj].add(mahjong_map[obj])

    mahjong_worthy_types = [typ for typ in type_reps_map.keys() if (len(type_reps_map[typ]) > 1) and (typ in keywords)]
    print ('Mahjong-worthy types: {}'.format(mahjong_worthy_types))

    keytype_rep_map = {}
    rst = {}

    for obj in obj_type_map.keys():
        if (obj_type_map[obj] in keywords) and (obj_type_map[obj] in mahjong_worthy_types):
            rst[obj] = mahjong_map[obj]
        elif (obj_type_map[obj] in keywords) and (obj_type_map[obj] not in mahjong_worthy_types):
            rst[obj] = obj
        else:
            if obj_type_map[obj] not in keytype_rep_map.keys():
                keytype_rep_map[obj_type_map[obj]] = obj
            rst[obj] = keytype_rep_map[obj_type_map[obj]]
    return rst


def strategy_mahjong_type_keyword (jar, obj_type_map, keywords, print_types=True):
    if print_types:
        print ('Default: mahjong, Keyword: type, keywords({}): {}'.format(len(keywords), list(keywords)[:10]))
    else:
        print ('Default: mahjong, Keyword: type, keywords: {}'.format(len(keywords)))
    # keywords = ['java.lang.Class']
    # keywords = ['java.lang.StringBuilder', 'java.lang.StringBuffer', 'char[]', 'java.lang.Character$UnicodeBlock', 'java.io.File', 'java.io.BufferedInputStream']
    mahjong_map = {}
    with open('{}-HeapAbstraction.facts'.format(jar), 'r') as f:
        lines = [s.strip().split('\t') for s in f.read().splitlines()]
        for line in lines:
            mahjong_map[line[0]] = line[1]
    print ('mahjong objs: {}'.format(len(mahjong_map.keys())))
    mahjong_key = set(mahjong_map.keys())
    obj_type_map_key = set(obj_type_map.keys())
    print (mahjong_key.difference(obj_type_map_key))
    
    keytype_rep_map = {}
    rst = {}
    
    for obj in mahjong_map.keys():
        try:
            type_of_obj = obj_type_map[obj]
            if type_of_obj in keywords:
                if type_of_obj not in keytype_rep_map.keys():
                    keytype_rep_map[type_of_obj] = obj
                rst[obj] = keytype_rep_map[type_of_obj]
            else:
                rst[obj] = mahjong_map[obj]
        except KeyError as e:
            rst[obj] = mahjong_map[obj]
    
    return rst


def strategy_mahjong_except(jar, obj_type_map, keywords):
    print ('Strategy: mahjong except: {}'.format(keywords))
    mahjong_map = {}
    with open('{}-HeapAbstraction.facts'.format(jar), 'r') as f:
        lines = [s.strip().split('\t') for s in f.read().splitlines()]
        for line in lines:
            mahjong_map[line[0]] = line[1]
    print ('mahjong objs: {}'.format(len(mahjong_map.keys())))
    mahjong_key = set(mahjong_map.keys())
    obj_type_map_key = set(obj_type_map.keys())
    print (mahjong_key.difference(obj_type_map_key))
    
    keytype_rep_map = {}
    rst = {}
    
    for obj in mahjong_map.keys():
        try:
            type_of_obj = obj_type_map[obj]
            if type_of_obj in keywords:
                rst[obj] = obj
            else:
                rst[obj] = mahjong_map[obj]
        except KeyError as e:
            rst[obj] = mahjong_map[obj]
    
    return rst


def strategy_clinit(type_heaps_map):
  print ('Strategy: clinit')
  rst = {}
  for typ in type_heaps_map.keys():
    same_type_heaps = type_heaps_map[typ]
    rep = ''
    for heap in same_type_heaps:
      if 'clinit' in heap:
        if rep == '':
          rep = heap
        rst[heap] = rep
      else:
        rst[heap] = heap
  
  return rst

def strategy_keywords(type_heaps_map):
  # keywords = ['clinit', 'byte[]']
  # keywords = ['clinit', 'java.lang.String']
  # keywords = ['clinit', 'java.lang.StringBuilder', 'char[]', 'int[]', '<class', 'java.lang.Object[]/']
  # keywords = ['clinit', 'java.lang.StringBuilder', 'char[]', 'int[]']
  # keywords = ['clinit', 'java.lang.StringBuilder', 'char[]', 'int[]', 'getContents', 'java.lang.StringBuffer', 'byte[]', '$UnicodeBlock/', 'java.io.File', 'java.lang.String', 'long[]']
  keywords = ['clinit', 'java.lang.StringBuilder']
  print ('Strategy: Keywords OR')
  print ('Keywords: '),
  print (keywords)
  # keywords = ['clinit', 'java.lang.String']
  rst = {}

  for typ in type_heaps_map.keys():
    
    keyword_reps = {}
    same_type_heaps = type_heaps_map[typ]
    if 'java.lang.Class' == typ:
      for heap in same_type_heaps:
        rst[heap] = '<class java.security.cert.CertPathValidatorException>'
      continue

    for heap in same_type_heaps:
      is_found = -1
      for keyword in keywords:
        if keyword in heap:
          is_found = keywords.index(keyword)
          break
      
      if is_found == -1:
        rst[heap] = heap
      else:
        if keywords[is_found] not in keyword_reps.keys():
          keyword_reps[keywords[is_found]] = heap
        rst[heap] = keyword_reps[keywords[is_found]]
  return rst
