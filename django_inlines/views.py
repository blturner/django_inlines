from django.contrib.admin.views.decorators import staff_member_required

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import Http404
from django.conf import settings

from django_inlines import inlines


@staff_member_required
def js_inline_config(request):
    registered = []
    sorted_inlines = sorted(inlines.registry._registry.items())
    for inline in sorted_inlines:
        d = {"name": inline[0]}
        inline_cls = inline[1]
        d["help"] = getattr(inline_cls, "help", "")
        d["variants"] = getattr(inline_cls, "variants", [])
        args = getattr(inline_cls, "inline_args", [])
        d["args"] = sorted(args, key=lambda d: d["name"])
        if issubclass(inline_cls, inlines.ModelInline):
            d["app_path"] = "%s/%s" % (
                inline_cls.model._meta.app_label,
                inline_cls.model._meta.model_name,
            )
        registered.append(d)
    return render_to_response(
        "admin/django_inlines/js_inline_config.js",
        {"inlines": registered},
        content_type="text/javascript",
    )


@staff_member_required
def get_inline_form(request):
    inline = request.GET.get("inline", None)
    target = request.GET.get("target", None)
    if not inline or not target:
        raise Http404('"inline" and "target" must be specified as a GET args')
    inline_cls = inlines.registry._registry.get(inline, None)
    if not inline_cls:
        raise Http404("Requested inline does not exist")
    context_dict = {
        "help_text": getattr(inline_cls, "help_text", ""),
        "inline_args": getattr(inline_cls, "inline_args", []),
        "target": target,
        "variants": getattr(inline_cls, "variants", []),
    }
    try:
        app_label = inline_cls.get_app_label()
    except AttributeError:
        pass

    if app_label:
        context_dict["app_label"] = app_label
        context_dict["changelist_url"] = reverse(
            "admin:{0}_{1}_changelist".format(
                inline_cls.model._meta.app_label,
                inline_cls.model._meta.model_name,
            )
        )
    return render_to_response(
        "admin/django_inlines/inline_form.html", context_dict
    )
