#!/usr/bin/env python
from __future__ import print_function
import time, collections
from sys import stderr as STDERR

RepeatType_base = collections.namedtuple('RepeatType_base',
                                      ('count','ival','ival_mul','ival_max'))

class RepeatType(RepeatType_base):
  def __int__(self): return self.count

configured_default = RepeatType(
    count   = 0,       # > 0: allow iteration alternating with successively
                       #      larger wait intervals via sleep_and_modify(rpt_t)
    ival    = 1.0,     # first sleep interval in seconds
    ival_mul = 2.0,    # multiplier for sleep interval
    ival_max = 5 * 60.0  # maximum sleep interval in seconds; default 5 min.
)

verbose = False
Default_Sleep_When_Integer_Used = 1.0 # second

def modified (q = configured_default, **kw):
    return RepeatType(**
        { pr[0]:pr[1] for pr in list(q._asdict().items()) + list(kw.items()) } )


class Bad_Retry_Type(RuntimeError): pass

def sleep_and_modify ( tries = configured_default ):
    repeat_iter = lambda t: modified( t, count = max(0, t.count - 1),
                                                 ival = min(t.ival*t.ival_mul, t.ival_max))
    if isinstance( tries, int ):
        if tries > 0:
            time.sleep(Default_Sleep_When_Integer_Used)
            return max( int(tries - 1), 0)
        else:
            return 0
    elif isinstance( tries, RepeatType ):
        if tries.count > 0:
            if verbose:
                print('sleeping for '+str(tries.ival)+'s; count= ',str(tries.count),file=STDERR)
            time.sleep( tries.ival )
            tries = repeat_iter( tries )
            if tries.count > 0: return tries
    else:
        raise Bad_Retry_Type("Required argument: int(N) | delay_repeat.modified(count=N)")
    return 0

################################################################

def test():

    global verbose
    verbose = True
    try:    input = raw_input
    except: pass

    x = modified ( ## --> start basis is configured_default
                        ival = 1.5,
                        ival_max = 10.0,
                        count=4 )

    if input('increasing type (y/n) ? ').upper().startswith('N'):

        x = modified ( x, ival_mul = 1.0 )

    if input('repeating type (y/n) ? ').upper().startswith('N'):

        x = modified ( x,  count = 0 )

    print ('sleeping...',file=STDERR)

    while x:
        x = sleep_and_modify( x )

    print ('...done',file=STDERR)

if __name__ == '__main__':

    test()
