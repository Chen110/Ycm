# -*- coding: utf-8 -*-
deploy_op = 'salt'        # salt/ansible/rcsy

SALT_API = {
            "url": "https://127.0.0.1:8888",
            "user": "salt",
            "password": "salt",
            }

# 自动装机
Cobbler_API = {
            "url": "",
            "user": "",
            "password": ""
            }

# zabbix api
zabbix_API = {
               "url" : "",
               "user": "Admin",
               "password": "zabbix"
             }

# salt result
RETURNS_MYSQL = {"host": "localhost",
               "port": 3306,
               "database": "salt",
               "user": "salt",
               "password": "salt"
                }
#服务模块
SERVICE = {"nginx": "nginx",
           "php": "php",
           "mysql": "mysql",
           "sysinit": "sysinit",
           "logstash": "logstash",
           "zabbix": "zabbix",
           "redis": "redis",
           "memcached": "memcached"
          }
#数据库
YCM_MYSQL = {"host": "localhost",
               "port": 3306,
               "database": "ycm",
               "user": "root",
               "password": "root"
                }
