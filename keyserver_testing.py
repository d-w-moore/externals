#!/usr/bin/env python

import subprocess

def gen_keyserver_cmd():
    servers = [
     "ipv4.pool.sks-keyservers.net",
     "pool.sks-keyservers.net",
     "na.pool.sks-keyservers.net",
     "eu.pool.sks-keyservers.net",
     "oc.pool.sks-keyservers.net",
    ]

    cmd = " || ".join(
     "gpg --keyserver hkp://%s "
     " --keyserver-options timeout=10 "
     " --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 "
                 " 7D2BAF1CF37B13E2069D6956105BD0E739499BDB " % server
         for server in servers)

    return cmd

#------------------------------------------------------------------------------

class mock_Popen_class:

    def __init__(self,count = 0):
        self.count = count

    def __call__(self,*args,**kwargs): # mock Popen constructor
        if self.count <= 0:
            object_ = subprocess.Popen(*self.args,**self.kwargs)
        else:
            object_ = self.mock_Popen_instance()
        self.count -= 1
        return object_

    class mock_Popen_instance:
        returncode = None
        def wait(self):
            self.communicate(['',''])
            return self.returncode
        poll = wait
        FAIL_CODE = 127
        def communicate(self,returnvalue=None):
            try:
                return ( 'mock stdout\n', 'mock stderr: return = {0.FAIL_CODE}\n'.format(self)
                       ) if returnvalue is None else tuple(returnvalue)
            finally:
                self.returncode = self.FAIL_CODE

if __name__ == '__main__':
    Popen = mock_Popen_class(count=1)
    p = Popen('(sleep 1)',shell=True)
    print (p.returncode)
    p.communicate()
    print ('hello')
    #p.communicate()
    #print('rtn = '+str(p.returncode))

