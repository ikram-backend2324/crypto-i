import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def _inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    return text


@register.filter
def render_markdown(value):
    """Tiny, safe markdown -> HTML (headings, lists, paragraphs, bold/italic/code)."""
    if not value:
        return ""
    lines = value.replace("\r\n", "\n").split("\n")
    html, list_type = [], None

    def close_list():
        nonlocal list_type
        if list_type:
            html.append(f"</{list_type}>")
            list_type = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue
        h = re.match(r"^(#{1,4})\s+(.*)$", line)
        if h:
            close_list()
            level = min(len(h.group(1)) + 1, 4)  # # -> h2
            html.append(f"<h{level}>{_inline(h.group(2))}</h{level}>")
            continue
        ol = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        ul = re.match(r"^\s*[-*•]\s+(.*)$", line)
        if ol:
            if list_type != "ol":
                close_list(); html.append("<ol>"); list_type = "ol"
            html.append(f"<li>{_inline(ol.group(1))}</li>")
            continue
        if ul:
            if list_type != "ul":
                close_list(); html.append("<ul>"); list_type = "ul"
            html.append(f"<li>{_inline(ul.group(1))}</li>")
            continue
        close_list()
        html.append(f"<p>{_inline(line)}</p>")

    close_list()
    return mark_safe("\n".join(html))
