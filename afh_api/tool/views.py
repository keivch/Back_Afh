from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tool
from .Serializer import ToolSerializer
import cloudinary
import cloudinary.uploader
from rest_framework.response import Response
from cloudinary.exceptions import Error
from .Services import createCodeTool, updateCodeTool

# Create your views here.
class ToolViewSet(viewsets.ModelViewSet):
    serializer_class = ToolSerializer
    queryset = Tool.objects.all()


@api_view(['POST'])
def addTool(request):
    try:
        name = request.data.get('name')
        imageFile = request.FILES.get('image')
        marca = request.data.get('marca')
        if not name or not marca:
            return Response({'error': 'Falta el nombre de la herramienta o la marca'}, status=400)
        if not imageFile:
            return Response({'error ': 'falta la imagen de la herramienta'}, status=404)
        valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if imageFile.content_type not in valid_image_types:
            return Response(
                {'error': 'Formato de imagen no válido. Solo se permiten JPEG, PNG, GIF o WEBP.'},
                status=400
            )
        code = createCodeTool(name)

        imageFile.seek(0)

        result = cloudinary.uploader.upload(imageFile, folder="afhimages/")

        imageUrl = result['secure_url']
        Tool.objects.create(
            name = name,
            image = imageUrl,
            code = code,
            marca = marca
        )

        return Response({'message': 'Herramienta creada con exito'}, status=201)
    except Exception as e:
        print(str(e))
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def updateTool(request):
    try:
        name = request.data.get('name')
        imageFile = request.FILES.get('image')
        state = request.data.get('state')
        id = request.data.get('id')
        marca = request.data.get('marca')

        tool = Tool.objects.filter(id=id).first()

        if name:
            code = updateCodeTool(name)
            tool.name = name
            tool.code = code
            tool.save()
        if imageFile:
            imageFile.seek(0)

            result = cloudinary.uploader.upload(imageFile, folder="afhimages/")

            imageUrl = result['secure_url']

            tool.image = imageUrl

            tool.save()
        if int(state) == 1:
            tool.state = 1
            tool.save()
        if int(state) == 2:
            tool.state = 2
            tool.save()
        if int(state) == 3:
            tool.state = 3
            tool.save()
        if int(state) == 4:
            tool.state = 4
            tool.save()
        if marca:
            tool.marca = marca
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
        if tool.state == 3 or tool.state == 4:
            return Response({'error': 'La herramienta no puede ser eliminada ya que esta en uso o reservada'}, status=400)

        tool.delete()
        return Response({'message': 'Herramienta eliminada con exito'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

            
            





    
