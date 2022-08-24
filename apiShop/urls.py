# -*- coding: utf-8 -*-

from django.urls import path

from apiCustomer.views import api_total_search, api_sign
from apiShop.views import api_front, api_info, api_gallery, api_review, api_blog

urlpatterns = [

    path('shop/front', api_front.TFront.as_view()),
    path('shop/front/<str:partner_id>', api_front.TFront.as_view()),
    path('shop/info', api_info.TInfo.as_view()),
    path('shop/info/<str:partner_id>', api_info.TInfo.as_view()),
    path('shop/info-photo', api_info.TInfoPhoto.as_view()),
    path('shop/sales-area', api_info.TSalesArea.as_view()),
    path('shop/sales-area/<str:partner_id>', api_info.TSalesArea.as_view()),
    path('shop/area-addr/<str:partner_id>', api_info.TAreaAddr.as_view()),
    path('shop/license-award', api_info.TLicenseAward.as_view()),
    path('shop/license-award/<str:partner_id>', api_info.TLicenseAward.as_view()),

    path('shop/gallery/<str:partner_id>', api_gallery.TGallery.as_view()),
    path('shop/review/<str:partner_id>', api_review.TReview.as_view()),
    path('shop/blog/<str:partner_id>', api_blog.TBlog.as_view()),
]