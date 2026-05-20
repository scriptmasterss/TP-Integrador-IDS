# Biblioteca FIUBA 
**Plataforma web para la gestión de préstamos/reservas universitarios** — Proyecto Final Integrador  
Introducción al Desarrollo de Software · FIUBA · 2026

---

## Descripción

Sistema web para administrar préstamos de equipamiento técnico (placas electrónicas, libros, PCs, proyectores/pantalla de proyección y cables) entre alumnos/docentes y la biblioteca/laboratorios de la facultad.

Permite a los alumnos buscar materiales y solicitar préstamos/reservas, y a los administradores gestionar el inventario, aprobar solicitudes, generar QRs de entrega y exportar reportes de retraso en entrega en PDF.

---

## Integrantes

| Nombre                          | Padrón    |
|---------------------------------|-----------|
| Karla Vanesa Torres Pérez       | 114908    |
| Camila Delfino                  | 113552    |
| Sofía Belén Machuca             | 113873    |
| Patricio Xavier López Apolo     | 115353    |
| Erick Fernando Carvalho Sánchez | 115509    |
| Abril Chiara Berlot             | 114287    |

---

### Requisitos previos

- Node.js--->(https://nodejs.org/) v18 o superior
- npm v9 o superior

### Instalación y ejecución del mockup

```bash
# 1. Instalar dependencias
npm install

# 2. Levantar el servidor de desarrollo
npm run dev
```

El proyecto estará disponible en `http://localhost:5173` (o el puerto que indique la consola).

Incluye las siguientes pantallas:
- **Dashboard del administrador** — métricas, gráficos de demanda y tabla de préstamos/reservas
- **Inventario** — búsqueda y filtrado de materiales con estado de disponibilidad
- **Formulario de solicitud** — carga de datos y fechas del préstamo/reserva
- **Confirmación con QR** — detalle del préstamo/reserva y QR dinámico para escanear al retirar/devolver

---

## Licencia

Proyecto académico — FIUBA 2026
