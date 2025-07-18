from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .Serializer import WorkOrderSerializer
from .models import WorkOrder
from .service import get_work_orders, get_work_order_by_id,create_pdf, create_work_order, update_work_order, get_work_order_whitout_certificate


# Create your views here.
class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    queryset = WorkOrder.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_work_order_view(request):
    try:
        data = request.data
        quote_id = data.get('quote_id')
        start_date = data.get('start_date')
        description = data.get('description')
        workplace = data.get('workplace')
        days_of_execution = data.get('days_of_execution')
        number_technicians = data.get('number_technicians')
        number_officers = data.get('number_officers')
        number_auxiliaries = data.get('number_auxiliaries')
        activity = data.get('activity')
        permissions = data.get('permissions')
        number_supervisors = data.get('number_supervisors')

        if not quote_id or not start_date or not workplace or not permissions or not activity or int(number_auxiliaries) < 0 or int(number_technicians) < 0 or int(number_officers) < 0 or int(number_supervisors) < 0 or not days_of_execution:
            return Response({'error': 'All fields are required'}, status=400)
        
        work_order = create_work_order(quote_id, start_date, days_of_execution, description, workplace, int(number_technicians), int(number_officers), int(number_auxiliaries), activity, permissions, int(number_supervisors))
        return Response({'message': 'Orden de trabajo creada exitosamente', 'id': work_order.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_work_order_view(request, id):
    try:
        data = request.data
        quote_id = data.get('quote_id')
        start_date = data.get('start_date')
        description = data.get('description')
        workplace = data.get('workplace')
        number_technicians = data.get('number_technicians')
        number_officers = data.get('number_officers')
        number_auxiliaries = data.get('number_auxiliaries')
        activity = data.get('activity')
        permissions = data.get('permissions')
        number_supervisors = data.get('number_supervisors')
        days_of_execution = data.get('days_of_execution')
        
        updated_work_order = update_work_order(
            id=id,
            quote_id=quote_id,
            start_date=start_date,
            description=description,
            workplace=workplace,
            number_technicians=number_technicians,
            number_officers=number_officers,
            number_auxiliaries=number_auxiliaries,
            activity=activity,
            permissions=permissions,
            number_supervisors=number_supervisors,
            days_of_execution=days_of_execution
        )

        return Response({'message': 'Orden de trabajo actualizada exitosamente', 'id': updated_work_order.id}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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
        response['Content-Disposition'] = f'attachment; filename="Orden-{work.quote.code}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
def get_work_order_whitout_certificate_view(request):
    try:
        work_orders = get_work_order_whitout_certificate()
        serializer = WorkOrderSerializer(work_orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
        
    

