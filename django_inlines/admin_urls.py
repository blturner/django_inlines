from django.urls import re_path as url

from . import views


urlpatterns = [
    url(
        r"^inline_config\.js$", views.js_inline_config, name="js_inline_config"
    ),
    url(r"^get_inline_form/$", views.get_inline_form, name="get_inline_form"),
]
