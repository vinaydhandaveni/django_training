from django.contrib import admin  
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from employee import views  
from employee.views import UserViewSet,DeptViewSet,EmpViewSet
from rest_framework.routers import DefaultRouter
'''
dept_list=DeptViewSet.as_view({'get':'list','post':'create'})
user_list=UserViewSet.as_view({'get':'list'})
dept_detail=DeptViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update'})
user_detail=UserViewSet.as_view({'get':'retrieve'})
'''
urlpatterns = [  
    path("",views.Loginpage.as_view(),name="login"),
    path("login",views.Login.as_view()),
    path("logout",views.Logout.as_view()),
    path("main",views.main),
    path("index/",views.index),
    path('admin/', admin.site.urls),  
    path('emp', views.emp), 
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),
    path('search',views.search),
    path('searchy/',views.searchy),
    path('add/',views.add),
    path('adddept',views.adddept),
    #path('dept',views.deptList.as_view(),name="dept-list"),
    #path('dept',dept_list,name="dept-list"),
    path('show_all',views.show_all),
    path('edit_dept',views.edit_dept),
    #path('dept/<int:pk>',views.dep_detail.as_view(),name="dept-detail"),
    #path('dept/<int:pk>/',views.dep_detail.as_view(),name="dep-detail"),
    #path('dept/<int:pk>',dept_detail,name="dept-detail"),
    #path('dept/<int:pk>/',dept_detail,name="dept-detail"),
    #path('emplist',views.empList.as_view(),name="emp-list"),
    #path('emp/<int:pk>',views.emp_detail.as_view(),name="employee-detail"),
    #path('users/', views.UserList.as_view(),name="user-list"),
    #path('users/<int:pk>/', views.UserDetail.as_view(),name="user-detail"),
    #path('users/',user_list,name="user-list"),
    #path('users/<int:pk>/', user_detail,name="user-detail"),
    #path('api',views.api_root)
    #path('search/<string:ename>',)
    path('dep_csv',views.try_csv_dept.as_view())
]  
urlpatterns=format_suffix_patterns(urlpatterns)

router = DefaultRouter()
router.register(r'dept', views.DeptViewSet,basename="dept")
router.register(r'users', views.UserViewSet,basename="user")
router.register(r'employee',views.EmpViewSet,basename="employee")

# The API URLs are now determined automatically by the router.
urlpatterns+= [
    path('api', include(router.urls)),
]
