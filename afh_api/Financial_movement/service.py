from .models import Egress, Income
import cloudinary
import cloudinary.uploader
from decimal import Decimal

def upload_image(imagefield):
    if not imagefield:
        return None
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if imagefield.content_type not in valid_image_types:
        raise ValueError('Formato de imagen no válido. Solo se permiten JPEG, PNG, GIF o WEBP.')
    imagefield.seek(0)
    result = cloudinary.uploader.upload(imagefield, folder="afhimages/")
    return result['secure_url']

def create_egress(responsible, amount, date, reason, payment_method,  origin_account,  observations = None, voucher = None):
    try:
        amount = Decimal(amount)
        
        new_egress = Egress.objects.create(
            responsible = responsible,
            amount = amount,
            date = date,
            reason = reason,
            payment_method = payment_method, 
            origin_account = origin_account
        )

        if voucher:
            url = upload_image(voucher)
            new_egress.voucher = url
        if observations:
            new_egress.observations = observations
        new_egress.save()
        
        return new_egress
    except Exception as e:
        print("Error al crear el egreso:", str(e))
        raise e
    

def update_egress(id, responsible = None, date = None , reason = None, payment_method = None, observations = None, origin_account = None, voucher = None):
    try:
        egress = Egress.objects.get(id=id)

        if responsible:
            egress.responsible = responsible
        if date:
            egress.date = date
        if reason:
            egress.reason = reason
        if payment_method:
            egress.payment_method = payment_method
        if observations:
            egress.observations = observations
        if origin_account:
            egress.origin_account = origin_account
        if voucher:
            url = upload_image(voucher)
            egress.voucher = url
        
        egress.save()
    except Exception as e:
        print("Error el egreso:", str(e))
        raise e
    
def create_income(responsible, amount, date, reason,  destination_account, payment_method, observations = None, voucher = None):
    try:
        amount = Decimal(amount)

        new_income = Income.objects.create(
            responsible = responsible,
            amount = amount,
            date = date,
            reason = reason,
            payment_method = payment_method,
            destination_account = destination_account
        )

        if voucher:
            url = upload_image(voucher)
            new_income.voucher = url
        if observations:
            new_income.observations = observations
        new_income.save()

        return new_income
    except Exception as e:
        print("Error el egreso:", str(e))
        raise e

def update_income(id, responsible = None, date = None, reason = None, payment_method = None, observations = None, voucher = None,destination_account = None):
    try:
        
        income = Income.objects.get(id=id)

        if responsible:
            income.responsible = responsible
        if date:
            income.date = date
        if reason:
            income.reason = reason
        if payment_method:
            income.payment_method = payment_method
        if observations:
            income.observations = observations
        if voucher:
            url = upload_image(voucher)
            income.voucher = url
        if destination_account:
            income.destination_account = destination_account
        
        income.save()
    except Exception as e:
        print("Error el egreso:", str(e))
        raise e
    
def get_incomes():
    try:
        incomes = Income.objects.all()
        return incomes
    except Exception as e:
        return str(e)
    
def get_income_by_id(id):
    try:
        income = Income.objects.get(id=id)
        return income
    except Exception as e:
        return str(e)
    
def get_egress():
    try:
        egress = Egress.objects.all()
        return egress
    except Exception as e:
        return str(e)
    
def get_egress_by_id(id):

    try:
        egress = Egress.objects.get(id=id)
        return egress
    except Exception as e:
        return str(e)