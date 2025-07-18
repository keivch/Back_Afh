Obtener balance general por rango de fechas
Endpoint: GET /balans/get/
Descripción: Devuelve el total de ingresos, egresos y el balance (ingresos - egresos) para un rango de fechas.

📥 Parámetros (query params):
Nombre	Tipo	Requerido	Ejemplo
start	str	✅	2025-01-01
end	str	✅	2025-12-31

📤 Ejemplo de solicitud:

GET /balans/get/?start=2025-01-01&end=2025-12-31
📦 Respuesta:

{
  "total_ingresos": 1000000,
  "total_egresos": 750000,
  "balance": 250000
}
💳 2. Obtener ingresos o egresos agrupados por método de pago
Endpoint: GET /balans/get_by_method_of_paymenth/<option>/
Descripción: Devuelve ingresos o egresos agrupados por método de pago u origen de cuenta, según la opción seleccionada.

🧾 Parámetros en la ruta:
Nombre	Tipo	Requerido	Descripción	Ejemplo
option	int	✅	1 para ingresos, 2 para egresos	1


📦 Respuesta (si option = 1):

[
  {
    "payment_method": "EFECTIVO",
    "total": 300000,
    "cantidad": 5
  },
  {
    "payment_method": "TRANSFERENCIA",
    "total": 700000,
    "cantidad": 3
  }
]
📦 Respuesta (si option = 2):

[
  {
    "origin_account": 1,
    "total": 500000,
    "cantidad": 4
  },
  {
    "origin_account": 2,
    "total": 250000,
    "cantidad": 2
  }
]
📆 3. Obtener resumen mensual de ingresos, egresos y balance
Endpoint: GET /balans/mensual/
Descripción: Devuelve los ingresos, egresos y balance agrupados por mes, dentro de un rango de fechas.

📥 Parámetros (query params):
Nombre	Tipo	Requerido	Ejemplo
start	str	✅	2025-01-01
end	str	✅	2025-12-31

📤 Ejemplo de solicitud:
http
Copy
Edit
GET /balans/get_balans_monthly/?start=2025-01-01&end=2025-12-31
📦 Respuesta:

[
  {
    "mes": "Enero",
    "ingresos": 400000,
    "egresos": 200000,
    "balance": 200000
  },
  {
    "mes": "Febrero",
    "ingresos": 300000,
    "egresos": 300000,
    "balance": 0
  }
]
