from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-student/<int:stid>/', views.delete_student, name='delete_student'),
    path('create-class/', views.create_class, name='create_class'),
    path('manage-classes/', views.manage_classes, name='manage_classes'),
    path('edit-class/<int:class_id>/', views.edit_class, name='edit_class'),
    path('create-subject/', views.create_subject, name='create_subject'),
    path('manage-subjects/', views.manage_subjects, name='manage_subjects'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('add-subject-combination/', views.add_subject_combination, name='add_subject_combination'),
    path('manage-subject-combination/', views.manage_subject_combination, name='manage_subject_combination'),
    path('add-student/', views.add_student, name='add_student'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('edit-student/<int:stid>/', views.edit_student, name='edit_student'),
    path('add-result/', views.add_result, name='add_result'),
    path('get-students-subjects/', views.get_students_subjects, name='get_students_subjects'),
    path('manage-result/', views.manage_result, name='manage_result'),
    path('edit-result/<int:stid>/', views.edit_result, name='edit_result'),
    path('add-notice/', views.add_notice, name='add_notice'),
    path('manage-notice/', views.manage_notice, name='manage_notice'),
    path('delete-notice/<int:id>/', views.delete_notice, name='delete_notice'),
    path('change-password/', views.change_admin_password, name='admin_change_password'),
    path('search-result/', views.search_result, name='search_result'),
    path('check-result/', views.check_result, name='check_result'),
  
 









]
