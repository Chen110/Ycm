from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.template import RequestContext
from zabbix_api import Zabbix_API
from asset.models import HostList
# Create your views here.

def monitor_host_list(request):
    """
    list monitor_host
    """
    hosts_list = Zabbix_API().getHosts()
    paginator = Paginator(hosts_list,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        msg_host = paginator.page(page)
    except :
        msg_host = paginator.page(paginator.num_pages)
    return render_to_response('monitor_list.html',
                                {'all_host_list': hosts_list ,
                                 'page': page,
                                  'paginator':paginator},
                                  context_instance=RequestContext(request)
                              )

def chcek_host_monitor(request):
    hosts_list = Zabbix_API().getHosts()
    monitor_hosts = [ hsots['host']  for hsots in hosts_list]
    asset_host_list = HostList.objects.all().values('hostname')
    asset_list = [ x['hostname'] for x in asset_host_list]
    difflist = list(set(asset_list).difference(monitor_hosts))
    paginator = Paginator(difflist,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        msg_host = paginator.page(page)
    except :
        msg_host = paginator.page(paginator.num_pages)
    return render_to_response('unmonitor_list.html',
                                {'host_list': difflist ,
                                 'page': page,
                                  'paginator':paginator},
                                  context_instance=RequestContext(request)
                              )
