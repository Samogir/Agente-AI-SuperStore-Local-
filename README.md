# Agente-AI-SuperStore-Local-
Agente de inteligencia artificial corriendo de manera local en un computador.
## Descripción 
Este proyecto se realizó con el fin de poder ejectuar un agente de inteligencia artificial que se pudiera correr de manera local, para este caso utilizaremos Llama 3.2, pero se puede utilizar cualquiera de los otros modelos disponibles.
## Procedimiento
### Obtener los datos
Para la adquisición de los datos recurrí a los archivos .csv encontrados [aquí](https://github.com/joselquin/SuperStore_sales?tab=readme-ov-file).
La estructura de las tablas es de la siguiente manera:

La tabla Productos tiene las siguientes columnas: Product_ID, Category, Sub_Category, Product_Name

La tabla clientes tiene las siguientes columnas: Customer_ID, Customer_Name, Segment, Country, City, State, Postal_Code, Region

La tabla Ordenes tiene las siguientes columnas: Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID, City, Product_ID, Sales, Quantity, Discount, Profit, Return
### Instalación de Ollama
Nos dirigimos al sitio web de (Ollama)[https://ollama.com/], y hacemos click en el botón que dice "Download". Una vez haya descargado el archivo abrimos en windows la terminal (se busca directamente en el buscador del pc)

En la terminal escribimos "ollama" y nos debería desplegar una lista con los comandos disponibles, esto nos hace entender de que ollama se instaló correctamente en nuestro computador, ahora hacemos el llamado al modelo que deseamos descargar, para este proyecto utilizaremos Llama 3.2 que nos entrega un buen rendimiento y no necesitamos GPU's demasiado potentes para correrlo.

Entonces para hacer la solicitud e instalar llama 3.2 escribimos en el terminal que tenemos abierto "pull llama3.2" y esperamos a que descargue, nos mostrará el progreso el mismo terminal. También debemos descargar un modelo embedido, para esto escribimos en la terminal lo siguiente: "pull mxbai-embed-large" y esperamos a que termine la descarga.

### Creación de entorno virtual.
Para la creación del entorno virtual primero debemos crear una carpeta, en la cual estará nuestro proyecto, una vez creada la carpeta entramos en ella y abrimos un "command window" dentro de ella y utilizaremos los siguietnes comandos:

-Creación del entorno virtual:
python -m venv venv

Activación del entorno virtual:
./venv/Scripts/activate

Después se instalarán los requirements en el entorno virtual para poder realizar el trabajo.
pip install -r .\requirements.txt

Para desactivar(lo utilizaremos cuando terminemos de usar el agente):
deactivate

### Correr el agente. 
Para correr nuestro agente virtual utilizaremos el comando directamente desde el command window python agent_with_pandas.py y allí mismo nos mostrará la interface para interactuar con nuestro agente y comenzar a hacerle las preguntas sobre la base de datos.
