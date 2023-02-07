# smart_home_backend

Creating virtual environmentpip  in project directory:
   
   - `python -m venv venv`

   - `source venv/bin/activate`

Installing Packages:

 - Django and DRF

   `pip install django-rest-framework`

   `pip install django-cors-headers`

   `pip install python-dotenv`

 - Xiaomi Bluetooth
   
   `sudo apt-get install python3-pip libglib2.0-dev`

   `pip install lywsd03mmc`

 - Install pyModbusTCP, tinyTuya, w1thermsensor, requests, beautifulsoup4

    `pip install pyModbusTCP tinyTuya w1thermsensor`

    `pip install requests beautifulsoup4`

 - Celery and Docker

   `curl -sSL https://get.docker.com | sh`

   `sudo usermod -aG docker pi`

 - restart device necessary.!
 - go inside venv

   `sudo apt-get install rabbitmq-server`

   `docker run -d -p 5672:5672 rabbitmq`

   `pip install celery`


 - import `.env` file to project and run django server
 
   `python manage.py runserver 0:8000`

 - 

    `celery -A tasks worker --loglevel=INFO
`
