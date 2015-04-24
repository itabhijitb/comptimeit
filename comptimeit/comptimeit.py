'''
Created on Apr 24, 2015

@author: abhibhat
'''
class CompareTimeIt(object):
    from collections import namedtuple
    Fn_Details = namedtuple('Fn_Details',('fn','setup', 'desc'), False)
    class Result_Details:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
        def items(self):
            return self.kwargs.items()
        def __iter__(self):
            return self.kwargs.iterkeys()
        def __getitem__(self, key):
            return self.kwargs[key]
        def __setitem__(self, key, value):
            self.kwargs[key] = value
            return self.kwargs[key]
        def keys(self):
            return self.kwargs.keys()
        def values(self):
            return self.kwargs.values()
    def __init__(self, testdatagen, repeat = None):
        from collections import OrderedDict
        self.fns = OrderedDict()
        self.result= OrderedDict()
        self.repeat = repeat
        self.testdatagen = testdatagen
    def register(self, fn, setup, desc  = ""):
        self.fns[fn.__name__] = CompareTimeIt.Fn_Details(fn, setup, desc)
    def __call__(self):
        from functools import partial
        from operator import itemgetter
        from collections import OrderedDict
        from timeit import timeit
        def time(fn, setup, *args, **kwargs):
            return timeit(partial(fn, *args, **kwargs),
                          number = self.repeat,
                          setup=setup)
        for data in self.testdatagen():
            iden, args, kwargs = data
            self.result[iden] = OrderedDict()
            for fname, fdetails in self.fns.items():
                self.result[iden][fname] = CompareTimeIt.Result_Details(rank = 0,
                                                                        fname = fname,
                                                                        result = time(fdetails.fn,
                                                                                      fdetails.setup,
                                                                                      *args,
                                                                                      **kwargs),
                                                                        desc = fdetails.desc)
            self.result[iden] = sorted(self.result[iden].items(), 
                                       key = lambda elem:elem[1]['result'])
            for rank in range(len(self.result[iden])):
                self.result[iden][rank][1]['rank'] = rank + 1
            self.result[iden] = OrderedDict(self.result[iden])
        return self

    def __repr__(self):
        op = ""
        for test_id in self.result:
            op += "Test Run for {}\n".format(test_id)
            key_size = [max(map(len, map(str, self.result[test_id])))]
            value_sizes = {}
            for fname, result in self.result[test_id].items():
                for col in result:
                    value_sizes[col] = max(value_sizes.get(col,len(col)), len(str(result[col])))
                
            op += "{{:^{}}}|".format(value_sizes['rank']+ 2).format('rank')    
            op += "{{:^{}}}|".format(value_sizes['fname'] + 2).format('fname')  
            op += "{{:^{}}}|".format(value_sizes['result'] + 2).format('result')     
            op += "{{:^{}}}|".format(value_sizes['desc'] + 2).format('desc') 
            op += '\n'             
            for fname in self.result[test_id]:
                op += "{{:^{}}}|".format(value_sizes['rank'] + 2).format(self.result[test_id][fname]['rank'])
                op += "{{:^{}}}|".format(value_sizes['fname'] + 2).format(self.result[test_id][fname]['fname'])
                op += "{{:^{}}}|".format(value_sizes['result'] + 2).format(self.result[test_id][fname]['result'])
                op += "{{:^{}}}|".format(value_sizes['desc'] + 2).format(self.result[test_id][fname]['desc'])
                op += '\n'
        return op
    def plot(self, log = False, title = None):
        try:
            from matplotlib import pyplot as plt
            import matplotlib.cm  as cm
            import numpy as np
        except ImportError:
            print "Plotting not Supported"
            return
        from operator import itemgetter
        
        width = .1
        fig, ax = plt.subplots()
        rects = []
        legends =[]
        bxticks = False
        color=cm.rainbow(np.linspace(0,1,len(self.result) + 1))
        for  index, test_id in enumerate(self.result,1): 
            OX, OY = zip(*map(itemgetter('fname','result'), 
                              self.result[test_id].values()))
            if not bxticks: 
                ind = np.arange(len(OX))
                ax.set_xticks(ind + width * len(self.result) / 2)
                ax.set_xticklabels(OX)
                bxticks = True
            rects.append(ax.bar(ind + width * index, 
                                OY, width, 
                                color = color[index]))
            legends.append(test_id)
        if log: ax.set_yscale('log')
        box = ax.get_position()
        ax.set_xlabel('Functions' , fontsize=16)
        ax.set_ylabel('Execution time in sec (log scale)' , fontsize=16)
        if title: ax.set_title(title , fontsize=20)
        ax.legend(map(itemgetter(0), rects), legends, 
                  bbox_to_anchor=(1, 1), fancybox=True, shadow=True)
        fig.autofmt_xdate()
        plt.show()
