# Workspace Guidelines & Rules

## Language & Persona Override

- **Español Neutro**: Siempre responder en **español neutro**. Está estrictamente prohibido usar el dialecto rioplatense (voseo, vos, tenés, podés, etc.).
- Usar un tono profesional, claro, directo y conciso.

## Estándar Profesional para README y Documentación (MANDATORIO)

Al crear, actualizar o finalizar la documentación (`README.md`) para cualquier proyecto o repositorio de GitHub, SIEMPRE se debe aplicar el siguiente estándar open-source de nivel enterprise:

### 1. Cabecera e Insignias (Shields.io)
- Encabezado centrado con logo/título, subtítulo conciso de alto impacto e insignias dinámicas de Shields.io (Licencia, Versión de Lenguaje/Runtime, Framework, Estado de Pruebas, Nivel de Diseño y Destino de Despliegue).
- Enlaces de navegación rápida a secciones clave (`Visión General`, `Características`, `Arquitectura`, `Uso Local`, `Despliegue`).

### 2. Características y Sistema de Diseño
- Detalle de capacidades del producto con formato claro.
- Resumen del sistema de diseño (paleta de colores, diseño de interfaz, micro-interacciones, diseño responsivo).

### 3. Arquitectura y Referencia de la API
- Diagrama en formato ASCII o Mermaid con el flujo de componentes (Cliente, Servidor, Motor, APIs externas).
- Tabla ordenada en markdown para los endpoints de la API (`Método`, `Endpoint`, `Descripción`).

### 4. Instalación y Pruebas Locales
- Comandos ejecutables paso a paso (`git clone`, entorno virtual, instalación de dependencias y arranque del servidor).
- Comando para ejecutar la suite de pruebas automatizadas (`pytest`, `npm test`, etc.).

### 5. Despliegue en Producción
- Guía detallada paso a paso para despliegue en la nube (Render, Docker, Vercel, Railway).
- Archivos de infraestructura como código (`render.yaml`, `Dockerfile`, `Procfile`) creados nativamente en el proyecto.
