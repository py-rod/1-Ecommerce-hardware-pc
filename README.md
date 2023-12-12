# Proyecto de E-commerce de Hardware de PC

Este es un pequeño proyecto sobre un e-commerce enfocado en la venta de hardware de PC.

## Tecnologías Utilizadas

1. Python
2. Django
3. HTML
4. CSS
5. JavaScript

## Características Implementadas

- **Sistema de Pagos con PayPal**
- **Sistema de Comentarios para los Productos**
- **Perfil del Usuario**
- **Operaciones en el Carrito de Compras: Añadir, Incrementar, Eliminar productos, y más**
- **Activación de Cuenta por Correo Electrónico**

## Instalación

Para instalar y ejecutar localmente este proyecto, sigue estos pasos:

1. Clone este repositorio.
2. Ejecute el servidor Django con el comando `python manage.py runserver`.
3. Abra su navegador y vaya a `http://localhost:8000`.

## Capturas de Pantalla

![Captura desde 2023-12-11 12-57-44](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/6fcf5da2-aa92-4740-acd5-d8643c289aec)


![Captura desde 2023-12-11 12-57-56](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/a54d5434-9c59-4d2f-8609-8da6008bd7b4)


![Captura desde 2023-12-11 12-58-07](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/b32d3c2b-3b7f-4496-81f2-13cd6ee3393d)


![Captura desde 2023-12-11 13-12-33](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/bec0dfe7-4b7a-465a-a30b-54f671fbfa03)


![Captura desde 2023-12-11 12-58-45](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/98fdcd84-e362-43fb-b01f-570c2b2b4e6f)


![Captura desde 2023-12-11 13-04-07](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/fad4cc6f-fd91-4bee-857d-a363dedd2cef)


![Captura desde 2023-12-11 13-08-58](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/76bfe04d-594f-433f-b97d-2dbc76fbc831)


![Captura desde 2023-12-11 13-09-11](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/10b0bba0-ddad-4f31-bde7-c41793cd0eff)


![Captura desde 2023-12-11 13-09-48](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/d29412bd-5de6-4b36-98a3-caa51e60403c)

## Instrucciones de Uso

### Configuración del Método de Pago con PayPal

1. Visita el siguiente [enlace](https://developer.paypal.com/demo/checkout/#/pattern/server).

   ![Captura de pantalla 1](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/b560c572-a827-4cec-aa10-fd93d2d775e5)

   Una vez en el enlace, copia el pequeño script que se muestra en la siguiente captura:

   ![Captura de pantalla 2](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/dffff4e0-9d98-40e0-bc03-03d134d70891)

2. Abre el archivo `index/templates/layouts/base.html`. Busca la sección indicada por la siguiente imagen y reemplaza el script actual con el que acabas de copiar del primer enlace.

   ![Captura de pantalla 3](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/38c4549e-0b14-4a51-8125-cb92493f0e59)

   Con estos pasos, habrás configurado el método de pago con PayPal.

### Configuración de la Cuenta de PayPal

1. Visita el [Panel de Desarrolladores de PayPal](https://developer.paypal.com/home/) y crea una cuenta o inicia sesión si ya tienes una.

2. Navega a la pestaña "Apps & Credentials" y haz clic en "Create app".

   ![Captura de pantalla 4](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/ee3f79a7-dc2f-46dd-b1bd-558d570b8676)

3. En la ventana emergente, ingresa el nombre de la app, elige un correo electrónico en "Sandbox Account", y haz clic en "Create app".

   ![Captura de pantalla 5](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/a4a1db7f-cb23-4a66-aeeb-5f845bc6c49a)

4. Copia el "CLIENT ID" de la nueva app creada.

   ![Captura de pantalla 6](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/6e3de8c7-72a5-4966-83c1-676c0d607fb5)

5. Vuelve al archivo `base.html` y reemplaza la parte de la URL `client-id=test` con tu "CLIENT ID" copiado.

   ![Captura de pantalla 7](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/5eb47644-39b2-4f56-b296-dec68bf82e02)

6. Avanza a la sección "SandBox Accounts" y haz clic en "Create Account".

   ![Captura de pantalla 8](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/d4ffac22-6278-4551-a5e2-415f5f480fb1)

7. Completa los detalles en la ventana emergente, y al finalizar, haz clic en "Create".

   ![Captura de pantalla 9](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/f85f1cdc-b33c-400c-b07c-7087648c1ece)

Con estos pasos, habrás completado la configuración del método de pago y la cuenta de PayPal para tu proyecto.

## Configuración de Correo Electrónico para Activación de Cuenta

Para que la activación de cuenta funcione, sigue estos pasos adicionales:

1. Dirígete a la configuración de tu cuenta de Google. Puedes acceder haciendo clic en tu perfil y seleccionando "Manage your Google Account".

    ![Captura de pantalla 1](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/cb1abb73-0377-4cb5-8448-1660a2e4539b)

2. En la sección de seguridad, selecciona "Verificación de dos pasos". Es posible que se te pida que ingreses tu contraseña.

    ![Captura de pantalla 2](https://github.com/py-rod/1-Ecommerce-hardware-pc/assets/103091079/1c1d6883-cc27-40cd-bbb6-523da5650e1e)

3. Desplázate hacia abajo hasta la sección "Contraseñas de aplicaciones", haz clic y se te pedirá un nombre. Proporciona un nombre y haz clic en "Crear". Se abrirá una ventana con una llave; copia esa llave, ya que la necesitarás.

4. Ve a la carpeta de tu proyecto `core`. Dentro de `core`, crea un archivo llamado `.env`.

5. Rellena y guarda el archivo `.env` con la siguiente información:

```dotenv
SECRET_KEY=[Pegar la clave secreta generada de la página aquí]
DEBUG=True
EMAIL_FROM=[Colocar el correo electrónico con el que creaste la aplicación]
EMAIL_HOST_USER=[Colocar el correo electrónico con el que creaste la aplicación]
EMAIL_HOST_PASSWORD=[Colocar la llave que obtuviste al crear la aplicación]
