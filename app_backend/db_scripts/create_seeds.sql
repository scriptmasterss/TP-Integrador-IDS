USE sistema_prestamos;

SET
  NAMES utf8mb4;

SET
  time_zone = '-03:00';

SET
  lc_time_names = 'es_ES';

SET
  FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE estado_devuelto;

TRUNCATE TABLE penalizacion;

TRUNCATE TABLE reserva;

TRUNCATE TABLE articulos;

TRUNCATE TABLE usuario;

TRUNCATE TABLE faq;

TRUNCATE TABLE normativa;

SET
  FOREIGN_KEY_CHECKS = 1;

-- Hash para la contraseña "password"
SET
  @dummy_hash = '$2b$12$.yNicNI/5TBWFR.cxzZyculiuEX/6lsgU/4V8um308AtCNfpDasm2';

-- =========================================================================
-- 1. USUARIOS (26 filas)
-- =========================================================================
INSERT INTO
  usuario (
    id,
    nombre,
    email,
    rol,
    carrera,
    contrasenia_hash,
    activo
  )
VALUES
  (
    1,
    'Juan Perez',
    'juan.perez@universidad.edu',
    'alumno',
    'Ingeniería en Informática',
    @dummy_hash,
    TRUE
  ),
  (
    2,
    'Ana Gomez',
    'ana.gomez@universidad.edu',
    'alumno',
    'Ingeniería Electrónica',
    @dummy_hash,
    TRUE
  ),
  (
    3,
    'Carlos Ruiz',
    'carlos.ruiz@universidad.edu',
    'profesor',
    'Ingeniería Mecánica',
    @dummy_hash,
    TRUE
  ),
  (
    4,
    'Laura Sol',
    'laura.sol@universidad.edu',
    'bibliotecario',
    'Desconocido',
    @dummy_hash,
    TRUE
  ),
  (
    5,
    'Admin User',
    'admin@universidad.edu',
    'admin',
    'Desconocido',
    @dummy_hash,
    TRUE
  ),
  (
    6,
    'Pedro Inactivo',
    'pedro.inactivo@universidad.edu',
    'alumno',
    'Ingeniería Química',
    @dummy_hash,
    FALSE
  ),
  (
    7,
    'María Rodríguez',
    'maria.rodriguez@universidad.edu',
    'alumno',
    'Ingeniería Civil',
    @dummy_hash,
    TRUE
  ),
  (
    8,
    'Diego Fernandez',
    'diego.fernandez@universidad.edu',
    'alumno',
    'Ingeniería Industrial',
    @dummy_hash,
    TRUE
  ),
  (
    9,
    'Patricia Lopez',
    'patricia.lopez@universidad.edu',
    'profesor',
    'Bioingeniería',
    @dummy_hash,
    TRUE
  ),
  (
    10,
    'Javier Martinez',
    'javier.martinez@universidad.edu',
    'alumno',
    'Lic. en Análisis de Sistemas',
    @dummy_hash,
    TRUE
  ),
  (
    11,
    'Elena Gomez',
    'elena.gomez@universidad.edu',
    'alumno',
    'Ingeniería en Alimentos',
    @dummy_hash,
    TRUE
  ),
  (
    12,
    'Ricardo Diaz',
    'ricardo.diaz@universidad.edu',
    'profesor',
    'Ingeniería en Petróleo',
    @dummy_hash,
    TRUE
  ),
  (
    13,
    'Sonia Alvarez',
    'sonia.alvarez@universidad.edu',
    'bibliotecario',
    'Desconocido',
    @dummy_hash,
    TRUE
  ),
  (
    14,
    'Lucas Benitez',
    'lucas.benitez@universidad.edu',
    'alumno',
    'Ingeniería en Energía Eléctrica',
    @dummy_hash,
    TRUE
  ),
  (
    15,
    'Clara Romero',
    'clara.romero@universidad.edu',
    'alumno',
    'Ingeniería en Agrimensura',
    @dummy_hash,
    TRUE
  ),
  (
    16,
    'Martin Silva',
    'martin.silva@universidad.edu',
    'alumno',
    'Ingeniería Naval',
    @dummy_hash,
    TRUE
  ),
  (
    17,
    'Sofia Castro',
    'sofia.castro@universidad.edu',
    'alumno',
    'Ingeniería en Informática',
    @dummy_hash,
    TRUE
  ),
  (
    18,
    'Alejandro Sosa',
    'alejandro.sosa@universidad.edu',
    'profesor',
    'Ingeniería Electrónica',
    @dummy_hash,
    TRUE
  ),
  (
    19,
    'Gabriela Medina',
    'gabriela.medina@universidad.edu',
    'alumno',
    'Ingeniería Industrial',
    @dummy_hash,
    TRUE
  ),
  (
    20,
    'Tomas Herrera',
    'tomas.herrera@universidad.edu',
    'alumno',
    'Ingeniería Mecánica',
    @dummy_hash,
    FALSE
  ),
  (
    21,
    'Nicolas Flores',
    'nicolas.flores@universidad.edu',
    'alumno',
    'Lic. en Análisis de Sistemas',
    @dummy_hash,
    TRUE
  ),
  (
    22,
    'Valeria Ortiz',
    'valeria.ortiz@universidad.edu',
    'alumno',
    'Bioingeniería',
    @dummy_hash,
    TRUE
  ),
  (
    23,
    'Daniel Mendez',
    'daniel.mendez@universidad.edu',
    'profesor',
    'Ingeniería Química',
    @dummy_hash,
    TRUE
  ),
  (
    24,
    'Florencia Blanco',
    'florencia.blanco@universidad.edu',
    'alumno',
    'Ingeniería Civil',
    @dummy_hash,
    TRUE
  ),
  (
    25,
    'Andres Acosta',
    'andres.acosta@universidad.edu',
    'alumno',
    'Ingeniería en Petróleo',
    @dummy_hash,
    TRUE
  ),
  (
    26,
    'Mariana Rios',
    'mariana.rios@universidad.edu',
    'bibliotecario',
    'Desconocido',
    @dummy_hash,
    TRUE
  );

