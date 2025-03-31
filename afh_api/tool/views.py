from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tool
from .Serializer import ToolSerializer
import cloudinary
import cloudinary.uploader
from rest_framework.response import Response
from cloudinary.exceptions import Error




# Create your views here.
class ToolViewSet(viewsets.ModelViewSet):
    serializer_class = ToolSerializer
    queryset = Tool.objects.all()


@api_view(['POST'])
def addTool(request):
    try:
        name = request.data.get('name')
        imageFile = request.FILES.get('image')
        if not name:
            return Response({'error': 'Falta el nombre de la herramienta'}, status=400)
        if not imageFile:
            return Response({'error ': 'falta la imagen de la herramienta'}, status=404)
        valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if imageFile.content_type not in valid_image_types:
            return Response(
                {'error': 'Formato de imagen no válido. Solo se permiten JPEG, PNG, GIF o WEBP.'},
                status=400
            )
        initials = "".join([word[0].upper() for word in name.split()])
        toolNames = Tool.objects.filter(name__iexact=name).count()
        if toolNames < 1:
            code = initials + "-1"
        else:
            number = toolNames + 1
            code = f"{initials}-{number}"

        imageFile.seek(0)

        result = cloudinary.uploader.upload(imageFile, folder="afhimages/")

        imageUrl = result['secure_url']
        Tool.objects.create(
            name = name,
            image = imageUrl,
            code = code
        )

        return Response({'message': 'Herramienta creada con exito'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def updateTool(request):
    try:
        name = request.data.get('name')
        image = request.FILES.get('image')
        



    
