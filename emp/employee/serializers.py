from rest_framework import serializers
from .models import Employee,Dept
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    department= serializers.HyperlinkedRelatedField(many=True, view_name='dept-detail',read_only=True)
    class Meta:
        model = User
        fields = ['url','id', 'username', 'department']

class DeptSerializer(serializers.HyperlinkedModelSerializer):
    '''id=serializers.IntegerField(read_only=True)
    edept=serializers.CharField(max_length=20)
    edepname=serializers.CharField(max_length=20)

    def create(self,validated_data):
        return Dept.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.edept=validated_data.get('edept',instance.edept)
        instance.edepname=validated_data.get('edepname',instance.edepname)
        instance.save()
        return instance'''
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Dept
        fields=['url','owner','edept','edepname']
    
class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    ''' id=serializers.IntegerField(read_only=True)
    eid=serializers.CharField(required=True,max_length=20)
    ename=serializers.CharField(max_length=20)
    eemail = serializers.EmailField()  
    edept= serializers.CharField(max_length=20)
    econtact = serializers.CharField(max_length=15) '''
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Employee
        fields=['url','owner','eid','ename','econtact','eemail','edept']
    '''def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.eid=validated_data.get('eid',instance.eid)
        instance.ename=validated_data.get('ename',instance.ename)
        instance.eemail=validated_data.get('eemail',instance.eemail)
        instance.edept=validated_data.get('edept',instance.edept)
        instance.econtact=validated_data.get('econtact',instance.econtact)
        instance.save()
        return instance'''
