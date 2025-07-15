📘 API de Movimientos Financieros – Egresos
Modelo: Egress


Campos del modelo:

Campo	Tipo	Requerido	Descripción
responsible	string	✅	Nombre de la persona responsable
amount	decimal	✅	Monto del egreso
date	date	✅	Fecha del egreso (YYYY-MM-DD)
reason	string	✅	Motivo del egreso
payment_method	string	✅	Método de pago utilizado
observations	file o string	❌	Observaciones del egreso
voucher	string	❌	Código o referencia del comprobante
origin_account	integer	✅	1 = CUENTA BANCARIA, 2 = CAJA PRINCIPAL

📨 1. Crear egreso
Endpoint: POST /egress/add/


🧾 Campos esperados:
Campo	Tipo	Requerido
responsible	string	✅
amount	decimal	✅
date	date	✅
reason	string	✅
payment_method	string	✅
observations	archivo	❌
voucher	string	❌
origin_account	integer	✅

🧪 Ejemplo (form-data):

Edit
{
  "responsible": "Laura Gómez",
  "amount": "87500.00",
  "date": "2025-07-07",
  "reason": "Compra de suministros",
  "payment_method": "Efectivo",
  "voucher": field,
  "origin_account": 2,
  "observations": "oli"
}
✅ Respuesta:

{
  "message": "Creado con exito",
  "id": 7
}
🔄 2. Actualizar egreso
Endpoint: PATCH /egress/update/<egress_id>/
Content-Type: multipart/form-data

🧾 Campos aceptados:
Todos los campos son opcionales. Envía solo los que deseas modificar.

Campo	Tipo
responsible	string
date	date
reason	string
payment_method	string
observations	archivo
voucher	string
origin_account	integer

🧪 Ejemplo:

{
  "payment_method": "Transferencia",
  "reason": "Ajuste de motivo"
}
✅ Respuesta:
json

{
  "message": "Actualizado con exito"
}
📥 3. Obtener todos los egresos
Endpoint: GET /egress/

✅ Respuesta:
json
Copy
Edit
[
  {
    "id": 1,
    "responsible": "Laura Gómez",
    "amount": "87500.00",
    "date": "2025-07-07",
    "reason": "Compra de suministros",
    "payment_method": "Efectivo",
    "observations": "N/A",
    "voucher": url,
    "origin_account": 2
  },
  ...
]
🔎 4. Obtener egreso por ID
Endpoint: GET /egress/<egress_id>/

✅ Respuesta:
json
Copy
Edit
{
  "id": 7,
  "responsible": "Laura Gómez",
  "amount": "87500.00",
  "date": "2025-07-07",
  "reason": "Compra de suministros",
  "payment_method": "Efectivo",
  "observations": "Archivo adjunto o texto",
  "voucher": url,
  "origin_account": 2
}