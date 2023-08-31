from rest_framework import serializers
from .models import *




class NewEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = { 
            'empId':{'required':True},
            'password':{'required':True}
            }

    def validate(self, attrs):
        email= attrs.get('email','').strip().lower()
        emp_id = attrs.get('empId', '') 
        if Employee.objects.filter(email = email).exists():
            raise serializers.ValidationError('User with this email is already exists')
        if Employee.objects.filter(empId=emp_id).exists():
            raise serializers.ValidationError('Employee with this Emp_id is already exists')
        return attrs

    def create(self, validated_data):
        user = Employee.objects.create(**validated_data)
        user.save()
        return user




class ListEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'



class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    
    def update(self, instance, validated_data):
        password = validated_data.pop('EmpId',None)
        # if password:
        #     instance.set_password('EmpId')
        instance = super().update(instance, validated_data)
        instance.save()
        return instance
    
