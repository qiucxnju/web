from django import template
import markdown

register = template.Library()


@register.filter(name='markdown')
def mark_down(value):
	return markdown.markdown(value)