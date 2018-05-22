from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

#Constants: jsonrpc_urlpatterns
jsonrpc_urlpatterns = patterns('ecoude_cooking',
        (r'^rpc$', 'system.ajax_views'),
)

#Constants: urlpatterns
urlpatterns = patterns('ecoude_cooking',
        (r'^$', 'system.views.home'),
        (r'^problems/$', 'system.views.problems'),
        (r'^problem/(?P<problem_id>\d+)$', 'system.views.notes'),
        (r'^solutions/(?P<problem_id>\d+)/(?P<framework_id>\d+)/$', 'system.views.solutions'),
        (r'^solution/(?P<inputfile_id>\d+)/(?P<framework_id>\d+)/$', 'system.views.solution'),
        (r'^about/$', 'system.views.about'),
        (r'^output/(?P<outputfile_id>\d+)$', 'system.views.output'),
        (r'^tag/(?P<tag_id>\d+)$', 'system.views.tag'),
        (r'^editproblem/(?P<problem_id>\d+)$', 'system.views.editproblem'),
        (r'^note/(?P<note_id>\d+)$', 'system.views.note'),
        (r'^statistics/$', 'system.views.statistics'),
        (r'^accounts/signup/$', 'system.views.signup'),
        url(r'^accounts/login/$', auth_views.login,{'template_name': 'login.html'},name='auth_login'),
        url(r'^accounts/logout/$',auth_views.logout,{'template_name': 'logout.html'},name='auth_logout'),
        (r'^accounts/profile', 'system.views.problems'),
        (r'^settings', 'system.views.settings'),
        (r'^ide/(?P<problem_id>\d+)/(?P<project_id>\d+)/$', 'system.views.ide'),
        (r'^problemtag/(?P<tag_id>\d+)$', 'system.views.problemtag'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

admin.autodiscover()
urlpatterns += patterns('',
    ('^admin/', include(admin.site.urls)), 
)
