# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from Ycm import settings

def index(request):
    request.session['deploy_op'] = settings.deploy_op
    if request.session.get('username'):
        username = request.session.get('username')
        return render_to_response('index.html',{},context_instance=RequestContext(request))
    else:
        msgs={'msg':u"请输入用户名和密码"}
        msgs.update(csrf(request))
        return render_to_response('login.html',msgs,context_instance=RequestContext(request))

def login(request):
    return render_to_response('login.html',{},context_instance=RequestContext(request))

def logout(request):
    del request.session['username']
    return render_to_response('login.html')

@csrf_exempt
def check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    request.session['username'] = username
    user = auth.authenticate(username=username, password=password)
    print
    msgs={}
    if user is not None :
        if user.is_active:
            #login(request, user)
            username = request.session.get('username')
            return render_to_response('index.html',{},context_instance=RequestContext(request))
        else:
            msgs['msg']=u"用户无权限"
    else:
        msgs['msg']=u"用户名或密码错误"
    msgs.update(csrf(request))
    print msgs
    return render_to_response('login.html',msgs,context_instance=RequestContext(request))
