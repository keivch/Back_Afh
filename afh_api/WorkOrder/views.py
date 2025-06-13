from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .Serializer import WorkOrderSerializer
from .models import WorkOrder
from .service import get_work_orders, get_work_order_by_id


# Create your views here.
class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    queryset = WorkOrder.objects.all()

@api_view(['GET'])
def get_work_orders_view(request):
    try:
        orders = get_work_orders()
        serializer = WorkOrderSerializer(orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_work_order_by_id_view(request, id):
    try:
        work_order = get_work_order_by_id(id)
        serializer = WorkOrderSerializer(work_order)
        return Response(serializer.data)
    except WorkOrder.DoesNotExist:
        return Response({'error': 'Work order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

