# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from server.saltapi import SaltAPI
from Ycm import settings
from ycm.mysql import db_operate
from asset.models import HostList
#from ycm.models import *
from  server.code import Code_Work
from  server.json_data import BuildJson
from ycm.action_message import enter
import time

def salt_key_list(request):
    """
    list all key
    """

    user = request.user
    sapi = SaltAPI()
    minions,minions_pre = sapi.list_all_key()

    return render_to_response('salt_key_list.html',
                            {'all_minions': minions, 'all_minions_pre': minions_pre},
                            context_instance=RequestContext(request))

def salt_accept_key(request):
    """
    accept salt minions key
    """
    #request.session.get('username')
    node_name = request.GET.get('node_name')
    sapi = SaltAPI()
    ret = sapi.accept_key(node_name)
    enter(request.session.get('username'),"salt","key",node_name,'saltstack accept node key')
    #Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack accept node key')
    return HttpResponseRedirect(reverse('key_list'))

def salt_delete_key(request):
    """
    delete salt minions key
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI()
    ret = sapi.delete_key(node_name)
    enter(request.session.get('username'),"salt","key",node_name,'saltstack delete node key')
    #Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack delete node key')
    return HttpResponseRedirect(reverse('key_list'))


def module_deploy(request):
    """
    deploy (nginx/php/mysql..etc) module
    """

    ret = []
    jid = []
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtcheck = HostList.objects.filter(hostname=tgt)
        if tgtcheck:
            content='saltstack %s module depoy' % (arg)
            enter(request.session.get('username'),"salt","deploy",tgt,content)
            #Message.objects.create(type='salt', action='deploy', action_ip=tgt, content='saltstack %s module depoy' % (arg))
            sapi = SaltAPI()
            if 'sysinit' in arg:
                obj = sapi.async_deploy(tgt,arg[-1])    #先执行初始化模块,其他任意
                jid.append(obj)
                arg.remove('sysinit')
                if arg:
                    for i in arg:
                        obj = sapi.async_deploy(tgt,i)
                        jid.append(obj)
            else:
                for i in arg:
                    obj = sapi.async_deploy(tgt,i)
                    jid.append(obj)
            db = db_operate()
            for i in jid:
                time.sleep(10)
                sql = 'select returns from salt_returns where jid=%s'
                result=db.select_table(settings.RETURNS_MYSQL,sql,str(i))    #通过jid获取执行结果
                ret.append(result)
            #sapi.async_deploy('test-01','zabbix.api')   #调用zabbix.api执行模块监控
        else:
           ret = '亲，目标主机不对，请重新输入'

    return render_to_response('salt_module_deploy.html',
                                {'ret': ret},
                                context_instance=RequestContext(request))

def remote_execution(request):
    """
    remote command execution
    """
    tgt =''
    arg =''
    ret = ''
    tgtcheck = ''
    danger = ('rm','reboot','init ','shutdown')
    #admin = request.session.get('username')
    user = request.user
    goal = request.GET.get('goal')
    print goal
    if goal == "host" or goal == None:
        if request.method == 'POST':
            #action = request.get_full_path().split('=')[1]
            action = request.GET.get('action')
            if action == 'exec':
                tgt = request.POST.get('tgt')
                arg = request.POST.get('arg')
                tgtcheck = HostList.objects.filter(hostname=tgt)
                argcheck = arg not in danger
                if tgtcheck and argcheck:
                    sapi = SaltAPI()
                    ret = sapi.remote_execution(tgt,'cmd.run',arg)
                elif not tgtcheck:
                    ret = '目标主机不正确，请重新确认'
                elif not argcheck:
                    ret = '危险命令，请确认'
            content='saltstack execution command: %s ' % (arg)
            enter(request.session.get('username'),"salt","execution",tgt,content)
            #Message.objects.create(type='salt', action='execution', action_ip=tgt, content='saltstack execution command: %s ' % (arg))
        return render_to_response('salt_remote_execution.html',
               {'tgt': tgt,
                'arg': arg,
                'ret': ret,
                },context_instance=RequestContext(request))
    else:
        return render_to_response('salt_remote_group_execution.html',
               {'tgt': tgt,
                'arg': arg,
                'ret': ret,
                },context_instance=RequestContext(request))

def code_deploy(request):
    """
    Pull code for building, pushed to the server
    """

    ret = ''
    host = {'ga': 'test-01', 'beta': 'localhost.localdomain'}
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'push':
            pro = request.POST.get('project')
            url = request.POST.get('url')
            ver = request.POST.get('version')
            env = request.POST.get('env')
            capi = Code_Work(pro=pro,url=url,ver=ver)
            data = {pro:{'ver':ver}}
            obj = capi.work()      #构建rpm包
            if obj['comment'][0]['result'] and obj['comment'][1]['result'] and obj['comment'][2]['result']:
                json_api = BuildJson()
                json_api.build_data(host[env],data)   #刷新pillar数据，通过deploy下发SLS执行代码发布
                sapi = SaltAPI()
                if env == 'beta':
                    jid = sapi.target_deploy('beta','deploy.'+pro)
                elif env == 'ga':
                    jid = sapi.target_deploy('tg','deploy.'+pro)
                else:
                    jid = sapi.target_deploy('beta','deploy.'+pro)
                time.sleep(8)
                db = db_operate()
                sql = 'select returns from salt_returns where jid=%s'
                ret=db.select_table(settings.RETURNS_MYSQL,sql,str(jid))    #通过jid获取执行结果
    return render_to_response('code_deploy.html',
                                {'ret': ret
                                },
                              context_instance=RequestContext(request))
