# SKILL: Análisis de CSV con Pandas

---

## Descripción

Esta skill documenta cómo usar la librería **Pandas** de Python para cargar, inspeccionar y extraer metadata de un archivo CSV. Se usa como base para alimentar a los agentes con contexto real de los datos.

---

## 1. Cargar el CSV

```python
import pandas as pd

df = pd.read_csv("data/ventas_q1.csv")
```

---

## 2. Inspección rápida

| Método              | Propósito                                      |
| ------------------- | ---------------------------------------------- |
| `df.head()`         | Ver las primeras 5 filas                       |
| `df.shape`          | Obtener (filas, columnas)                      |
| `df.dtypes`         | Tipos de dato de cada columna                  |
| `df.info()`         | Resumen completo: tipos, no-nulos, memoria     |
| `df.describe()`     | Estadísticas descriptivas de columnas numéricas |
| `df.columns.tolist()`| Lista de nombres de columnas                   |

---

## 3. Extraer metadata para el contexto de los agentes

```python
# Estadísticas descriptivas (se envían como contexto al LLM)
stats = df.describe().to_string()

# Columnas y tipos
columns_info = df.dtypes.to_string()

# Primeras filas como muestra
sample = df.head().to_string()

# Valores únicos por categoría
categorias = df["Categoria"].unique().tolist()
productos = df["Producto"].unique().tolist()
```

---

## 4. Métricas clave calculadas

```python
# Margen de beneficio por fila
df["Margen_EUR"] = df["Ventas_EUR"] - df["Coste_EUR"]
df["Margen_Pct"] = (df["Margen_EUR"] / df["Ventas_EUR"] * 100).round(2)

# Totales
total_ventas = df["Ventas_EUR"].sum()
total_coste = df["Coste_EUR"].sum()
margen_global = ((total_ventas - total_coste) / total_ventas * 100).round(2)

# Agrupado por categoría
por_categoria = df.groupby("Categoria").agg(
    Ventas_Total=("Ventas_EUR", "sum"),
    Coste_Total=("Coste_EUR", "sum"),
    Num_Transacciones=("Producto", "count")
).reset_index()
```

---

## 5. Construir contexto textual para el LLM

```python
contexto = f"""
=== DATASET: ventas_q1.csv ===
Filas: {df.shape[0]} | Columnas: {df.shape[1]}

--- Columnas ---
{columns_info}

--- Estadísticas Descriptivas ---
{stats}

--- Muestra de datos (primeras 5 filas) ---
{sample}

--- Categorías únicas ---
{categorias}

--- Productos únicos ---
{productos}
"""
```

Este contexto se pasa como parte del prompt a cada agente LLM para que analicen datos reales.
