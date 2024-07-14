from django.urls import path
from django.contrib.auth import views as auth_views
from .views import main_page_view, policy_view, elektrik_view, kişisel_view, signout, profile_view, calender_view, \
    office_view, olasılık_view, tasarım_view, yazılım_view, odeme_view, unatuhenticated_view, authenticated_view, \
    mobiluygulama_view, nesneyonelimliprg_view, temelalgoritma_view, webgelistirme_view, yazilimtest_view, activate, \
    ictasarim_view, mimarlik_view, modatasarim_view, oyuntasarim_view, olasilikveistatistik_view, excell_view, \
    onenote_view, outlook_view, powerpoint_view, sharepoint_view, word_view, iletisimbecerileri_view, motivasyon_view, \
    ozguven_view, zamanyonetimi_view, elektrikproje_view, temelelektrik_view, register_instructor_view, calender_view, \
    category_view, subcategory_view, checkout_view, my_courses, instructor_courses, add_new_course
from . import views

urlpatterns = [
    path('',views.main_page_view, name='main_page'),

    # ------------------ Dersler -----------------#
    path('elektrik/',elektrik_view, name='elektrik'),
    path('kişisel/',kişisel_view, name='kişisel'),
    path('office/',office_view, name='office'),
    path('olasılık/',olasılık_view, name='olasılık'),
    path('tasarım/',tasarım_view, name='tasarım'),
    path('yazilimcategory/',yazılım_view, name='yazilim'),
    path('category/<int:id>',category_view, name='dynamic_category'),
    path('subcategory/<int:id>', subcategory_view, name='dynamic_subcategory'),

    # ------------------ Dersler Son -----------------#
    
    
    path('policy/',policy_view, name='policy'),
    path('register/', views.register_view, name='register'), 
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('register_insturctor/',views.register_instructor_view, name='register_insturctor'), 
    path('login/', views.login_view, name='login'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile_view, name='profile'),
    


    # ------------------ Odeme -----------------#s
    path('odeme/',odeme_view, name='odeme'),
    path('my_courses/',my_courses, name = 'my_courses'),
    path('instructor_courses/',instructor_courses, name = 'instructor_courses'),
    path('add_new_course/', add_new_course, name='add_new_course'),
    path('set_meeting_url/', views.set_meeting_url, name='set_meeting_url'),
    path('set_video_url/', views.set_video_url, name='set_video_url'),
    path('calender/',calender_view, name='calender'),
    path('checkout/<int:id>',checkout_view, name='checkout'),

    # ------------------ Loginli mainm -----------------#
    path('authenticated/',authenticated_view, name='authenticated'),
    path('unauthenticated/',unatuhenticated_view, name='unatuhenticated'),

    
    # ------------------ Ders Başlıkları-----------------#
    # Yazılım
    path('mobiluygulama/',mobiluygulama_view, name='mobiluygulama'),
    path('nesneyonelimliprg/',nesneyonelimliprg_view, name='nesneyonelimliprg'),
    path('temelalgoritma/',temelalgoritma_view, name='temelalgoritma'),
    # path('veritabani/',veritabani_view, name='veritabani'),
    path('webgelistirme/',webgelistirme_view, name='webgelistirme'),
    path('yazilimtest/',yazilimtest_view, name='yazilimtest'),

    # Tasarım
    path('ictasarim/',ictasarim_view, name='ictasarim'),
    path('mimarlik/',mimarlik_view, name='mimarlik'),
    path('modatasarim/',modatasarim_view, name='modatasarim'),
    path('oyuntasarim/',oyuntasarim_view, name='oyuntasarim'),

    # Olasılık
    path('olasilikveistatistik/',olasilikveistatistik_view, name='olasilikveistatistik'),

    # Office
    path('excell/',excell_view, name='excell'),
    path('onenote/',onenote_view, name='onenote'),
    path('outlook/',outlook_view, name='outlook'),
    path('powerpoint/',powerpoint_view, name='powerpoint'),
    path('sharepoint/',sharepoint_view, name='sharepoint'),
    path('word/',word_view, name='word'),

    # Kişisel Gelişim
    path('iletisimbecerileri/',iletisimbecerileri_view, name='iletisimbecerileri'),
    path('motivasyon/',motivasyon_view, name='motivasyon'),
    path('ozguven/',ozguven_view, name='ozguven'),
    path('zamanyonetimi/',zamanyonetimi_view, name='zamanyonetimi'),

    #Elektrik
    path('elektrikproje/',elektrikproje_view, name='elektrikproje'),
    path('temelelektrik/',temelelektrik_view, name='temelelektrik'),
    
    # ------------------ Ders Başlıkları-----------------#
   path('calender/',calender_view, name='calender')
]
