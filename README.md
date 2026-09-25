# 🚲 Bicycle Workshop Control System — Taller de Bicicletas

> **UNAD · Ingeniería de Sistemas · Programación (213023) — Fase 2, Ejercicio 1**
> Aplicación de escritorio en Python que gestiona el ingreso, la salida y el cobro
> de bicicletas en un taller, con inicio de sesión, arquitectura limpia y 35 pruebas unitarias.

---

## 📖 Tabla de contenido

1. [Qué hace el proyecto](#-qué-hace-el-proyecto)
2. [Demostración rápida](#-demostración-rápida)
3. [Requisitos](#-requisitos)
4. [Instalación](#-instalación)
5. [Cómo usar la aplicación](#-cómo-usar-la-aplicación)
6. [Arquitectura del proyecto](#-arquitectura-del-proyecto)
7. [Estructura de archivos](#-estructura-de-archivos)
8. [Clases principales](#-clases-principales)
9. [Pruebas](#-pruebas)
10. [Explicado para aprender](#-explicado-para-aprender)
11. [Lista de chequeo del Anexo](#-lista-de-chequeo-del-anexo)
12. [Problemas conocidos](#-problemas-conocidos)
13. [Autor](#-autor)

---

## 🎯 Qué hace el proyecto

El taller necesita dejar el papel y controlar en computador:

- **Iniciar sesión** con usuario y contraseña antes de ver el sistema.
- **Registrar bicicletas** con serial, costo por hora y hora de ingreso.
- **Guardarlas** en una lista interna visible en pantalla.
- **Seleccionar una bicicleta** y registrar su hora de salida.
- **Calcular automáticamente** el costo: `horas transcurridas × costo por hora`.
- **Validar** que la hora de salida sea posterior a la de ingreso.

Toda la interfaz gráfica está en **inglés** (requisito del Anexo), mientras que las
clases del dominio conservan los **nombres exactos en español** que pide la guía.

---

## ⚡ Demostración rápida

```bash
# 1. Clonar el repositorio
git clone <URL-DEL-REPO>
cd <CARPETA-DEL-REPO>

# 2. Instalar la única dependencia externa
pip install customtkinter

# 3. Ejecutar la aplicación
python exercise1_bicycle_workshop.py

# 4. Iniciar sesión con:
#    Usuario:    programacion
#    Contraseña: programacion
```

---

## 🧰 Requisitos

| Requisito      | Versión probada |
|----------------|-----------------|
| Python         | 3.13.9          |
| customtkinter  | 5.2.2           |
| tkinter        | incluida con Python estándar en Windows |
| unittest       | incluida en la biblioteca estándar (sin instalación extra) |

> No se usa `pytest` ni ninguna otra dependencia: el proyecto funciona solo con
> la biblioteca estándar más `customtkinter` para la interfaz moderna.

---

## 💾 Instalación

```bash
# Opción A: instalación mínima
pip install customtkinter

# Opción B: verificar versiones
python --version
pip show customtkinter
```

---

## 🖥️ Cómo usar la aplicación

1. **Login.** La ventana inicial pide usuario y contraseña.
   Credenciales válidas: `programacion` / `programacion`.
   Si fallan, aparece un mensaje de error y la ventana vibra; la contraseña se borra.
2. **Register Bicycle.** Escribe serial, costo por hora (número positivo) y hora de
   ingreso en formato `HH:MM` de 24 horas. Pulsa **Register Entry**.
3. **Bicycles in Workshop.** Cada bicicleta aparece como una fila seleccionable.
   Haz clic en una para seleccionarla (se resalta en verde).
4. **Register Exit.** Escribe la hora de salida `HH:MM` y pulsa **Calculate Total**.
   El programa muestra el total, una ventana de resumen y retira la bicicleta
   de la lista (el servicio ya terminó).

---

## 🏛️ Arquitectura del proyecto

Se usa **Clean Architecture** en tres capas. La regla de oro: **las capas internas
no conocen a las externas**. El dominio y la aplicación son Python puro, sin
`tkinter`; solo la infraestructura dibuja ventanas.

```text
┌──────────────────────────────────────────────┐
│  INFRASTRUCTURE (bicycle_workshop/           │
│  infrastructure/)  — CustomTkinter, ventanas │
│  LoginWindow, BicycleWorkshopApp, app.main() │
│  como composition root (único CTk)           │
├──────────────────────────────────────────────┤
│  APPLICATION (bicycle_workshop/application/) │
│  LoginService, WorkshopService — casos de    │
│  uso y estado (lista interna, selección)     │
├──────────────────────────────────────────────┤
│  DOMAIN (bicycle_workshop/domain/)           │
│  Usuario, BicicletaTaller — lógica pura del  │
│  negocio, copiada del Anexo sin cambios      │
└──────────────────────────────────────────────┘
         Las dependencias apuntan hacia adentro ↓
```

**Flujo de datos típico:** la ventana llama al servicio, el servicio usa la
entidad, la entidad valida y calcula, el resultado vuelve a la ventana.

---

## 🗂️ Estructura de archivos

```text
.
├── exercise1_bicycle_workshop.py      # Entry point fino (solo llama a main)
├── bicycle_workshop/
│   ├── __init__.py                    # Exporta main de forma LAZY (los tests no cargan GUI)
│   ├── domain/
│   │   └── entities.py                # Usuario, BicicletaTaller (lógica pura)
│   ├── application/
│   │   └── services.py                # LoginService, WorkshopService (casos de uso)
│   └── infrastructure/
│       ├── app.py                     # main(): crea el único CTk y abre el login
│       └── ui/
│           ├── login_window.py        # Ventana de inicio de sesión
│           └── main_window.py         # Ventana principal del taller
└── tests/
    ├── test_entities.py               # 17 pruebas del dominio
    └── test_services.py               # 18 pruebas de la aplicación
```

---

## 🧩 Clases principales

### `Usuario` — control de acceso

```python
from bicycle_workshop.domain.entities import Usuario

usuario = Usuario()  # credenciales por defecto: programacion / programacion
usuario.validar("programacion", "programacion")  # True
usuario.validar("programacion", "otra")          # False
```

- Atributos privados: `_usuario`, `_password`.
- Método público: `validar(usuario_ingresado, password_ingresada)`.
- Retorna `True` solo cuando ambas credenciales coinciden.

### `BicicletaTaller` — el corazón del taller

```python
from bicycle_workshop.domain.entities import BicicletaTaller

bici = BicicletaTaller("ABC123", 5000)
bici.registrar_ingreso("09:30")
bici.registrar_salida("11:00")      # valida que sea mayor al ingreso
total = bici.calcular_total("11:00")  # (90 min / 60) * 5000 = 7500.0
bici.obtener_serial()                 # "ABC123"
```

- Atributos privados: `_serial`, `_hora_ingreso`, `_costo_por_hora`.
- Métodos: `registrar_ingreso(hora)`, `registrar_salida(hora)`,
  `calcular_total(hora_salida)`, `obtener_serial()`.
- Las horas usan formato `HH:MM` de 24 horas y se convierten a minutos internamente.
- Si la salida es menor o igual al ingreso, lanza `ValueError`.

### Servicios de aplicación

- **`LoginService.validate(usuario, password)`**: limpia espacios, rechaza vacíos
  y delega en `Usuario.validar`.
- **`WorkshopService`**: guarda la lista interna `bicycles`, registra con
  `register_bicycle(serial, costo, ingreso)`, selecciona con `select_bicycle(i)`,
  cobra con `calculate_total(salida)` y retira con `remove_current()`.

---

## ✅ Pruebas

35 pruebas con `unittest` de la biblioteca estándar. No requieren interfaz gráfica.

```bash
# Ejecutar todas las pruebas con detalle
python -m unittest discover -s tests -v

# Resultado esperado
# Ran 35 tests in 0.00Xs
# OK
```

| Archivo               | Cantidad | Qué cubre |
|-----------------------|----------|-----------|
| `test_entities.py`    | 17       | `Usuario.validar`, conversión de horas, ingreso/salida, cálculo de totales, serial |
| `test_services.py`    | 18       | Login con espacios/vacíos, registro válido e inválido, selección, cobro, retiro |

---

## 🎓 Explicado para aprender

> Si estás estudiando y quieres **explicar** este proyecto en una sustentación,
> esta sección es tu guion.

### 1. Encapsulación (lo privado con `_`)

Las clases guardan sus datos con guion bajo (`_usuario`, `_hora_ingreso`) para que
nadie los cambie directamente desde fuera. La única forma de usarlos es a través de
métodos públicos (`validar`, `registrar_ingreso`). Eso se llama **encapsulación**:
proteges los datos y obligas a pasar por tus reglas (por ejemplo, validar la hora).

### 2. Separación en capas (por qué hay 3 carpetas)

- **Dominio:** las reglas del negocio que existirían aunque no hubiera pantallas
  (¿cuánto cuesta? ¿la hora es válida?).
- **Aplicación:** el flujo de trabajo (lista de bicis, cuál está seleccionada).
- **Infraestructura:** lo que el usuario ve y toca (botones, ventanas).

Si mañana cambias `customtkinter` por otra librería, solo tocas infraestructura.
El dominio y sus 35 pruebas siguen intactos. Esa es la ganancia de Clean Architecture.

### 3. Cómo explicar el cálculo en 30 segundos

> "Convierto las horas `HH:MM` a minutos totales, resto salida menos ingreso para
> obtener los minutos transcurridos, los divido entre 60 para pasar a horas y
> multiplico por el costo por hora. Antes de calcular, valido que la salida sea
> mayor que el ingreso; si no, lanzo un error que la ventana muestra al usuario."

### 4. Por qué el import es "lazy"

`bicycle_workshop/__init__.py` no importa la GUI al inicio. Así los tests pueden
importar el dominio sin abrir ventanas ni necesitar pantalla. La GUI solo se carga
cuando ejecutas el programa real. Es un truco estándar llamado **lazy import**.

---

## 📋 Lista de chequeo del Anexo

- [x] Módulo de login que se muestra primero y bloquea el sistema principal.
- [x] Clase `Usuario` con `_usuario`, `_password` y `validar(...)`.
- [x] Clase `BicicletaTaller` con `_serial`, `_hora_ingreso`, `_costo_por_hora`.
- [x] Métodos `registrar_ingreso`, `registrar_salida`, `calcular_total`, `obtener_serial`.
- [x] Lista interna de bicicletas con selección y registro de salida.
- [x] Cálculo automático del costo y validación de horas.
- [x] Interfaces gráficas en inglés, lógica con nombres exactos del Anexo.
- [x] Programación Orientada a Objetos con encapsulación.

---

## ⚠️ Problemas conocidos

1. **No crear un segundo `CTk()`.** En Windows, destruir la ventana de login y crear
   otra ventana principal cuelga la app. Por eso el login reutiliza la misma raíz
   (`on_success` limpia los widgets y construye el sistema principal encima).
2. **Sin `placeholder_text` nativo.** El placeholder de CustomTkinter tragaba
   pulsaciones de teclas en Windows. Los campos inician vacíos con etiquetas fijas.
3. **Sin re-bind de `<KeyRelease>`.** Re-suscribir el evento en cada tecla congelaba
   la escritura; el handler solo limpia el mensaje de error.

---

## 👤 Autor

Proyecto académico — UNAD, Ingeniería de Sistemas, curso Programación (213023).
Desarrollado en Python con Clean Architecture y pruebas `unittest`.
