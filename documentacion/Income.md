📨 1. Crear ingreso
Endpoint: POST /income/add/
Content-Type: multipart/form-data

🧾 Campos esperados:
Campo	Tipo	Requerido
responsible	string	✅
amount	decimal	✅
date	date	✅
reason	string	✅
payment_method	string	✅
observations	archivo	❌
voucher	string	❌
destination_account	integer	✅

🧪 Ejemplo (Postman form-data):
json
Copy
Edit
{
  "responsible": "Juan Pérez",
  "amount": "150000.00",
  "date": "2025-07-07",
  "reason": "Donación institucional",
  "payment_method": "Transferencia",
  "voucher": image,
  "destination_account": 1,
  "observations": "holi"
}
✅ Respuesta:
json

{
  "message": "Creado con exito",
  "id": 5
}
🔄 2. Actualizar ingreso
Endpoint: PATCH /incomes/update/<income_id>/


🧾 Campos aceptados:
Todos los campos son opcionales. Envía solo los que desees actualizar.

Campo	Tipo
responsible	string
date	date
reason	string
payment_method	string
observations	archivo
voucher	string
destination_account	integer

🧪 Ejemplo:
json

{
  "reason": "Corrección de motivo",
  "payment_method": "Efectivo"
}
✅ Respuesta:
json

{
  "message": "actualizado con exito"
}
📥 3. Obtener todos los ingresos
Endpoint: GET /income/

✅ Respuesta:
json

[
  {
    "id": 1,
    "responsible": "Juan Pérez",
    "amount": "150000.00",
    "date": "2025-07-07",
    "reason": "Donación institucional",
    "payment_method": "Transferencia",
    "observations": "Observaciones generales",
    "voucher": url",
    "destination_account": 1
  },
  ...
]
🔎 4. Obtener ingreso por ID
Endpoint: GET /income/<income_id>/

✅ Respuesta:
json

{
  "id": 5,
  "responsible": "Juan Pérez",
  "amount": "150000.00",
  "date": "2025-07-07",
  "reason": "Donación institucional",
  "payment_method": "Transferencia",
  "observations": "Observaciones generales",
  "voucher": url,
  "destination_account": 1
}