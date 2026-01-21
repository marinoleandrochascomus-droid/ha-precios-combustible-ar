# Precio Combustible Argentina 🇦🇷 para Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/tu_usuario/precio_combustible_ar)

[Español](#español) | [English](#english)

---

<a name="español"></a>
## 🇪🇸 Español

Esta integración permite monitorear en tiempo real los precios de los combustibles en las estaciones de servicio de la República Argentina, utilizando los datos oficiales de la Secretaría de Energía (Resolución 314/2016).

### ✨ Características
* 📍 **Filtrado Inteligente**: Selección por Provincia (CABA, Buenos Aires, etc.) y Localidad.
* ⛽ **Soporte Multicombustible**: Nafta Súper, Premium, Gasoil Grado 2/3 y GNC.
* 🖼️ **Logos Oficiales**: Identificación visual inmediata (YPF, Shell, Axion, Puma).
* 🕒 **Estado del Dato**: Indica si el precio está "Al día" o "Desactualizado" (+30 días).
* 🚀 **Alto Rendimiento**: Arquitectura asíncrona que no bloquea tu instancia de Home Assistant.
* 📊 **Atributos Detallados**: Dirección exacta, localidad y fecha de última modificación oficial.

### 🚀 Instalación

#### Opción 1: HACS (Recomendado)
1. Ve a **HACS** > **Integraciones**.
2. Clic en los tres puntos (arriba a la derecha) > **Repositorios personalizados**.
3. Pega la URL de este repositorio y selecciona la categoría **Integración**.
4. Busca "Precio Combustible Argentina" e instala.
5. **Reinicia Home Assistant**.

#### Opción 2: Manual
1. Descarga el repositorio y copia la carpeta `custom_components/precio_combustible_ar` dentro del directorio `custom_components/` de tu servidor.
2. **Reinicia Home Assistant**.

### ⚙️ Configuración
1. Ve a **Ajustes** > **Dispositivos y Servicios**.
2. Haz clic en **Añadir Integración** y busca `Precio Combustible Argentina`.
3. Selecciona tu **Provincia** (ej: CABA).
4. Selecciona tu **Localidad** y el **Tipo de Combustible**.
5. ¡Listo! Se creará un sensor por cada estación encontrada.

---

## Capturas de Pantalla
<p align="center">
  <img src="screenshots/Captura de pantalla 2026-01-21 114730.png" width="400" title="Detalle">
  <img src="screenshots/Captura de pantalla 2026-01-21 114743.png" width="400" title="Detalle">
  <img src="screenshots/Captura de pantalla 2026-01-21 114805.png" width="400" title="Detalle">
  <img src="screenshots/Captura de pantalla 2026-01-21 114837.png" width="400" title="Detalle">
</p>

---

<a name="english"></a>
## 🇺🇸 English

Monitor real-time fuel prices across Argentina using official data from the Secretary of Energy.

### ✨ Features
* 📍 **Smart Filtering**: Select by Province (including CABA) and Locality.
* ⛽ **Multi-fuel Support**: Regular, Premium, Diesel, and CNG.
* 🖼️ **Brand Logos**: Visual identification for major brands (YPF, Shell, Axion, Puma).
* 🕒 **Data Freshness**: Visual indicators for "Up to date" or "Outdated" prices.
* 🚀 **Performance**: Fully asynchronous architecture to keep your system fast.

### 🚀 Installation
1. **HACS**: Add this repository as a "Custom Repository".
2. **Manual**: Copy the `precio_combustible_ar` folder to your `custom_components` directory.
3. **Restart** Home Assistant and add the integration via the UI.

---

### ⚠️ Notas y Calidad de Datos / Disclaimer
* **Origen**: Los datos provienen del portal de Datos Abiertos de la Nación. 
* **Actualización**: La frecuencia de actualización de precios depende exclusivamente de lo informado por cada estación de servicio bajo la normativa vigente.
* **IA**: Proyecto desarrollado con asistencia de IA (Gemini) para la optimización de procesos de filtrado y estabilidad del sistema.

---
**Desarrollado en Argentina 🇦🇷**
