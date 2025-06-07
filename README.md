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

**Bajkal** ist eine Webanwendung zum Russischlernen. Sie kombiniert moderne Sprachlerntechniken wie Spaced Repetition, automatisierte Lernstapel, Audio-Unterstützung und Fortschrittsverfolgung und beinhaltet App-Features wie Kursbuchung und Benutzerkonten.

---

## Features

- **Vokabeltrainer** mit _Spaced Repetition_
- **Automatisch erzeugte Lernstapel** (Feed)
- **Integriertes Wörterbuch** mit Suchfunktion
- **Audio-Aussprache** für Vokabeln
- **Lernfortschrittsanzeige**
- **Benutzerkonten** & **Kurse buchen** (aktuell A1 & A2)
- **Mobile-optimiertes Frontend**

Geplant:

- Öffentliche Wörterbuchseite
- Grammatiktrainer
- Erweiterung auf Kursniveau C1

---

## Tech-Stack

- **Backend:** Django + Gunicorn
- **Frontend:** Django Templates
- **Datenbank:** PostgreSQL
- **Queueing:** Redis + Celery
- **Deployment:** Docker Compose mit Nginx Reverse Proxy