-- =========================================================================
-- 2. ARTÍCULOS (26 filas)
-- =========================================================================
INSERT INTO
  articulos (
    id,
    nombre,
    tipo,
    seccion,
    stock,
    necesita_reparacion,
    activo
  )
VALUES
  (
    1,
    'Multímetro Digital',
    'Herramienta',
    'Laboratorio 1',
    5,
    FALSE,
    TRUE
  ),
  (
    2,
    'Osciloscopio',
    'Electrónica',
    'Laboratorio 1',
    2,
    TRUE,
    TRUE
  ),
  (
    3,
    'Cámara Térmica',
    'Instrumento',
    'Almacén',
    1,
    FALSE,
    TRUE
  ),
  (
    4,
    'Set Destornilladores',
    'Herramienta',
    'Taller',
    10,
    FALSE,
    TRUE
  ),
  (
    5,
    'Proyector',
    'Multimedia',
    'Biblioteca',
    3,
    FALSE,
    TRUE
  ),
  (
    6,
    'Tablet Antigua',
    'Electrónica',
    'Desuso',
    1,
    TRUE,
    FALSE
  ),
  (
    7,
    'Generador de Funciones',
    'Electrónica',
    'Laboratorio 1',
    3,
    FALSE,
    TRUE
  ),
  (
    8,
    'Soldador de Estaño',
    'Herramienta',
    'Taller',
    8,
    FALSE,
    TRUE
  ),
  (
    9,
    'Fuente de Alimentación Regulable',
    'Electrónica',
    'Laboratorio 2',
    4,
    FALSE,
    TRUE
  ),
  (
    10,
    'Calibre Digital',
    'Instrumento',
    'Taller',
    6,
    FALSE,
    TRUE
  ),
  (
    11,
    'Notebook I7',
    'Computación',
    'Biblioteca',
    5,
    FALSE,
    TRUE
  ),
  (
    12,
    'Analizador de Redes',
    'Telecomunicaciones',
    'Laboratorio 3',
    1,
    FALSE,
    TRUE
  ),
  (
    13,
    'Impresora 3D Portable',
    'Prototipado',
    'Taller',
    2,
    TRUE,
    TRUE
  ),
  (
    14,
    'Kit de Sensores Arduino',
    'Electrónica',
    'Laboratorio 1',
    12,
    FALSE,
    TRUE
  ),
  (
    15,
    'Nivel Óptico',
    'Medición',
    'Almacén Topografía',
    2,
    FALSE,
    TRUE
  ),
  (
    16,
    'Pistola de Calor',
    'Herramienta',
    'Taller',
    3,
    FALSE,
    TRUE
  ),
  (
    17,
    'Gafas de Realidad Virtual',
    'Multimedia',
    'Gabinete IT',
    2,
    FALSE,
    TRUE
  ),
  (
    18,
    'Deshumidificador de Ambiente',
    'Mantenimiento',
    'Almacén',
    2,
    FALSE,
    TRUE
  ),
  (
    19,
    'Balanza de Precisión',
    'Medición',
    'Laboratorio Química',
    3,
    FALSE,
    TRUE
  ),
  (
    20,
    'Viscosímetro',
    'Instrumento',
    'Laboratorio Química',
    1,
    FALSE,
    TRUE
  ),
  (
    21,
    'Tacómetro Digital',
    'Medición',
    'Taller Mecánica',
    2,
    FALSE,
    TRUE
  ),
  (
    22,
    'Durometro',
    'Instrumento',
    'Taller Mecánica',
    1,
    FALSE,
    TRUE
  ),
  (
    23,
    'Punta de Prueba Lógica',
    'Electrónica',
    'Laboratorio 2',
    15,
    FALSE,
    TRUE
  ),
  (
    24,
    'Microscopio Digital',
    'Instrumento',
    'Laboratorio Bio',
    3,
    FALSE,
    TRUE
  ),
  (
    25,
    'Placa de Desarrollo FPGA',
    'Electrónica',
    'Laboratorio 3',
    5,
    FALSE,
    TRUE
  ),
  (
    26,
    'Monitor de Gases',
    'Seguridad',
    'Almacén',
    2,
    TRUE,
    FALSE
  );

