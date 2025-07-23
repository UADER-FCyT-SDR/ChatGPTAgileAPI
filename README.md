# ChatGPTAgileAPI

Scripts utilizados para evaluar preliminarmente la aplicabilidad, ventajas y desventajas de utilizar grandes modelos
de lenguaje (LLM) durante el ciclo de desarrollo de software, específicamente en la tarea de evaluar requerimientos
con el objetivo de identificar casos de prueba (test cases), resaltar problemas en forma temprana y evaluar tanto
la completitud como la com-plejidad de los requerimientos.

El uso de ésta tecnología tiene un potencial enorme para mejorar la calidad en un proyecto de construcción de software
mediante el incremento significativo de la productividad de validación y verificación reduciendo por lo tanto el retrabajo
necesario por lo que puede producir ventajas significativas en el costo para el desarrollo, la calidad obtenida y la
satisfacción del cliente.

Utilizado para la evaluación realizada en el artículo

*Uso de grandes modelos conversacionales de lenguaje para generar casos de prueba bajo metodologías ágiles*

# Instalación

* Colocar los requerimientos a procesar como archivos de texto independientes con extensión .req
* Actualizar el script processWER.sh con la clave OPENAI_KEY_API
* Asegurarse de tener instalado Python 3
* Ejecutar el script processWER.sh
* Obtener los resultados como archivos .txt y .log 
