# umbrales-compras-publicas
# 📊 Analítica de datos como insumo para el ejercicio de la potestad de definición de umbrales de la Contraloría General basado en componentes adicionales a las estimaciones procedimentales

---

## 📋 I. Resumen Ejecutivo

El propósito principal de este análisis es examinar el **impacto** que ha tenido la emisión de la **Ley General de Contratación Pública, Ley No.9986**, y su posible impacto para tomar medidas por parte de la **Contraloría General de la República (CGR)** sobre los umbrales definidos en el numeral 36 de esa Ley y conforme la potestad que se le otorga al órgano contralor en el párrafo final del mismo, conforme al comportamiento de las compras públicas. 

El objetivo es ofrecer una **comprensión exhaustiva** de cómo estos umbrales, influenciados por elementos que exceden las valoraciones económicas iniciales, configuran el marco de la contratación pública y sus implicaciones prácticas en la gestión de los recursos estatales.

### 🎯 Alcance del Análisis

Por otra parte, este análisis se circunscribe al examen de los **umbrales establecidos por la CGR** en el contexto de su esquema recursivo aplicable a las compras públicas, para esto se analizarán:

- 📜 Las disposiciones normativas
- 📋 Directrices pertinentes  
- ⚖️ La jurisprudencia que fundamenta la fijación de estos límites

Todo esto dentro de las potestades de la institución en la búsqueda de un control recursivo conforme a ese comportamiento de las compras públicas.

### 🔬 Metodología

El **pilar de este estudio** es el uso de analítica de datos detallado de variables adicionales a las estimaciones procedimentales que la CGR debe considerar al momento de definir de forma ordinaria dichos umbrales, que básicamente es un ejercicio inercial de traída a valor presente de un monto inicial establecido por el legislador.

#### 📊 Variables de Análisis

Conforme a lo anterior se tomará como base **dos variables principales**:

1. **📈 Índice Herfindahl-Hirschman (IHH o HHI)** 
   - Referido a la concentración de segmentos de bienes y servicios en compras públicas

2. **📉 Coeficiente de variación de precios**
   - En los códigos de bienes y servicios en aquellos segmentos con menor concentración de adjudicatarios

### 🎯 Hipótesis Central

> La base de la presente propuesta parte de determinar aquellos **segmentos de compras públicas** con un menor grado de concentración de adjudicatarios, es decir los segmentos que presentan un **IHH menor** y dentro de esos segmentos aquellos códigos de bienes y servicios que han presentado una **menor variabilidad del precio adjudicado** (CV menor).

**Supuesto fundamental:** Entre mayor variabilidad de adjudicatarios y menos volatilidad de precios corresponden a bienes y servicios que presentan un **menor riesgo** de presentar comportamientos anómalos durante el proceso de contratación hasta la adjudicación.

### ⏱️ Período de Estudio

Como **hito determinante** del estudio se revisaron los períodos:
- 📅 **Previos** a la emisión de la nueva Ley de contratación
- 📅 **Posteriores** a la emisión de la nueva Ley de contratación

Analizando posibles cambios en la variable de concentración de adjudicatarios.

---

## 🚀 Ejecutar el Análisis

Código de análisis de IHH por segmento de SICOP:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cgrcostarica/umbrales-compras-publicas/blob/main/umbrales_hhi_rfc.ipynb)



Código de análisis de coeficiente de variación de precios CV por código de producto 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cgrcostarica/umbrales-compras-publicas/blob/main/coeficiente_variacion_precio%20(1).ipynb)
---

*Desarrollado por la Contraloría General de la República de Costa Rica*



