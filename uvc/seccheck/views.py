# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok


from zope import component
from zope import interface
from zope.publisher.interfaces.browser import IBrowserView


def default_view_name(component, module=None, **data):
    try:
        return component.__name__.lower()
    except:
        return ''


grok.templatedir('templates')


class SecOverview(grok.Page):
    grok.name('so')
    grok.context(interface.Interface)

    def getAvailableViews(self):
        views = component.getAdapters(
            (self.context, self.request),
            interface.Interface)
        views = {k: v for (k, v) in views if IBrowserView.providedBy(v)}
        return views

    def update(self):
        views = self.getAvailableViews()
        views.pop('')
        views.pop('widget_macros')
        self.views = views

    def getName(self, page):
        return "%s <br/> %s.%s" % (
            grok.name.bind().get(page) or default_view_name(page),
            page.__class__.__module__,
            page.__class__.__name__)

    def getPermission(self, page):
        return grok.require.bind().get(page)
