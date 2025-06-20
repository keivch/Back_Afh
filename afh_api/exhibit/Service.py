from .models import Exhibit
import cloudinary
import cloudinary.uploader


def upload_image(imagefield):
    if not imagefield:
        return None
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if imagefield.content_type not in valid_image_types:
        raise ValueError('Formato de imagen no válido. Solo se permiten JPEG, PNG, GIF o WEBP.')
    imagefield.seek(0)
    result = cloudinary.uploader.upload(imagefield, folder="afhimages/")
    return result['secure_url']

def create_exhibit(tittle, imagefield=None):
    try:

        urls = []
        for image in imagefield:
            urls.append(upload_image(image))

        
        exhibit = Exhibit.objects.create(
            tittle=tittle,
            images=urls
        )
        return exhibit
    except Exception as e:
        print(f"Error creating exhibit: {str(e)}")
        return None
    
def update_exhibit(id, tittle=None, imagefield=None):
    try:
        exhibit = Exhibit.objects.get(id=id)
        if tittle is not None:
            exhibit.tittle = tittle
        if imagefield is not None:
            urls = []
            for image in imagefield:
                urls.append(upload_image(image))
            exhibit.images = urls
        exhibit.save()
        return exhibit
    except Exception as e:
        print(f"Error updating exhibit: {str(e)}")
        return None
    
def get_exhibits():
    try:
        exhibits = Exhibit.objects.all()
        return exhibits
    except Exception as e:
        print(f"Error retrieving exhibits: {str(e)}")
        return None
    
def get_exhibit_by_id(id):
    try:
        exhibit = Exhibit.objects.get(id=id)
        return exhibit
    except Exhibit.DoesNotExist:
        print("Exhibit not found")
        return None
    except Exception as e:
        print(f"Error retrieving exhibit: {str(e)}")
        return None
