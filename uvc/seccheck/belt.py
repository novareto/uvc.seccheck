# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface
from zope.security.interfaces import Forbidden
from uvcsite.interfaces import IMyHomeFolder


@grok.subscribe(IMyHomeFolder, grok.IBeforeTraverseEvent)
def second_belt(object, event):
    principal = event.request.principal
    allowed_users = set(['zope.manager', object.__name__])
    allowed_groups = set(['uvc.MasterUser'])
    if principal.id not in allowed_users:
        if not (set(principal.groups) & allowed_groups):
            raise Forbidden('You are not authorized here.')
