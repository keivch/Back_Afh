from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .Serializer import WorkOrderSerializer
from .models import WorkOrder
from .service import get_work_orders, get_work_order_by_id,create_pdf, finish_work


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
    

@api_view(['GET'])
def pdf_quote_view(request, id_workorder):
    try:
        if not id_workorder:
            return Response({'error': 'Id de la cotizacion es requerido'}, status=400)
        work = WorkOrder.objects.get(id=id_workorder)
        buffer = create_pdf(id_workorder)

        # Preparar respuesta como archivo descargable
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Orden-{work.Quotes.code}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def finish_work_view(request, id):
    try:
        if not id:
            return Response({'error': 'Id de la orden de trabajo es requerido'}, status=400)
        finish_work(id)
        return Response({'message': 'Orden de trabajo finalizada exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
        
    

