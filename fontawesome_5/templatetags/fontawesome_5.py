from typing import Any, Optional

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import conditional_escape, format_html, mark_safe

from .. import Icon
from ..app_settings import get_css, get_prefix

css = get_css()
register = template.Library()


@register.simple_tag
def fa5_icon(*args, **kwargs):
    return Icon(*args, **kwargs).as_html()


@register.simple_tag
def fontawesome_5_static():
    staticfiles = []

    for stylesheet in css:
        staticfiles.append(format_html('<link href="{}" rel="stylesheet" media="all">', stylesheet))

    staticfiles.append(
        format_html(
            '<script type="text/javascript" src="{}"></script>', static("fontawesome_5/js/django-fontawesome.js")
        )
    )

    return mark_safe(conditional_escape("\n").join(staticfiles))


@register.inclusion_tag("fontawesome_5/icon_as_html.html")
def icon_as_html(icon: str, size: Optional[str] = None, title: Optional[str] = None) -> dict[str, Any]:
    """
    Render the icon as HTML, with extra size and title.

    :param icon: Icon
    :param size: Size of the icon
    :param title: Title of the icon
    :return: Render-able dict
    """
    output = {"debug": settings.DEBUG}
    # Parse the icon
    split = icon.split(",")
    if len(split) == 1:
        _prefix = get_prefix()
        _icon_name = split[0]
    else:
        _prefix = split[0]
        _icon_name = split[1]
    output.update(
        {
            "title": title,
            "size": size,
            "icon": _icon_name,
            "style_prefix": _prefix,
        }
    )
    return output
