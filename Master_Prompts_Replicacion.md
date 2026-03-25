# Guía Maestra de Replicación: DataFinder via "Agent Manager"

A la hora de crear aplicaciones complejas con IA (como este dashboard multi-agente de Streamlit), la mejor práctica no es dar un único mandato gigante a la IA, sino utilizar un enfoque de **Agent Manager**. 

En este modelo, tú actúas como el "Manager" o "Product Owner", y **delegas tareas muy específicas a diferentes Agentes virtuales**. Cada agente recibe un rol y un contexto limitado a su especialidad, haciendo que el código final sea mucho más limpio, mantenible y libre de alucinaciones.

A continuación, se detallan los **prompts exactos** divididos por "Bloques de Agentes" para que puedas replicar la aplicación.

---

## 🛠️ Bloque 1: Agente Especialista en Datos (Data Engineer)
*Tu objetivo como Manager es pedirle a un especialista en Python/Pandas que te prepare el terreno de los datos de entrada, sin que se preocupe por la interfaz visual ni la API de GenAI.*

> **Prompt (Copia y pega a tu asistente):**
> "Actúa como un Data Engineer especialista en Python y Pandas. Crea un archivo de skill (por ejemplo `SKILL_pandas.md`) que documente paso a paso: 
> 1. Cómo cargar un archivo CSV.
> 2. Cómo solucionar problemas comunes de codificación (intentar utf-8 y luego fallback a latin-1).
> 3. Cómo parsear columnas de fechas inteligentemente.
> 4. Cómo construir una función que devuelva un bloque de 'contexto de texto' puro que incluya: número de filas y columnas, tipos de datos, conteo de valores nulos, estadísticas numéricas (con `describe()`) y una previsualización de las primeras 50 filas.
> El objetivo final es que puedas pasar este texto como contexto a un LLM."

---

## 🎭 Bloque 2: Agente de Prompt Engineering
*Aquí delegamos la tarea de diseñar la personalidad de los agentes "internos" que vivirán dentro de la aplicación final.*

> **Prompt (Copia y pega a tu asistente):**
> "Actúa como un experto en Prompt Engineering y diseño de comportamiento LLM. Crea un archivo llamado `config/PROMPTS.md` definiendo dos System Prompts estrictos:
> 
> 1. **Agente Ingeniero (Data Engineer)**: Su misión es leer datos estadísticos (como los provistos por pandas.describe()) y devolver estrictamente hallazgos matemáticos/técnicos, formatos numéricos y métricas en formato Markdown. Prohíbele terminantemente dar opiniones, juicios de negocio o recomendaciones.
> 2. **Agente Consultor (Business Consultant)**: Un directivo Senior. Su misión es ingerir los cálculos técnicos del Ingeniero y generar InsightsEstratégicos. Debe evaluar rentabilidad, impacto comercial y dictar Recomendaciones claramente estructuradas.
> 
> Redacta las instrucciones delineando las fronteras entre ambos."

---

## 🧠 Bloque 3: Agente Backend IA (Integración Gemini API)
*Con los datos y los prompts listos, llamamos a un desarrollador backend para que nos conecte con el motor LLM y maneje sus peculiaridades técnicas (límites de tasa, seguridad).*

> **Prompt (Copia y pega a tu asistente):**
> "Actúa como un Backend Engineer especialista en IA. Escribe la lógica en Python utilizando el SDK más reciente de Google Generative AI (`google.genai`). 
> Necesito una única función modular llamada `call_gemini(api_key, system_prompt, context, user_query, model_name)`. Esta función debe armar el prompt dinámicamente y pasar el `system_prompt` como `system_instruction`. 
> Requisito crítico: Implementa un mecanismo de reintento escalar (`retry` con 3 intentos y un bloque `time.sleep`) para manejar las excepciones de HTTP 429 (Rate Limit). Devuelve un bloque genérico de error únicamente si todos los intentos fallan."

---

## 🎨 Bloque 4: Agente Frontend y UX/UI
*Ahora llamamos al maquetador visual. A este agente no le importan los datos reales, solo le importa que la aplicación se vea increíble y premium.*

> **Prompt (Copia y pega a tu asistente):**
> "Actúa como un Frontend Developer y experto en UX especializado en Streamlit. Crea el esqueleto visual de una aplicación `app.py`.
> Requerimientos:
> 1. **Estética Premium (Modo Claro)**: Inyecta CSS personalizado. Usa la fuente Google 'Inter'. Oculta por defecto el header de Streamlit. Crea tarjetas de chat con bordes redondeados y sombras sutiles.
> 2. **Sidebar**: Añade contenedores para logo, input de API Key oculto (password), y un widget `st.file_uploader`. Incluye un botón Toggle por si el usuario prefiere usar un CSV local de 'demo'.
> 3. **Hero Section y Chat**: En el flujo principal, monta un Hero section motivacional estilo 'glassmorphism' si no hay datos subidos. Si los hay, usa los controles `st.chat_message` y `st.chat_input` para montar una interfaz de chat impecable, y muestra métricas base estilo KPIs arriba de la pantalla."

---

## 🎼 Bloque 5: Agente Orquestador (Ensamblaje final)
*Tú vuelves a tu Rol de Manager y le pides a un desarrollador Integrador Full-Stack que junte el código de los 4 agentes anteriores en el circuito final.*

> **Prompt (Copia y pega a tu asistente):**
> "Actúa como un Integrador Full-Stack. Toma la base visual construida en Streamlit, integra las funciones de Pandas creadas, inyecta los System Prompts para los agentes internos, e incorpora la función `call_gemini`.
> El flujo final a programar es:
> 1. Cuando el usuario escriba en el chat, valida que exista el CSV y la API key.
> 2. Llama a tu función constructora del contexto Pandas.
> 3. Abre un bloque visual (`st.chat_message`), pinta una tarjeta de CSS llamada 'Data Engineer Output' y ejecuta `call_gemini` usando el spinner 'Procesando datos...'. Pinta el texto resultante.
> 4. Inmediatamente debajo en la misma iteración del chat, abre una nueva tarjeta CSS 'Business Consultant Analysis', lanza otro spinner, y ejecuta un segundo `call_gemini` usando el otro system prompt.
> Guarda todo el histórico en `st.session_state` y realiza un rerun."
