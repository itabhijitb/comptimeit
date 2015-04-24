from comptimeit import CompareTimeIt
from itertools import  ifilter
def test_data_gen():
    from random import sample
    for i in range(1,5):
        n = 10**i
        population = set(range(1,100000))
        some_list = sample(list(population),n)
        population.difference_update(some_list)
        some_dict = dict(zip(sample(population,n),
                     sample(range(1,100000),n)))
        yield "Population Size of {}".format(n), (some_list, some_dict), {}
def foo_set(some_list, some_dict):
    return some_dict.viewkeys() & set(some_list )        
def foo_set_ashwin(some_list, some_dict):
    return some_dict.viewkeys() & set(some_list )

def foo_nested(some_list, some_dict):
    for x in some_list:
        if x in some_dict:
            return True
    return False

def foo_any(some_list, some_dict):
    return any(x in some_dict for x in some_list)

def foo_ifilter(some_list, some_dict):
    return bool(next(ifilter(some_dict.__contains__, some_list), False))

def foo_ifilter_v1(some_list, some_dict):
    return not not next(ifilter(some_dict.__contains__, some_list), False)

def foo_ifilter_v2(some_list, some_dict):
    return any(ifilter(some_dict.__contains__, some_list))
if __name__ == "__main__":
    for i in range(1,5):
        repeat = 10**i
        print "Timeit repeated for {} times".format(repeat)
        ctit = CompareTimeIt(test_data_gen, None)
        ctit.repeat = repeat
        ctit.register(foo_set, "")
        ctit.register(foo_set_ashwin, "")
        ctit.register(foo_nested, "")
        ctit.register(foo_any, "")
        ctit.register(foo_ifilter, "from __main__ import ifilter")
        ctit.register(foo_ifilter_v1, "from __main__ import ifilter")
        ctit.register(foo_ifilter_v2, "from __main__ import ifilter")
        print ctit()
        ctit.plot(log = True, title = "Timeit repeated for {} times".format(repeat))