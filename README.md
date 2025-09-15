Cripto App 🚀

Conoce los detalles sobre todas las criptomonedas que hay en el mercado. Antes de entrar en el ecosistema cripto, es de vital importancia saber qué hay detrás de cada proyecto, el nivel de descentralización de cada cripto, su organización si la hay, sus creadores, su arquitectura o su historia.

Además de toda esta información, esta web facilita el precio en tiempo real y otros datos financieros, obtenidos a través de la plataforma CoinGecko.

Pero este proyecto no se queda aquí. También queremos explicarte cualquier concepto cripto con el que tengas dudas. ¿Qué es el staking o la minería cripto? ¿Qué es un exchange descentralizado? ¿Qué peligros tiene un proyecto cripto?

Aprende todo lo relativo al mundo cripto a través de nuestra plataforma, pregunta todo lo que quieras y aprovecha los datos en tiempo real que te ofrecemos.

📌 Características

💻 Frontend en HTML + CSS (templates)

⚡ Backend con Flask

🤖 Integración con Groq LLM

📊 Datos de criptos vía CoinGecko API

🗄️ Persistencia en PostgreSQL (AWS RDS)

📦 Imagen Docker lista para ejecutar en cualquier máquina

⚙️ Requisitos

🐍 Python 3.11+

🐳 Docker

🌐 Cuenta en DockerHub y GitHub (para despliegue)

▶️ Cómo ejecutar con Docker

Clonar el repo:

bash
git clone https://github.com/pedropas95/cripto-app.git
cd cripto-app


Crear archivo .env en la raíz (con tus credenciales):

env
GROQ_API_KEY=tu_api_key
DB_HOST=tu_host
DB_NAME=tu_db
DB_USER=tu_usuario
DB_PASS=tu_password
DB_PORT=5432


Construir la imagen en Docker:

bash
docker build -t cripto-app:latest .


Ejecutar el contenedor:

bash
docker run -p 8000:8000 --env-file .env cripto-app:latest


Abrir en el navegador:

arduino
http://localhost:8000

🐳 DockerHub

La imagen está disponible en:
👉 DockerHub: pedropas95/cripto-app

📚 Autor

Pedro López Fontaneda – Proyecto final Bootcamp Data Analysis en The Bridge

🏗️ Arquitectura del proyecto
text
         👤 Usuario
              │
              ▼
       🌐 Interfaz Web (HTML/CSS/JS)
              │
              ▼
        ⚡ Flask Backend (Python)
              │
    ┌─────────┴──────────┐
    │                    │
    ▼                    ▼
 🤖 LLM (Groq API)   📊 CoinGecko API
    │                    │
    └─────────┬──────────┘
              ▼
      🗄️ Base de datos (PostgreSQL en AWS RDS)
              │
              ▼
         📜 Respuesta + Datos
              │
              ▼
         👤 Usuario final
