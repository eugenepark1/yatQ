'''
Created on Oct 18, 2017

@author: eugenep
'''
import random
import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r %2.6f sec' % \
              (method.__name__, te-ts)
        return result

    return timed

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n) # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

'''
queue_status = {
        node_1: (<sumDurs> , <num_of_workers>)
        .
        .
        .
        node_n: (<sumDurs> , <num_of_workers>)
    }
    
jobs_to_assign = [dur1, ..., durn]
'''

def calculate_balanceConstant(queue_status):
    '''
    @return: q_constant (lower the better)
    '''
    q_loads = [ tup_v[0]/tup_v[1] for tup_v in queue_status.itervalues()]

    return stddev(q_loads)


@timeit
def assign(jobs, queue_status):
    '''
    for example, let's say we have two queues
    q_load =  (d/n) / w 
        (q1) 12d 4n 4w    <  (q2) 3d 1n 1w  
            3/4                    12/4
    
    now if i had [3,3,3,3,3], then i would want
    [3]x4 to q(1) and [3]x1 to (q2)
    
    
    
    # of workers and the number of jobs are the most important
    4 workers get 4 jobs and 1 worker get 1 job
    next Q is which 4 jobs and which 1 job       - we figured out the number of jobs, now need to figure out which
    easy case [10,10,10,10,10]
    hard case [1,4,5,6,2] if q1 and q2 are empty then it doesnt matter, but if queue arent empty then we need some work

    checkkkk
    '''
    print calculate_balanceConstant(queue_status)
    q_loads = [ tup_v[0]/tup_v[1] for tup_v in queue_status.itervalues()]
    q_loads.sort()
    print q_loads

    print q_loads



num_of_queues = 100
queue_status = dict( zip( ["node_%s" % i for i in range(num_of_queues)], [(random.randint(12,36), 4) for i in range(num_of_queues)]) )
#print queue_status

num_of_jobs = 10000
jobs_to_assign = [random.randint(1,10) for i in range(num_of_jobs)]

print assign(jobs_to_assign, queue_status)








