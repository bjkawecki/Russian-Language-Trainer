# Russian Language Trainer 'Bajkal'

![Python](https://img.shields.io/badge/Python-FFD43B?style=flat-square&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=green)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![Postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=flat-square&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker%20Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![htmx](https://img.shields.io/badge/%3C/%3E%20htmx-3D72D7?style=flat-square&logo=mysl&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy-777BB4?style=flat-square&logo=numpy&logoColor=white)

![logo](assets/logo.png)

**Bajkal** is a web application for learning Russian. It combines modern language learning techniques such as spaced repetition, automated learning decks, audio support, and progress tracking, and includes app features like course booking and user accounts.

---

## Features

- **Vocabulary trainer with spaced repetition**
- **Automatically generated learning decks** (feed)
- **Integrated dictionary with search functionality**
- **Audio pronunciation for vocabulary**
- **Learning progress tracking**
- **User accounts & course booking** (currently A1 & A2)
- **Mobile-optimized frontend**

Planned:

- Public dictionary page
- Grammar trainer
- Expansion to course level C1

---

## Tech-Stack

- **Backend:** Django + Gunicorn
- **Frontend:** Django Templates + HTMX
- **Database:** PostgreSQL
- **Queueing:** Redis + Celery
- **Deployment:** Docker Compose + Nginx Reverse Proxy
