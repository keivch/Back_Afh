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
        imageFile = request.FILES.get('image')
        state = request.data.get('state')
        id = request.data.get('id')

        tool = Tool.objects.filter(id=id).first()

        if name:
            code = ""
            initials = "".join([word[0].upper() for word in name.split()])
            toolNames = Tool.objects.filter(name__iexact=name).count()
            if toolNames < 1:
                code = initials + "-1"
            else:
                number = toolNames + 1
                code = f"{initials}-{number}"
            tool.name = name
            tool.code = code
            tool.save()
        if imageFile:
            imageFile.seek(0)

            result = cloudinary.uploader.upload(imageFile, folder="afhimages/")

            imageUrl = result['secure_url']

            tool.image = imageUrl

            tool.save()
        if state == 2:
            tool.state = 2
            tool.save()
        if state == 3:
            tool.state = 3
            tool.save()
        return Response({'message': 'Herramienta actualizada exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def geTools(request):
    try:
        tools = Tool.objects.all()  
        serializer = ToolSerializer(tools, many=True)  
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def getToolById(request, tool_id):
    try:
        tool = Tool.objects.filter(id = tool_id).first()
        serializer = ToolSerializer(tool)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def deleteTool(request, tool_id):
    try:
        tool = Tool.objects.filter(id = tool_id).first()
        tool.delete()
        return Response({'message': 'Herramienta eliminada con exito'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

            
            





    