-- =========================================================================
-- 3. RESERVAS (25 filas)
-- Solo los IDs del 11 al 22 tendrán estado 'devuelto' y poblarán estado_devuelto
-- =========================================================================
INSERT INTO
  reserva (
    id,
    id_usuario,
    id_articulo,
    estado_reserva,
    fecha_retiro,
    fecha_regreso
  )
VALUES
  (
    1,
    1,
    1,
    'entregado',
    '2026-06-15 09:00:00',
    '2026-06-22 18:00:00'
  ),
  (
    2,
    2,
    2,
    'pendiente',
    '2026-06-20 10:00:00',
    '2026-06-22 10:00:00'
  ),
  (
    3,
    3,
    4,
    'aprobado',
    '2026-06-18 14:00:00',
    '2026-06-25 14:00:00'
  ),
  (
    4,
    7,
    5,
    'rechazado',
    '2026-06-01 09:00:00',
    '2026-06-02 09:00:00'
  ),
  (
    5,
    8,
    7,
    'cancelado',
    '2026-06-10 11:00:00',
    '2026-06-12 11:00:00'
  ),
  (
    6,
    10,
    9,
    'entregado',
    '2026-06-14 08:30:00',
    '2026-06-19 12:00:00'
  ),
  (
    7,
    11,
    11,
    'aprobado',
    '2026-06-19 09:00:00',
    '2026-06-21 17:00:00'
  ),
  (
    8,
    14,
    14,
    'pendiente',
    '2026-06-24 10:00:00',
    '2026-06-26 10:00:00'
  ),
  (
    9,
    15,
    15,
    'pendiente',
    '2026-06-25 08:00:00',
    '2026-06-25 18:00:00'
  ),
  (
    10,
    16,
    16,
    'rechazado',
    '2026-06-05 14:00:00',
    '2026-06-07 14:00:00'
  ),
  (
    11,
    1,
    3,
    'devuelto',
    '2026-05-10 08:00:00',
    '2026-05-12 08:00:00'
  ),
  (
    12,
    7,
    8,
    'devuelto',
    '2026-05-15 10:00:00',
    '2026-05-17 10:00:00'
  ),
  (
    13,
    8,
    10,
    'devuelto',
    '2026-05-20 09:00:00',
    '2026-05-22 09:00:00'
  ),
  (
    14,
    10,
    11,
    'devuelto',
    '2026-05-25 14:00:00',
    '2026-05-28 14:00:00'
  ),
  (
    15,
    17,
    17,
    'devuelto',
    '2026-06-01 09:00:00',
    '2026-06-03 17:00:00'
  ),
  (
    16,
    19,
    19,
    'devuelto',
    '2026-06-02 08:00:00',
    '2026-06-04 12:00:00'
  ),
  (
    17,
    21,
    23,
    'devuelto',
    '2026-06-05 11:00:00',
    '2026-06-05 16:00:00'
  ),
  (
    18,
    22,
    24,
    'devuelto',
    '2026-06-06 09:30:00',
    '2026-06-08 09:30:00'
  ),
  (
    19,
    24,
    25,
    'devuelto',
    '2026-06-08 13:00:00',
    '2026-06-10 13:00:00'
  ),
  (
    20,
    25,
    14,
    'devuelto',
    '2026-06-10 10:00:00',
    '2026-06-12 10:00:00'
  ),
  (
    21,
    2,
    1,
    'devuelto',
    '2026-06-11 09:00:00',
    '2026-06-13 09:00:00'
  ),
  (
    22,
    14,
    4,
    'devuelto',
    '2026-06-12 15:00:00',
    '2026-06-14 15:00:00'
  ),
  (
    23,
    17,
    13,
    'entregado',
    '2026-06-16 10:00:00',
    '2026-06-20 10:00:00'
  ),
  (
    24,
    19,
    21,
    'aprobado',
    '2026-06-19 08:00:00',
    '2026-06-22 12:00:00'
  ),
  (
    25,
    21,
    9,
    'cancelado',
    '2026-06-12 09:00:00',
    '2026-06-14 09:00:00'
  );

