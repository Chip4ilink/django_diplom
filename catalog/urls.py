from django.urls import path, re_path
from . import views
# from django.conf.urls import url


urlpatterns = [
    # path(r'^catalog/$', views.index, name='index'),
    # path('books/', views.BookListView.as_view(), name='books'),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^divisions/$', views.DivisionListView.as_view(), name='divisions'),
    re_path(r'^division/(?P<pk>\d+)$', views.DivisionDetailView.as_view(), name='division-detail'),
    re_path(r'^devices/$', views.DeviceListView.as_view(), name='devices'),
    re_path(r'^device/(?P<pk>\d+)$', views.DeviceDetailView.as_view(), name='device-detail'),
    re_path(r'^readings/$', views.MeterReadingListView.as_view(), name='readings'),

    re_path(r'^division/(?P<pk>\d+)/readings', views.division_readings, name='division-readings'),
]

urlpatterns += [
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    re_path(r'^booksborrowed/$', views.LoanedBooksForLibrarianListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    re_path(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    re_path(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    re_path(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]

urlpatterns += [
    re_path(r'^reading/create/$', views.MeterReadingCreate, name='reading_create'),
    re_path(r'^reading/(?P<pk>\d+)/update/$', views.MeterReadingUpdate.as_view(), name='reading_update'),
    re_path(r'^reading/(?P<pk>\d+)/delete/$', views.MeterReadingDelete.as_view(), name='reading_delete'),
]

urlpatterns += [
    re_path(r'^device/create/$', views.DeviceCreate.as_view(), name='device_create'),
    re_path(r'^device/(?P<pk>\d+)/update/$', views.DeviceUpdate.as_view(), name='device_update'),
    re_path(r'^device/(?P<pk>\d+)/delete/$', views.DeviceDelete.as_view(), name='device_delete'),
]

urlpatterns += [
    re_path(r'^division/create/$', views.DivisionCreate.as_view(), name='division_create'),
    re_path(r'^division/(?P<pk>\d+)/update/$', views.DivisionUpdate.as_view(), name='division_update'),
    re_path(r'^division/(?P<pk>\d+)/delete/$', views.DivisionDelete.as_view(), name='division_delete'),
]

urlpatterns += [
    re_path(r'^import-csv/$', views.import_csv, name='import_csv'),
    re_path(r'^success/$', views.success_page, name='success_page'),  # Create this view if needed
]