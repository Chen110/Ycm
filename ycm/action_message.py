# -*- coding: utf-8 -*-
from models import *

def enter(admin,ctype,caction,caction_ip,message):
    Message.objects.create( who = admin,
                            type = ctype,
                            action = caction,
                            action_ip = caction_ip,
                            content = message)
