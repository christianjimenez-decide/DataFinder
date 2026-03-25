# BeeBot Data Analyst

Una aplicación web de Streamlit que sirve como un asistente dinámico de Análisis de Datos multi-agente. Con BeeBot, puedes cargar cualquier archivo de datos CSV y recibir instantáneamente tanto procesamiento estadístico técnico como información estratégica de negocios de alto nivel potenciada por la IA Gemini.

## Características

- **Ingestión Dinámica de Datos**: Arrastra y suelta cualquier archivo `.csv`. La aplicación detecta automáticamente los tipos de columnas, analiza las fechas y genera un contexto estadístico relevante.
- **Arquitectura Multi-Agente**: 
  - *Ingeniero de Datos*: Procesa los datos proporcionando cálculos numéricos precisos, resúmenes estadísticos e interpretaciones técnicas.
  - *Consultor de Negocios*: Consume contextos técnicos para sintetizar estrategias y recomendaciones de negocio accionables.
- **Vistas Previas Inteligentes**: Representación automática de muestras del conjunto de datos, métricas de alto nivel y resúmenes de distribución directamente en el panel de control.
- **Interfaz Moderna**: Una interfaz limpia con estilos personalizados y estéticas oscuras/claras que imitan un espacio de trabajo generativo premium.

## Requisitos Previos

- Python 3.9 o superior
- Una clave de API de Google Gemini válida. Puedes generar una en [Google AI Studio](https://aistudio.google.com/apikey).

## Primeros Pasos

1. **Clona el repositorio o descarga el código fuente** (si aún no lo has hecho).

2. **Instala las dependencias**

    > [!TIP]
    > Se recomienda usar un entorno virtual de Python al configurar el proyecto localmente.

    Asegúrate de haber instalado las librerías necesarias desde tu terminal:

    ```bash
    pip install streamlit pandas google-genai
    ```

3. **Ejecuta la aplicación**

    ```bash
    streamlit run app.py
    ```

    La aplicación se vinculará a un puerto local y se abrirá automáticamente en tu navegador predeterminado (normalmente en `http://localhost:8501`).

## Uso

1. Abre el menú de configuración ubicado en la barra lateral izquierda y proporciona tu Clave de API de Gemini.
2. Selecciona tu modelo generativo preferido (por ejemplo, `Gemini 2.5 Flash` o `Gemini 2.5 Pro`).
3. Carga un archivo CSV estructural a través de la zona de carga, o activa la demo integrada (`ventas_q1.csv`) si solo quieres probar el flujo de trabajo.
4. Interactúa usando la entrada de chat principal haciendo preguntas relacionadas con el conjunto de datos (por ejemplo, "¿Cuáles son las tendencias clave entre los productos?").

> [!NOTE] 
> La aplicación utiliza límites de contexto centrados en `pandas`. Los conocimientos y el razonamiento generados por los agentes dependen estrictamente del contenido de los datos enviados.

## Estructura del Proyecto

- `app.py`: El script de ejecución principal que define los componentes de la interfaz de Streamlit, estilos, módulos de preparación de datos y conexiones de API.
- `data/`: Almacenamiento de datos de demostración (contiene `ventas_q1.csv`).
- `config/` / `skills/`: Instrucciones y capacidades extensibles que habilitan comportamientos inteligentes bajo varios escenarios.

## Agradecimientos

- Construido utilizando [Streamlit](https://streamlit.io/).
- Inteligencia de lenguaje impulsada por el [Google GenAI Python SDK](https://github.com/googleapis/google-genai-sdk).
