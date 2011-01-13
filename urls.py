from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view
from minicms.solrest.handlers import ContentsHandler,ContentItemHandler

contents = Resource(handler=ContentsHandler)
contentItem = Resource(handler=ContentItemHandler)

urlpatterns = patterns('',
	url(r'/item/(.*)', contentItem),
    url(r'/(.*)/(.*)/(.*)', contents),
    # automated documentation
    url(r'^$', documentation_view),
)