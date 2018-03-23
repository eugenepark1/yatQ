'''
Created on Oct 16, 2017

@author: eugenep


given a list of jobs' expectued durs and q weight, distribute the jobs so that q's weight is the most balanced
most_balanced = diff amonst weights of Q's are minimal

queues = {
        q1: (weight1, num_of_workers1),
        ...
        qn: (weightn, num_of_workersn)
        }

where (1,1) == (8,8) as q_constant = weight/num_of_workers

jobs = (<cpus>, <time>)
where cpu > 1, reduces num_of_workes by <cpus>-1 until <time>


    now, if cpus is > 1, it will reduce the number of jobs which can be run on the node of the queue
    so this has to be taken into an account
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


def calculate_qWeight(qDur, qResource, numWorker):
        
    base = float(qResource) / float(numWorker)
    #print "qDur %s qResource %s numWorker %s base %s" % (qDur, qResource, numWorker, base)

    return qDur/ base

def calculate_balanceConstant(queue_status):
    '''
    A queue holds N jobs where a job = Job(dur, cpu)
    q_dur = sum(job_dur)
    q_resource = sum(job_cpu)
    
    queue_status = {
        q1: (q_dur1, q_resource1, num_of_workers1),
        ...
        qn: (q_durn, q_resourcen, num_of_workersn)
    }
    
    q_weight should be elapsed time.. but 
    easiest q_weight is q_dur / (q_resources / num_of_workers)
    
    q_constant = stddev of q_weights
    
    @return: q_constant (lower the better)
    '''

    q_constant = [ calculate_qWeight(tup_v[0], tup_v[1], tup_v[2]) for tup_v in queue_status.itervalues()]
    #print q_constant
    return stddev(q_constant)

num_of_queues = 100
queue_status = dict( zip( ["node_%s" % i for i in range(num_of_queues)], [(random.randint(12,36), random.randint(4,5), 4) for i in range(12)]) )
#print "q_status: %s" % queue_status

num_of_jobs = 10000
jobs_to_assign = [(random.randint(1,10), random.randint(1,2)) for i in range(num_of_jobs)]
#print "jobs %s" % jobs_to_assign

@timeit
def assign(jobs, queue_status):
    '''
    goal here is to distribute jobs to queues so that calculateConstant for queues are minimized
    
    assignMap = {
            <q_name1>: [job1...jobn]
            ...
            <q_namen>: [job1...jobn]
        }
    '''
    print "current balanceConstant %.3f" % calculate_balanceConstant(queue_status)
    assignMap = {}

    q_constant_sorted = []
    for q_name, q_values in queue_status.iteritems():
        q_constant = calculate_qWeight(q_values[0], q_values[1], q_values[2])
        q_constant_sorted.append( (q_name, q_constant) )
    q_constant_sorted.sort(key=lambda tup: tup[1])
    print q_constant_sorted

    #jobs_sorted = sorted(jobs, key=lambda tup: tup[0]*tup[1], reverse=True)
    jobs.sort(key=lambda tup: tup[0]*tup[1])
    
    # percentage based
    
    
    
    
    print "after balanceConstant %.3f" % calculate_balanceConstant(queue_status)
    return assignMap

print assign(jobs_to_assign, queue_status)





