# -*- coding: utf-8 -*-
from Ycm import settings
import threading
from sys import path
if 'saltserver' not in path:
    path.append(r'saltserver')
from saltapi import SaltAPI

def get_server_status_info(tgt):
    '''
    Salt API得到资产信息，进行格式化输出
    '''
    info = {}
    sapi = SaltAPI()
    ret = sapi.remote_noarg_execution(tgt,'status.all_status')
    cpu_status=ret['cpustats]
    disk_status=ret['diskstats']
    mem_status=ret['meminfo']
    
    vm_status=ret['vmstats']
    return info
