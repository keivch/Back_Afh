from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .Serializer import DeliveryCertificateSerializer
from .models import Delivery_certificate
from .Service import create_delivery_certificarte, update_delivery_certificate, get_deliverys_certificates, get_delivery_certificate_by_id, add_exhibit_to_delivery_certificate, create_pdf

# Create your views here.
class DeliveryCertificateViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryCertificateSerializer
    queryset = Delivery_certificate.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_delivery_certificate_view(request):
    try:
        data = request.data
        work_order_id = data.get('work_order_id')
        observations = data.get('observations')
        recommendations = data.get('recommendations')
        exhibit_ids = data.get('exhibit_ids', [])
        description = data.get('description')
        development = data.get('development')
        in_charge = data.get('in_charge')
        post = data.get('post')
        if not work_order_id or not observations or not recommendations:
            return Response({'error': 'Todos los datos son requeridos'}, status=400)

        create_delivery_certificarte(work_order_id, observations, recommendations, exhibit_ids, description, development, in_charge, post)

        return Response({'message': 'Certificado de entrega creado exitosamente'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_delivery_certificate_view(request, id):
    try:
        data = request.data
        observations = data.get('observations')
        recommendations = data.get('recommendations')
        development = data.get('development')
        description = data.get('description')
        in_charge = data.get('in_charge')
        post = data.get('post')

        if not observations and not recommendations:
            return Response({'error': 'Debe proporcionar al menos una observación o recomendación'}, status=400)
        
        update_delivery_certificate(id, observations, recommendations, development, description, in_charge, post)

        return Response({'message': 'Certificado de entrega actualizado exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_delivery_certificates_view(request):
    try:
        delivery_certificates = get_deliverys_certificates()
        serializer = DeliveryCertificateSerializer(delivery_certificates, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_delivery_certificate_by_id_view(request, id):
    try:
        delivery_certificate = get_delivery_certificate_by_id(id)
        if not delivery_certificate:
            return Response({'error': 'Certificado de entrega no encontrado'}, status=404)
        
        serializer = DeliveryCertificateSerializer(delivery_certificate)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_exhibit_to_delivery_certificate_view(request, delivery_certificate_id, exhibit_id):
    try:
        delivery_certificate = add_exhibit_to_delivery_certificate(delivery_certificate_id, exhibit_id)
        if not delivery_certificate:
            return Response({'error': 'Certificado de entrega o exhibición no encontrado'}, status=404)
        
        serializer = DeliveryCertificateSerializer(delivery_certificate)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_pdf_view(request, id):
    try:
        buffer = create_pdf(id)
        if not buffer:
            return Response({'error': 'No se pudo generar el PDF'}, status=404)
        delivery = get_delivery_certificate_by_id(id)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado_entrega_{delivery.work_order.quote.code}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)