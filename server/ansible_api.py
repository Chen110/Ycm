# -*- coding: utf-8 -*-

import requests
from Ycm import settings

url = settings.ANSIBLE_API['url'].rstrip('/')
user = settings.ANSIBLE_API['user']
password = settings.ANSIBLE_API['password']

class AnsibleAPI(object):
    __token_id = ''
    def __init__(self):
        self.__url = url
        self.__user = user
        self.__password =  password

    def token_id(self):
        ''' user login and get token id '''
        params = { username': self.__user, 'password': self.__password}
        content = self.postRequest(params,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def postRequest(self,obj,prefix='/'): #post提交
        url = self.__url + prefix
        headers = {'X-Auth-Token' : self.__token_id}
        resp = requests.post(url,
                    data = obj,
                    headers = headers,
                    verify = False
                    )
        return resp.json()


    def remote_noarg_execution(self,tgt,fun):
        ''' 无参数的命令 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        self.token_id()
        content = self.postRequest(params)
        try:
            ret = content['return'][0][tgt]
        except Exception as a:
            ret = ""
        return ret

    def remote_execution(self,tgt,fun,arg):
        ''' 有参数的命令 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        self.token_id()
        content = self.postRequest(params)
        try:
            ret = content['return'][0][tgt]
        except Exception , e:
            ret = u'命令错误'
        return ret

    def target_remote_execution(self,tgt,fun,arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        self.token_id()
        content = self.postRequest(params)
        try:
            jid = content['return'][0]['jid']
        except Exception ,e:
            jid = "error"
        return jid

    def deploy(self,tgt,arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        self.token_id()
        content = self.postRequest(params)
        return content

    def async_deploy(self,tgt,arg):
        ''' Asynchronously send a command to connected minions '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        self.token_id()
        content = self.postRequest(params)
        jid = content['return'][0]['jid']
        return jid

    def target_deploy(self,tgt,arg):
        ''' Based on the node group forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        self.token_id()
        content = self.postRequest(params)
        jid = content['return'][0]['jid']
        return jid