-- =========================================================================
-- 4. ESTADO DEVUELTO (25 filas)
-- Relacionado dinámicamente con registros devueltos o testeos de incidencias anteriores
-- =========================================================================
INSERT INTO
  estado_devuelto (id, id_reserva, dias_retraso, condiciones)
VALUES
  (1, 11, 0, 'Excelente estado'),
  (2, 11, 2, 'Ligeros rasguños en la carcasa'),
  (3, 12, 0, 'Limpio y operativo'),
  (4, 13, 1, 'Caja de transporte levemente dañada'),
  (5, 14, 0, 'Sin novedades, software intacto'),
  (6, 15, 0, 'Completo con cables correspondientes'),
  (
    7,
    16,
    3,
    'Sucio, requiere limpieza en laboratorio'
  ),
  (8, 17, 0, 'Perfecto estado físico y funcional'),
  (
    9,
    18,
    0,
    'Devuelto a término, batería cargada'
  ),
  (
    10,
    19,
    0,
    'Caja de empaque original arrugada, equipo bien'
  ),
  (
    11,
    20,
    0,
    'Falta un cable puente del kit, usuario notificado'
  ),
  (
    12,
    21,
    5,
    'Retraso por olvido de entrega, equipo ok'
  ),
  (13, 22, 0, 'Herramientas completas'),
  (14, 11, 0, 'Re-inspeccionado por el supervisor'),
  (15, 12, 0, 'Devolución estándar exitosa'),
  (
    16,
    13,
    0,
    'Validado por el laboratorio de petróleos'
  ),
  (17, 14, 0, 'Cargador con marcas de uso severas'),
  (18, 15, 1, 'Entrega en mostrador fuera de hora'),
  (19, 16, 0, 'Condiciones óptimas'),
  (20, 17, 0, 'Ok'),
  (
    21,
    18,
    0,
    'Inspeccionado por el docente a cargo'
  ),
  (22, 19, 0, 'Sin fallas'),
  (23, 20, 0, 'Equipo reingresado a estante A3'),
  (24, 21, 0, 'Entregado sin protector de goma'),
  (25, 22, 2, 'Demora por feriado institucional');

