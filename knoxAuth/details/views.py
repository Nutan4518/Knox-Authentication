# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView,UpdateAPIView, DestroyAPIView,ListAPIView
from .models import *
from .serializers import *

# Create your views here.

#####create a new user
# class NewEmployeeAPI(CreateAPIView):
#     # permission_classes = [IsAuthenticated]
#     permission_classes = (AllowAny,)
#     queryset = Employee.objects.all()
#     serializer_class = NewEmployeeSerializer
   

class NewEmployeeAPI(APIView):
    # permission_classes = (AllowAny,)
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            # print(request.data)
            serializer = NewEmployeeSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# list all employees
# class ListEmployeeAPIView(generics.ListAPIView):
#     # permission_classes = [IsAuthenticated]

#     queryset = Employee.objects.all()
#     serializer_class = ListEmployeeSerializer

class ListEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ListEmployeeSerializer
    def get(self,request,format=None):
        if request.query_params:
            AllEmp = Employee.objects.filter(**request.query_params.dict())
        else:
            AllEmp = Employee.objects.all()
        if AllEmp:
            serializer = ListEmployeeSerializer(AllEmp, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

# #######       update employee details
# class UpdateEmployeeAPI(UpdateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = UpdateUserSerializer

class UpdateEmployeeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = UpdateUserSerializer(employee, data=request.data,partial =True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Employee updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# delete a particular employee
# class DeleteEmployeeAPIView(DestroyAPIView):
#     queryset = Employee.objects.all()
#     lookup_field = 'pk'  # The field to use for deleting the object, e.g., 'id' or 'Emp_id
   
class DeleteEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




