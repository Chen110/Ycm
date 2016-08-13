from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template import RequestContext
from ycm.mysql import db_operate
from ycm.models import Message

def history_list(request):
    #msg_list = Message.objects.all()
    admin = request.session.get('username')
    msg_list = Message.objects.filter(who = admin)
    paginator = Paginator(msg_list,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        msg_host = paginator.page(page)
    except :
        msg_host = paginator.page(paginator.num_pages)
    return render_to_response('history.html',
                                {'all_msg_list': msg_host,
                                 'page': page,
                                 'paginator':paginator
                                 },context_instance=RequestContext(request))
