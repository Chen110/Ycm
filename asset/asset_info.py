# -*- coding: utf-8 -*-
from Ycm import settings
import threading
from sys import path
if 'saltserver' not in path:
    path.append(r'saltserver')
from saltapi import SaltAPI

asset_info = []

def get_server_asset_info(tgt):
    '''
    Salt API得到资产信息，进行格式化输出
    '''
    print
    global asset_info
    info = []
    sapi = SaltAPI()
    ret = sapi.remote_noarg_execution(tgt,'grains.items')
    manufacturer = ret['manufacturer']
    info.append(manufacturer)
    productname = ret['productname']
    info.append(productname)
    serialnumber = ret['serialnumber']
    info.append(serialnumber)
    cpu_model = ret['cpu_model']
    info.append(cpu_model)
    num_cpus = int(ret['num_cpus'])
    info.append(num_cpus)
    num_gpus = int(ret['num_gpus'])
    info.append(num_gpus)
    mem_total = str(round(int(ret['mem_total'])/1000.0,))[:-2] + 'G'
    info.append(mem_total)
    disk = sapi.remote_noarg_execution(tgt,'disk.usage')
    disk_size = str(int(disk['/']['1K-blocks'])/1048576) + 'G'
    info.append(disk_size)
    try:
        raidlevel = ret['raidlevel']
    except Exception as e:
        raidlevel = ""
    info.append(raidlevel)

    id = ret['id']
    info.append(id)

    try:
        lan_ip = ret['lan_ip'][0]
    except Exception as e:
        lan_ip = ""
    info.append(lan_ip)

    try:
        lan_mac = ret['hwaddr_interfaces']['eth0']
    except Exception,e :
        lan_mac = ""
    info.append(lan_mac)
    sys_ver = ret['os'] + ret['osrelease'] + '-' + ret['osarch']
    info.append(sys_ver)
    virtual = ret['virtual']
    info.append(virtual)
    try:
        idc_name = ret['idc_name']

    except Exception as e:
        idc_name=""
    info.append(idc_name)
    return info
