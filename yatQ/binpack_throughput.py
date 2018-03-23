'''
Created on Oct 16, 2017

@author: eugenep

given a throughput (throughput meaning, how many jobs which can run in parallel, not a dispatch throughput)
to elaborate, even if you have a throughput of 1000 jobs/sec, if there are 10 cores, then obv not all 1000 jobs will run in parallel
in this problem, we will assume that there are enough resources to match throughput 

find the minimum throughput for minimum elapsed time
    implies in what order job needs to be dispatched - always sorted
'''
import random

# klibo@ontap
freqMap_klibo_ontap = {
    153: 1,
    31: 1,
    25: 1, 
    24: 1,
    17: 2,
    16: 1,
    15: 1,
    14: 1,
    13: 2,
    12: 4,
    11: 5,
    10: 2,
    9: 9,
    8: 13,
    7: 32,
    6: 41,
    5: 108,
    4: 254,
    3: 502,
    2: 1100,
    1: 790,
    0: 2099
    }

freqMap_klibo_nblade = {
    17: 1,
    13: 5,
    12: 6,
    11: 1,
    10: 7,
    8: 8,
    7: 13,
    6: 19,
    5: 37,
    4: 63,
    3: 163,
    2: 236,
    1: 70,
    0: 3
    }

freqMap_ulibso_mgmtgateway = {
    110: 1,
    95: 1,
    75: 1,
    70: 2,
    69: 1,
    66: 1,
    57: 3,
    56: 1,
    55: 1,
    54: 1,
    53: 2,
    52: 2,
    51: 1,
    50: 1,
    49: 1,
    48: 1,
    45: 1,
    44: 2,
    43: 2,
    42: 8,
    41: 2,
    40: 1,
    39: 3,
    38: 3,
    37: 2,
    36: 2,
    35: 1,
    33: 4,
    32: 7,
    31: 4,
    30: 7,
    29: 2,
    28: 1,
    27: 8,
    26: 7,
    25: 10,
    24: 8,
    23: 12,
    22: 8,
    21: 17,
    20: 18,
    19: 9,
    18: 10,
    17: 21,
    16: 18,
    15: 19,
    14: 26,
    13: 26,
    12: 23,
    11: 45,
    10: 36,
    9: 36,
    8: 52,
    7: 52,
    6: 67,
    5: 139,
    4: 244,
    3: 171,
    2: 244,
    1: 1021,
    0: 511
    }

freqMap = freqMap_ulibso_mgmtgateway

compile_times = []
for k,v in freqMap.iteritems():
    if k == 0:
        compile_times += [round(random.random(),4) for i in range(v)]
    else:
        compile_times += [k]*v
print compile_times

#compile_times = [5,3,2,1,5]
compile_times.reverse()
tp = 48
max_parallel = 48

running = []
elapsed_time = 0
while True:
    
    # decr running jobs
    tmp_running = []
    for i in running:
        i = i-1
        if i > 0:
            tmp_running.append(i)
    running = tmp_running

    # dispatch jobs
    cnt = 0
    while True:
        if len(running) == max_parallel:
            break

        if len(compile_times) > 0:
            running.append( compile_times.pop(0) )
            cnt += 1
            if cnt == tp:
                break
        else:
            break

    print "remaing jobs: %s" % compile_times
    print "running jobs: %s" % running
    print "elapsed time %s"  % elapsed_time

    if len(running) == 0:
        break
    
    elapsed_time += 1

    

