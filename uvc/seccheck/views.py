# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope import component
from zope import interface
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.publisher.interfaces.browser import IBrowserView
from zope.security.management import getInteraction
from zope.location import ILocation
# from zope.security import canAccess   ## We could avoid a security context switch
from zope.securitypolicy.interfaces import Allow
from zope.security.testing import Participation, Principal
from zope.security import checkPermission
from zope.security.management import getSecurityPolicy
from grokcore.view.interfaces import IGrokView


def default_view_name(component, module=None, **data):
    try:
        return component.__name__.lower()
    except:
        return ''


grok.templatedir('templates')


def lineage(item):
    while item is not None:
        yield item
        try:
            item = item.__parent__
        except AttributeError:
            # We try an adaptation. If it fails, this time, we let it
            # bubble up.
            item = ILocation(item)
            item = item.__parent__


class SecOverview(grok.Page):
    grok.name('so')
    grok.context(interface.Interface)

    def __init__(self, context, request):
        grok.Page.__init__(self, context, request)
        self.principal = getInteraction().participations[0].principal

    def getAvailableViews(self, excepts=[]):
        generic_views = {}
        views = {}

        adapters = component.getAdapters(
            (self.context, self.request),
            interface.Interface)

        for k, v in adapters:
            if k not in excepts and IGrokView.providedBy(v):
                adapts = grok.context.bind().get(v)
                if adapts is interface.Interface:
                    generic_views[k] = v
                else:
                    views[k] = v
        return generic_views, views

    def update(self):
        self.generic, self.views = self.getAvailableViews(excepts=['widget_macros'])
        self.users = self.getUsers()
        
    def getName(self, page):
        return "%s <br/> %s.%s" % (
            grok.name.bind().get(page) or default_view_name(page),
            page.__class__.__module__,
            page.__class__.__name__)
 
    def getUsers(self):
        users = {}
        settings = IPrincipalRoleMap(self.context).getPrincipalsAndRoles()
        for role, userid, access in settings:
            if access is Allow:
                if userid in users:
                    users[userid].add(role)
                else:
                    users[userid] = set((role,))
        users['zope.Authenticated'] = set()
        users['zope.Everybody'] = set()
        return users

    def getAllowance(self, userid, view):
        participations = [Participation(Principal(userid))]
        interaction = getSecurityPolicy()(*participations)
        permission = grok.require.bind().get(view)
        allowed = interaction.checkPermission(permission, view)
        return {"permission": permission, "access": allowed}