-- =========================================================================
-- 5. PENALIZACIONES (25 filas)
-- Vinculado a usuarios y reservas existentes de manera lógica
-- =========================================================================
INSERT INTO
  penalizacion (
    id,
    id_usuario,
    id_reserva,
    motivo,
    fecha_inicio,
    fecha_fin,
    activa,
    severidad
  )
VALUES
  (
    1,
    1,
    11,
    'Devolución tardía de equipo',
    '2026-05-12 09:00:00',
    '2026-05-20 09:00:00',
    FALSE,
    'baja'
  ),
  (
    2,
    7,
    4,
    'Uso indebido de solicitud',
    '2026-06-01 10:00:00',
    '2026-07-01 10:00:00',
    TRUE,
    'media'
  ),
  (
    3,
    8,
    13,
    'Retraso de 1 día en entrega de calibre',
    '2026-05-23 08:00:00',
    '2026-05-26 08:00:00',
    FALSE,
    'baja'
  ),
  (
    4,
    19,
    16,
    'Retraso de 3 días e instrumental sucio',
    '2026-06-07 13:00:00',
    '2026-06-21 13:00:00',
    TRUE,
    'media'
  ),
  (
    5,
    2,
    21,
    'Demora crítica de 5 días en entrega',
    '2026-06-18 10:00:00',
    '2026-07-02 10:00:00',
    TRUE,
    'alta'
  ),
  (
    6,
    14,
    22,
    'Entrega fuera de término recurrente',
    '2026-06-16 16:00:00',
    '2026-06-23 16:00:00',
    TRUE,
    'baja'
  ),
  (
    7,
    10,
    14,
    'No reportar falla física al retirar',
    '2026-05-29 09:00:00',
    '2026-06-05 09:00:00',
    FALSE,
    'baja'
  ),
  (
    8,
    15,
    9,
    'Falta a cita de retiro aprobada sin aviso',
    '2026-06-26 08:00:00',
    '2026-07-03 08:00:00',
    TRUE,
    'baja'
  ),
  (
    9,
    16,
    10,
    'Intento de reserva con datos falseados',
    '2026-06-06 09:00:00',
    '2026-07-06 09:00:00',
    TRUE,
    'alta'
  ),
  (
    10,
    25,
    20,
    'Falta de componente menor en Kit Arduino',
    '2026-06-13 11:00:00',
    '2026-06-20 11:00:00',
    TRUE,
    'baja'
  ),
  (
    11,
    1,
    1,
    'Descarga total de batería destructiva',
    '2026-06-23 09:00:00',
    '2026-07-23 09:00:00',
    TRUE,
    'media'
  ),
  (
    12,
    11,
    7,
    'Negativa a devolver en fecha pactada',
    '2026-06-22 08:00:00',
    '2026-07-06 08:00:00',
    TRUE,
    'media'
  ),
  (
    13,
    24,
    19,
    'Daño menor cosmético en carcasa FPGA',
    '2026-06-11 14:00:00',
    '2026-06-18 14:00:00',
    FALSE,
    'baja'
  ),
  (
    14,
    22,
    18,
    'Retraso administrativo de entrega',
    '2026-06-09 10:00:00',
    '2026-06-12 10:00:00',
    FALSE,
    'baja'
  ),
  (
    15,
    17,
    15,
    'Entrega fuera de hora de atención',
    '2026-06-04 18:00:00',
    '2026-06-07 18:00:00',
    FALSE,
    'baja'
  ),
  (
    16,
    21,
    17,
    'Falta de limpieza en visor VR',
    '2026-06-06 09:00:00',
    '2026-06-10 09:00:00',
    FALSE,
    'baja'
  ),
  (
    17,
    10,
    6,
    'Negativa a firmar acta de retiro',
    '2026-06-15 13:00:00',
    '2026-06-22 13:00:00',
    TRUE,
    'baja'
  ),
  (
    18,
    3,
    3,
    'Olvido de instrumental en aula común',
    '2026-06-26 15:00:00',
    '2026-07-10 15:00:00',
    TRUE,
    'media'
  ),
  (
    19,
    8,
    5,
    'Cancelación tardía sobre la hora',
    '2026-06-11 09:00:00',
    '2026-06-14 09:00:00',
    FALSE,
    'baja'
  ),
  (
    20,
    17,
    23,
    'Maltrato a impresora 3D (atasco forzado)',
    '2026-06-21 11:00:00',
    '2026-08-21 11:00:00',
    TRUE,
    'alta'
  ),
  (
    21,
    19,
    24,
    'Devolución por terceros sin autorización',
    '2026-06-23 09:00:00',
    '2026-06-30 09:00:00',
    TRUE,
    'baja'
  ),
  (
    22,
    7,
    12,
    'Manchas de grasa en manual de usuario',
    '2026-05-18 09:00:00',
    '2026-05-21 09:00:00',
    FALSE,
    'baja'
  ),
  (
    23,
    14,
    8,
    'Petición reiterada de extensión denegada',
    '2026-06-25 11:00:00',
    '2026-07-02 11:00:00',
    TRUE,
    'baja'
  ),
  (
    24,
    2,
    2,
    'No presentarse al laboratorio a la hora fijada',
    '2026-06-21 08:00:00',
    '2026-06-24 08:00:00',
    TRUE,
    'baja'
  ),
  (
    25,
    1,
    3,
    'Acumulación de advertencias menores',
    '2026-06-19 12:00:00',
    '2026-07-03 12:00:00',
    TRUE,
    'media'
  );

