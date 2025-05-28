# agent_with_pandas.py
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_ollama.llms import OllamaLLM
import os

from data_processing import load_all_dataframes, get_column_names_for_prefix, PRODUCTS_FILE, ORDERS_FILE, CUSTOMERS_FILE

LLM_MODEL_NAME = "llama3.2"
llm = OllamaLLM(model=LLM_MODEL_NAME, temperature=0)

def main():
    print(f"--- Iniciando Agente IA con Capacidades de Análisis Pandas (v4.5 - LLM: {LLM_MODEL_NAME}) ---")

    all_data = load_all_dataframes()
    if not all_data or \
       'productos' not in all_data or \
       'ordenes' not in all_data or \
       'clientes' not in all_data:
        print("ERROR CRÍTICO: No se pudieron cargar todos los DataFrames. Saliendo.")
        return

    df_productos = all_data['productos']
    df_ordenes = all_data['ordenes']
    df_clientes = all_data['clientes']
    
    column_description_for_prefix = get_column_names_for_prefix(all_data)

    agent_prefix = f"""
Eres un agente experto en análisis de datos con Pandas. Tu tarea es responder a la PREGUNTA ACTUAL DEL USUARIO generando y ejecutando código Python usando la herramienta `python_repl_ast`.

**Formato Estricto para Acciones:**
Cuando decidas usar la herramienta `python_repl_ast`, DEBES usar el siguiente formato EXACTO:
Action: python_repl_ast
Action Input: [TU CÓDIGO PYTHON AQUÍ. El código debe ser completo y ejecutable. Usa `print()` en tu código para que el resultado de una operación clave sea la Observación.]

**Información de los DataFrames Disponibles (df1: productos, df2: órdenes, df3: clientes):**
{column_description_for_prefix}

**Proceso de Pensamiento y Respuesta (¡MUY IMPORTANTE!):**
1.  **Analiza la PREGUNTA ACTUAL DEL USUARIO.** No te desvíes por preguntas o información de turnos anteriores, a menos que la pregunta actual explícitamente se refiera a ello.
2.  **Planifica los Pasos:** Decide qué información necesitas y de qué DataFrame(s) (`df1`, `df2`, `df3`). Piensa en la secuencia de operaciones Pandas.
3.  **Ejecuta Código (Acción):** Genera UNA acción Pandas lógica a la vez usando el formato `Action: python_repl_ast` y `Action Input: [código]`.
4.  **Observa el Resultado:** La salida de tu código (la Observación) es la información que has recuperado.
5.  **Decide y Concluye (¡CLAVE!):**
    * **Si la Observación contiene la respuesta directa o la pieza final de información que necesitas para responder a la PREGUNTA ACTUAL DEL USUARIO, ¡DEBES CONCLUIR! Tu siguiente paso NO debe ser otra `Action: python_repl_ast`. En su lugar, debes proporcionar la "Final Answer" al usuario.**
    * Por ejemplo, si la pregunta es "¿Cuál es el nombre del cliente X?" y tu código `print(df3[df3['Customer_ID']=='X']['Customer_Name'].iloc[0])` produce la Observación "Nombre Apellido", entonces tu siguiente paso es: `Final Answer: El nombre del cliente X es Nombre Apellido.`
    * Otro ejemplo: si para "producto con más pérdidas por devolución" obtienes el `Product_ID` en una observación, y luego el `Product_Name` en la siguiente observación, y ya tienes ambas piezas, ¡CONCLUYE con la "Final Answer"!
    * Si la Observación indica que necesitas un paso más (ej. obtuviste un ID y ahora necesitas el nombre), entonces sí, realiza otra `Action: python_repl_ast`.
6.  **Respuesta Final:** Cuando tengas la respuesta, formúlala en lenguaje natural.

**Consideraciones de Código Pandas:**
- **`df1` (productos):** Para nombres de productos (`Product_Name`) usando `Product_ID`.
- **`df2` (órdenes):** Para ventas, transacciones. Columnas: `Order_ID`, `Product_ID`, `Customer_ID`, `City` (envío), `Sales`, `Quantity`, `Profit`, `Return`. Todas las columnas numéricas importantes ya son del tipo correcto.
    - Para "producto con más pérdidas por devoluciones" (interpretando pérdida como `Sales` de ítems devueltos):
        a. `df_returned = df2[df2['Return'] == 1]`
        b. `sales_lost_per_product = df_returned.groupby('Product_ID')['Sales'].sum()`
        c. `top_product_id_lost = sales_lost_per_product.idxmax()` (Observa este ID)
        d. `max_sales_lost = sales_lost_per_product.max()` (Observa este valor)
        e. `top_product_name = df1.loc[df1['Product_ID'] == top_product_id_lost, 'Product_Name'].iloc[0]` (Observa este nombre)
        f. Luego, con `top_product_name` y `max_sales_lost`, da la "Final Answer".
- **`df3` (clientes):** Para `Customer_Name` usando `Customer_ID`.

Ahora, responde la PREGUNTA ACTUAL DEL USUARIO.
"""

    try:
        print("Inicializando Pandas DataFrame Agent...")
        agent_executor = create_pandas_dataframe_agent(
            llm,
            [df_productos, df_ordenes, df_clientes],
            prefix=agent_prefix,
            agent_executor_kwargs={
                "handle_parsing_errors":True,
                 # Considera añadir un OutputFixingParser si los errores de formato persisten mucho
            },
            verbose=True,
            allow_dangerous_code=True,
            max_iterations=10, # Démosle un poco de espacio si los pasos son legítimamente múltiples
        )
        print("¡Agente Pandas listo!")
    except Exception as e:
        print(f"Error inicializando el agente Pandas: {e}")
        return

    print("\nPuedes empezar a hacer preguntas analíticas sobre tus datos.")
    print("Escribe 'salir' o 'q' para terminar la conversación.")

    while True:
        user_question = input("\nTú: ")
        if user_question.lower() in ['salir', 'q']:
            print("Agente: ¡Hasta luego!")
            break
        if not user_question.strip():
            continue

        print("\nAgente pensando y analizando datos...")
        try:
            response = agent_executor.invoke({"input": user_question})
            print(f"\nAgente: {response['output']}")
        except Exception as e:
            print(f"  ERROR al procesar la pregunta con el Agente Pandas: {e}")
            import traceback
            traceback.print_exc()
        print("\n----------------------------------------------------")

if __name__ == "__main__":
    if not all(os.path.exists(f) for f in [PRODUCTS_FILE, ORDERS_FILE, CUSTOMERS_FILE]):
        print(f"ERROR: Uno o más archivos CSV ({PRODUCTS_FILE}, {ORDERS_FILE}, {CUSTOMERS_FILE}) no se encontraron.")
    else:
        main()