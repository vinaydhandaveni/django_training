from django.shortcuts import render,redirect 
from django.http import HttpResponse, JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status,mixins,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from .serializers import DeptSerializer,EmployeeSerializer,UserSerializer
from .models import Employee,Dept
from itertools import chain
from rest_framework.views import APIView
from django.db import connection
from django.views import View
from django.contrib.auth.models import User
from rest_framework import permissions,viewsets
from .permissions import isowner_readonly
from rest_framework.reverse import reverse
import csv
class try_csv_dept(View):
    def get(self,request):
        response=HttpResponse(
            content_type='text/csv',headers={"Content-Disposition":'attachment; filename="dept.csv"',}
        )
        writer=csv.writer(response)
        writer.writerow(["DeptNo","DeptName"])
        depts=Dept.objects.all()
        for d in depts:
            writer.writerow([d.edept,d.edepname])
        return response

# Create your views here.
def emp(request): #add employee 
    D=Dept.objects.get(edept=request.POST["edept"]) 
    q=Employee(ename=request.POST["name"],eid=request.POST["eno"],econtact=request.POST["con"],eemail=request.POST["email"],edept=D)
    q.save()
    return render(request,'employee/main.html',{})  

def main(request):
    return render(request,'employee/main.html',{})

def index(request):  #input for a new employee
    return render(request,"employee/index.html",{})

def show(request):  #show all employee details
    #to display all the employee details based on employee id
    employees = Employee.objects.all().order_by("eid")
    return render(request,"employee/show.html",{'employees':employees}) 
 
def searchy(request): #input for id to search an employee
    return render(request,"employee/search.html",{})

def add(request):#input to add dept
    #dept=Dept.objects.get.all()
    return render(request,"employee/add_dept.html",{})

def edit(request, id):  #edit employee
    employee = Employee.objects.get(id=id)  
    return render(request,'employee/edit.html', {'employee':employee}) 

def destroy(request, id):  #delete employee 
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show") 

def update(request, id):  #update employee details
    employee = Employee.objects.get(id=id)  
    employee.ename=request.POST["ename"]
    employee.eemail=request.POST["eemail"]
    employee.econtact=request.POST["econtact"]
    employee.eid=request.POST["eid"]
    employee.edept=request.POST["edept"]
    employee.save()
    employees=Employee.objects.all()
    return render(request,"employee/show.html",{'employees':employees}) 

def search(request):#search an employee in db
    idn=request.POST["itsid"]
    emp=[Employee.objects.get(eid=idn)]
    return render(request,"employee/show.html",{'employees':emp})

def adddept(request):#adding department to db
    d=Dept(edept=request.POST["did"],edepname=request.POST["dname"])
    d.save()
    return render(request,"employee/main.html",{})

def edit_dept(request):
    return render(request,"employee/edit_dept.html",{})

'''def show_dept(request):#showing department details
    depart = Dept.objects.all()  
    return render(request,"employee/show_depts.html",{'departments':depart})'''

def show_all(request):#employee details along with depatment name
    List1=[]
    obje=Employee.objects.all().order_by("eid")
    depts=Dept.objects.all()
    for obj in obje:
        all_details=dict()
        dep=depts.get(edept=obj.edept)
        all_details["empid"]=obj.eid
        all_details["empname"]=obj.ename
        all_details["empcontact"]=obj.econtact
        all_details["empemail"]=obj.eemail
        all_details["deptname"]=dep.edepname
        List1.append(all_details)
    return render(request,"employee/show_all.html",{"all_det":List1})
''' #not working
def showy(request):
    c=connection.cursor()
    all_d=[c.execute("select e.eid,e.ename,e.econtact,e.eemail,d.edepname from Employee e,Dept d where e.edept=d.edept")]
    return render(request,"employee/show_all.html",{"all_det":all_d})
'''
#Function based API Views
'''
@api_view(['GET', 'POST'])
def dept_list(request,format=None):
    if request.method=='GET':
        #Dept=Dept.objects.all()
        serializer=DeptSerializer(Dept.objects.all(),many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializer=DeptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    '''

'''@api_view(['GET','PUT','DELETE'])
def dept_detail(request,pk,format=None):
    try:
        d = Dept.objects.get(pk=pk)
    except Dept.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = DeptSerializer(d)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = DeptSerializer(d, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        d.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    '''
#Class based API VIews
'''
class DeptList(APIView):
    def get(self,request,format=None):
        d=Dept.objects.all()
        ser=DeptSerializer(d,many=True)
        return Response(ser.data)
    def post(self,request,format=None):
        ser=DeptSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.data,status=status.HTTP_400_BAD_REQUEST)

class Dept_details(APIView):
    def get_object(self,pk):
        try:
            d=Dept.objects.get(pk=pk)
            return d
        except:
            raise Http404
        
    def get(self,request,pk,format=None):
        d=self.get_object(pk)
        ser=DeptSerializer(d)
        return Response(ser.data)
    
    def put(self,request,pk,format=None):
        d=self.get_object(pk)
        serializer = DeptSerializer(d, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        dep = self.get_object(pk)
        serializer = DeptSerializer(dep,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        d=Dept.objects.get(pk=pk)
        d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  '''
#Using Mixins for APIs    
'''
class deptList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    queryset=Dept.objects.all()
    serializer_class=DeptSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    

class dep_detail(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset=Dept.objects.all()
    serializer_class=DeptSerializer
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
'''
#Using GenericAPIViews
'''
class deptList(generics.ListCreateAPIView):
    queryset=Dept.objects.all()
    serializer_class=DeptSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class dep_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Dept.objects.all()
    serializer_class=DeptSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,isowner_readonly]

'''
'''
class empList(generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class emp_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,isowner_readonly]
#   User API Views
'''
'''
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''
'''
@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'users list':reverse('user-list',request=request,format=format),'department list': reverse('dept-list',request=request,format=format),
        'employee-list':reverse('emp-list',request=request,format=format)
    })
'''

#Using ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class DeptViewSet(viewsets.ModelViewSet):
    queryset=Dept.objects.all()
    serializer_class=DeptSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EmpViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)