-- =========================================================================
-- 6. FAQ (25 filas)
-- =========================================================================
INSERT INTO
  faq (id, titulo, descripcion)
VALUES
  (
    1,
    '¿Cómo reservar?',
    'Seleccione el artículo y pulse solicitar.'
  ),
  (2, 'Horarios', 'Lunes a Viernes de 8 a 20hs.'),
  (
    3,
    '¿Cómo devolver?',
    'Entregar en mostrador de biblioteca.'
  ),
  (
    4,
    '¿Qué pasa si se rompe?',
    'Reportar inmediatamente al bibliotecario.'
  ),
  (
    5,
    'Sanciones',
    'Las penalizaciones impiden nuevas reservas.'
  ),
  (
    6,
    '¿Cuánto dura el préstamo?',
    'El periodo estándar es de un máximo de 7 días corridos.'
  ),
  (
    7,
    '¿Puedo renovar?',
    'Sí, siempre que no haya otra reserva pendiente sobre el artículo.'
  ),
  (
    8,
    '¿Qué hago si el laboratorio está cerrado?',
    'Diríjase a la ventanilla central de biblioteca para la entrega.'
  ),
  (
    9,
    '¿Quiénes pueden usar el sistema?',
    'Alumnos regulares, docentes e investigadores autorizados.'
  ),
  (
    10,
    '¿Se pueden retirar consumibles?',
    'No, insumos como estaño o cables pelados se solicitan directo al pañol.'
  ),
  (
    11,
    '¿Cómo cancelo una reserva?',
    'Desde su panel de usuario, sección Historial -> Cancelar antes del retiro.'
  ),
  (
    12,
    'Olvidé mi contraseña',
    'Utilice el enlace de recuperación o consulte al administrador IT.'
  ),
  (
    13,
    '¿Hay límite de artículos por reserva?',
    'Sí, un máximo de 3 artículos en simultáneo por usuario.'
  ),
  (
    14,
    '¿Los profesores tienen plazos distintos?',
    'Los docentes pueden solicitar extensiones por proyectos semestrales.'
  ),
  (
    15,
    '¿Qué significa estado Pendiente?',
    'Su solicitud está a la espera de la validación del bibliotecario.'
  ),
  (
    16,
    '¿Qué significa estado Aprobado?',
    'Su reserva fue aceptada, ya puede concurrir en el horario pautado a retirar.'
  ),
  (
    17,
    '¿Qué significa estado Entregado?',
    'Usted posee físicamente el equipo en este momento.'
  ),
  (
    18,
    'Daños preexistentes',
    'Revise el equipo al recibirlo. Si nota fallas, repórtelo en ese instante.'
  ),
  (
    19,
    '¿Puedo enviar a un compañero a retirar?',
    'No, los retiros son estrictamente personales con credencial o DNI.'
  ),
  (
    20,
    'Notificaciones',
    'El sistema envía correos automáticos ante la proximidad del vencimiento.'
  ),
  (
    21,
    'Pérdida de componentes',
    'Si pierde un accesorio, se penalizará hasta la reposición del mismo.'
  ),
  (
    22,
    'Uso fuera de la facultad',
    'Requiere una nota de autorización firmada por el Director de Carrera.'
  ),
  (
    23,
    'Sanciones por mora',
    'Se calculan de forma automática según los días de retraso registrados.'
  ),
  (
    24,
    '¿El sistema funciona feriados?',
    'Se pueden cargar reservas, pero no habrá entregas ni recepciones físicas.'
  ),
  (
    25,
    'Contacto de Soporte',
    'Ante errores de sistema, envíe mail a soporte.prestamos@universidad.edu.'
  );

