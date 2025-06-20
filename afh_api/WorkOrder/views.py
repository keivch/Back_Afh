from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .Serializer import WorkOrderSerializer
from .models import WorkOrder
from .service import get_work_orders, get_work_order_by_id,create_pdf, create_work_order, update_work_order


# Create your views here.
class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    queryset = WorkOrder.objects.all()

@api_view(['POST'])
def create_work_order_view(request):
    try:
        data = request.data
        quote_id = data.get('quote_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        description = data.get('description')
        workplace = data.get('workplace')
        number_technicians = data.get('number_technicians')
        number_officers = data.get('number_officers')
        number_auxiliaries = data.get('number_auxiliaries')
        activity = data.get('activity')
        permissions = data.get('permissions')
        number_supervisors = data.get('number_supervisors')

        if not quote_id or not start_date or not workplace or not number_technicians or not activity or not permissions or not description or not number_officers or not number_auxiliaries or not number_supervisors:
            return Response({'error': 'All fields are required'}, status=400)
        
        work_order = create_work_order(quote_id, start_date, end_date, description, workplace, number_technicians, number_officers, number_auxiliaries, activity, permissions, number_supervisors)
        return Response({'message': 'Orden de trabajo creada exitosamente', 'id': work_order.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['PATCH'])
def update_work_order_view(request, id):
    try:
        data = request.data
        quote_id = data.get('quote_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        description = data.get('description')
        workplace = data.get('workplace')
        number_technicians = data.get('number_technicians')
        number_officers = data.get('number_officers')
        number_auxiliaries = data.get('number_auxiliaries')
        activity = data.get('activity')
        permissions = data.get('permissions')
        number_supervisors = data.get('number_supervisors')
        
        updated_work_order = update_work_order(
            id=id,
            quote_id=quote_id,
            start_date=start_date,
            end_date=end_date,
            description=description,
            workplace=workplace,
            number_technicians=number_technicians,
            number_officers=number_officers,
            number_auxiliaries=number_auxiliaries,
            activity=activity,
            permissions=permissions,
            number_supervisors=number_supervisors
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
    
        
    

