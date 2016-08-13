# -*- coding: utf-8 -*-
import json
import requests
class Zabbix_API:
    def __init__(self):
        self.url = "http://www.yaolinux.cn/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.authID = self.user_login()
    def user_login(self):
        data = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "user.login",
                        "params": {
                            "user": "Admin",
                            "password": "zabbix"
                        },
                        "id": 0
                        }
                    )
        resp = self.postRequest(data)
        return resp['result']

    def postRequest(self,data):

        try:
            resp = requests.post(
                        self.url,
                        data = data,
                        headers = self.header,
                        verify = False
                    )
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            return resp.json()

    def getHosts(self):
        '''获取主机列表'''
        data = data = json.dumps(
                                {
                                     "jsonrpc": "2.0",
                                     "method": "host.get",
                                     "params": {
                                        "output":["hostid","name","status","host"],
                                        "filter":{"host":""},
                                    },
                                    "auth" : self.authID, # theauth id is what auth script returns, remeber it is string
                                    "id" : 1,
                                    })
        hosts = self.postRequest(data)
        return hosts['result']
    def getGroup(self):
        '''获得组列表'''
        data = json.dumps(
                        {
                            "jsonrpc":"2.0",
                            "method":"hostgroup.get",
                            "params":{
                                "output":["groupid","name"],
                            },
                            "auth" : self.authID, # theauth id is what auth script returns, remeber it is string
                            "id":1,
                        })
        groups = self.postRequest(data)
        print groups['result']
    def getItems(self,host_id):
        '''获取主机监控项id'''
        data = json.dumps(
                        {
                            "jsonrpc":"2.0",
                            "method":"item.get",
                            "params":{
                                    "output":["itemids","key_"],
                                    "hostids": host_id ,
                                    },
                                    "auth": self.authID, # theauth id is what auth script returns, remeber it is string
                                    "id":1,
                         })
        items =  self.postRequest(data)
        print items['result']

    def get_items_history(self,item_id):
        '''获取监控项历史数据'''
        data = json.dumps(
                        {
                            "jsonrpc":"2.0",
                            "method":"history.get",
                            "params":{
                                "output":"extend",
                                "history":3,
                                "itemids":item_id,
                                "limit":10
                                },
                            "auth":self.authID , # theauth id is what auth script returns, remeber it is string
                            "id":1,
                        })
        history =  self.postRequest(data)
        print history
'''if __name__ == '__main__':
    zabbix = Zabbix_API()
    zabbix.getHosts()
    zabbix.getItems(10105)
    zabbix.getItems(23680)'''
