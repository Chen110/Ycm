# -*- coding: utf-8 -*-

"""Ycm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from ycm.views import login, index,check,logout
from installos.views import *
from asset.views import *
from audits.views import *
from server.views import *
from monitor.views import *
urlpatterns = [
    url(r'^ycm/admin/', include(admin.site.urls)),
    #url(r'^/index.html$', 'ycm.views.index'),
    url(r'^$', index, name='index'),
    url(r'^login/$', login,name='login'),
    url(r'^logout/$', logout,name='logout'),
    url(r'^check/$',check,name='check'),
    url(r'^install/install_list/$', system_install_list, name='install_list'),
    url(r'^install/install_manage/(?P<id>\d+)/$', system_install_managed, name='install_manage'),
    url(r'^install/add_install/$', system_install_managed, name='add_install'),
    url(r'^install/system_install/$',system_install, name='system_install'),
    url(r'^install/install_record/$',system_install_record, name='install_record'),
    #资产管理
    url(r'^asset/host_list/$', host_list, name='host_list'),
    url(r'^asset/add_host/$', host_list_manage, name='add_host'),
    url(r'^asset/delete_host/', host_list_manage, name='host_delete'),
    url(r'^asset/host_manage/(?P<id>\d+)/$', host_list_manage, name='host_manage'),
    #url(r'^asset/server_asset/$', server_asset_list, name='server_asset_list'),
    url(r'^asset/server_get/$', get_server_asset, name='get_server_asset'),
    url(r'^asset/device_list/$', network_device_list, name='network_device_list'),
    url(r'^asset/device_add/$', network_device_discovery, name='add_device'),
    url(r'^asset/idc_list/$', idc_asset_list, name='idc_asset_list'),
    url(r'^asset/add_idc/$', idc_asset_manage, name='add_idc'),
    #命令操作
    url(r'^server/key_list/$', salt_key_list, name='key_list'),
    url(r'^server/key_delete/$', salt_delete_key, name='delete_key'),
    url(r'^server/key_accept/$', salt_accept_key, name='accept_key'),
    url(r'^server/module_deploy/$', module_deploy, name='module_deploy'),
    url(r'^server/remote_execution/$', remote_execution, name='remote_execution'),
    url(r'^server/code_deploy/$', code_deploy, name='code_deploy'),

    url(r'^audit/history/$', history_list, name='history_list'),
    #监控
    url(r'monitor/monitor_host_list/$',monitor_host_list,name="monitor_host_list"),
    url(r'monitor/chcek_host_monitort/$',chcek_host_monitor,name="chcek_host_monitor"),
]
