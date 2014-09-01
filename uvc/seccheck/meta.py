import martian
import grok
import uvcsite
import os


class SecurityError(grok.GrokError):
    pass


_require_marker = object()


class CheckRequireGrokker(martian.ClassGrokker):
    """Ensure every grok.View has a grok.require directive"""
    martian.component(grok.View)
    martian.directive(grok.require, default=_require_marker)

    def execute(self, factory, config, require, **kw):
        if os.environ.get('UVC_SEC_CHECK') == '1':
            if require is _require_marker:
                context = grok.context.bind().get(factory)
                uvcsite.log('%r --> %r' % (factory, context))
        return True


class PageRequireGrokker(CheckRequireGrokker):
    martian.component(uvcsite.Page)


class PageRequireGrokker(CheckRequireGrokker):
    martian.component(uvcsite.TablePage)


class PageRequireGrokker(CheckRequireGrokker):
    martian.component(uvcsite.Form)
