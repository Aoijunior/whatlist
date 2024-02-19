# Bot de WhatsApp Automatizado 

Este proyecto consiste en una aplicación web desarrollada con Streamlit que permite enviar mensajes personalizados a través de WhatsApp Web de manera automatizada. La aplicación carga un archivo con los datos de los contactos, filtra los destinatarios según criterios específicos, y envía mensajes personalizados a cada uno de ellos.

## Características principales

- Interfaz intuitiva: La aplicación presenta una interfaz de usuario fácil de usar, con instrucciones claras para guiar al usuario a través del proceso de envío de mensajes.
- Filtros avanzados: Permite aplicar filtros avanzados para seleccionar los destinatarios de manera precisa, según criterios como edad, ubicación geográfica, etc.
- Personalización de mensajes: Permite personalizar los mensajes con variables que se reemplazan automáticamente por los datos de los contactos, como el nombre, el apellido, etc.
- Automatización: Una vez configurados los filtros y redactado el mensaje, la aplicación envía automáticamente los mensajes a través de WhatsApp Web, sin intervención manual del usuario.

## Tecnologías utilizadas

- Streamlit: Se utiliza como framework para construir la interfaz de usuario de la aplicación.
- Pandas: Se utiliza para la manipulación y análisis de datos, especialmente para cargar y filtrar los datos de los contactos.
- PyAutoGUI: Se utiliza para la automatización de acciones en el navegador web, como hacer clic y escribir texto en WhatsApp Web.
- Requests: Se utiliza para enviar los mensajes codificados a URL para que se redacten de manera correcta en Whatsapp Web.

## Instalación y ejecución

Para ejecutar la aplicación de forma local, sigue estos pasos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias del proyecto ejecutando `pip install -r requirements.txt`.
3. Ejecuta la aplicación con el comando `streamlit run main.py`.
4. Accede a la aplicación en tu navegador web en la dirección `http://localhost:8501`.

## Contribuciones y problemas conocidos

Este proyecto está en constante desarrollo, por lo que las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna sugerencia de mejora, no dudes en abrir un issue en este repositorio.

## Autor

Este proyecto fue desarrollado por [Junior Alata Sihues](https://github.com/Aoijunior).

---