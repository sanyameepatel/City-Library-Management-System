from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^reader/$', views.reader, name="reader"),
    url(r'^reader/(?P<reader_id>\d+)/$', views.get_reader, name="reader"),
    url(r'^reader/(?P<reader_id>\d+)/search_document/$', views.search_document, name="search_document"),
    url(r'^reader/(?P<reader_id>\d+)/reserve_document/(?P<doc_id>\d+)/$', views.reserve_document,
        name="reserve_document"),
    url(r'^reader/(?P<reader_id>\d+)/borrow_document/(?P<doc_id>\d+)/$', views.borrow_document,
        name="borrow_document"),
    url(r'^reader/(?P<reader_id>\d+)/reserve_document_copy/(?P<copy_id>\d+)/$', views.reserve_document_copy,
        name="reserve_document_copy"),
    url(r'^reader/(?P<reader_id>\d+)/borrow_document_copy/(?P<copy_id>\d+)/$', views.borrow_document_copy,
        name="borrow_document_copy"),
    url(r'^reader/(?P<reader_id>\d+)/borrow_reserve_copy/(?P<res_number>\d+)/(?P<copy_id>\d+)/$', views.borrow_reserved_copy,
        name="borrow_reserved_copy"),
    url(r'^reader/(?P<reader_id>\d+)/view_reserved_documents/$', views.view_reserved_documents,
        name="view_reserve_document_copy"),
    url(r'^reader/(?P<reader_id>\d+)/publisher_documents/$', views.documents_by_publisher,
        name="search_document_publisher"),
    url(r'^reader/(?P<reader_id>\d+)/reserve_document/$', views.search_document_reserve,
        name="reserve_documents"),
    url(r'^reader/(?P<reader_id>\d+)/borrow_document/$', views.search_document_borrow,
        name="borrow_documents"),
    url(r'^reader/(?P<reader_id>\d+)/return_document/$', views.view_borrowed_documents,
        name="return_documents"),
    url(r'^reader/(?P<reader_id>\d+)/return_document_copy/(?P<borrowid>\d+)/(?P<copy_id>\d+)/$',
        views.return_borrowed_documents, name="return_document_copy"),
    url(r'^reader/(?P<reader_id>\d+)/check_fine/(?P<borrowid>\d+)/$',
        views.check_fine, name="check_fine"),
    url(r'^reader/(?P<reader_id>\d+)/view_borrowed_documents/$',
        views.view_borrowed_doc, name="borrow_doc"),
    url(r'^reader/(?P<reader_id>\d+)/cancel_reservation/(?P<res_number>\d+)/$',
        views.cancel_reservation, name="cancel_res"),
    # url(r'^reader_operations/(?P<reader_id>[0-9]+)$', views.reader_homepage, name="reader_operations"),
]