-- =========================================================================
-- 7. NORMATIVA (25 filas)
-- =========================================================================
INSERT INTO
  normativa (id, titulo, descripcion)
VALUES
  (
    1,
    'Reglamento 001',
    'Uso exclusivo de equipos para fines académicos.'
  ),
  (
    2,
    'Seguridad Lab',
    'Prohibido comer o beber en áreas de trabajo.'
  ),
  (
    3,
    'Responsabilidad',
    'El usuario es responsable por pérdida o daño.'
  ),
  (4, 'Plazos', 'Máximo de 7 días por préstamo.'),
  (
    5,
    'Acceso',
    'Solo alumnos regulares pueden reservar.'
  ),
  (
    6,
    'Código de Conducta',
    'Trato respetuoso hacia el personal técnico y bibliotecario.'
  ),
  (
    7,
    'Epps Obligatorios',
    'Uso de gafas de seguridad y calzado cerrado en el taller mecánico.'
  ),
  (
    8,
    'Protocolo Eléctrico',
    'No energizar circuitos sin la supervisión previa del docente.'
  ),
  (
    9,
    'Devolución Limpia',
    'Los instrumentos deben devolverse libres de polvo, grasa o anotaciones.'
  ),
  (
    10,
    'Prioridad Docente',
    'Las clases prácticas tienen prioridad de stock sobre proyectos personales.'
  ),
  (
    11,
    'Sanción por Reincidencia',
    'Tres faltas leves automáticas equivalen a una suspensión de un mes.'
  ),
  (
    12,
    'Uso de Software',
    'Prohibida la instalación de software sin licencia en notebooks prestadas.'
  ),
  (
    13,
    'Reporte de Averías',
    'Obligación de declarar cualquier comportamiento anómalo del hardware.'
  ),
  (
    14,
    'Fines Comerciales',
    'Queda terminantemente prohibido usar los equipos para lucro privado.'
  ),
  (
    15,
    'Verificación de Identidad',
    'El personal exigirá acreditación física antes de cada entrega.'
  ),
  (
    16,
    'Puntualidad Retiro',
    'Reservas aprobadas expiran si no se retiran dentro de las 24 horas.'
  ),
  (
    17,
    'Cuidado Multimedia',
    'Los proyectores deben dejarse enfriar antes de ser guardados en el estuche.'
  ),
  (
    18,
    'Norma de Calibración',
    'No alterar los precintos de calibración de los osciloscopios.'
  ),
  (
    19,
    'Almacenamiento de Datos',
    'El sistema borra los perfiles locales de las PCs al ser devueltas.'
  ),
  (
    20,
    'Fuerza Mayor',
    'En contingencias edilicias, los plazos de devolución quedan congelados.'
  ),
  (
    21,
    'Uso de Baterías',
    'Cargar los dispositivos únicamente con los transformadores provistos.'
  ),
  (
    22,
    'Reserva de Espacios',
    'La reserva del equipo no garantiza el espacio físico en el laboratorio.'
  ),
  (
    23,
    'Auditorías de Stock',
    'El pañol permanecerá cerrado los últimos dos días del ciclo lectivo.'
  ),
  (
    24,
    'Firmas Digitales',
    'Las aprobaciones vía sistema tienen validez de declaración jurada.'
  ),
  (
    25,
    'Modificaciones de la Norma',
    'La Secretaría Académica se reserva el derecho de alterar los plazos.'
  );
