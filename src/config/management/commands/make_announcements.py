import logging
import os
import re

import markdown
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.announcements.models import Announcement

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Parse Markdown files from a specified folder and store them in the Announcement model"

    def handle(self, *args, **kwargs):
        markdown_folder = os.path.join(
            settings.BASE_DIR, "config", "messages"
        )  # Stelle sicher, dass dieser Ordner existiert
        if not os.path.exists(markdown_folder):
            self.stdout.write(
                self.style.ERROR(
                    "Der Ordner mit den Markdown-Dateien wurde nicht gefunden."
                )
            )
            return

        for filename in os.listdir(markdown_folder):
            if filename.endswith(".md"):
                file_path = os.path.join(markdown_folder, filename)
                with open(file_path, "r") as file:
                    markdown_content = file.read()

                    # Verarbeite die Frontmatter und den Inhalt
                    metadata, content = self.parse_frontmatter(
                        filename, markdown_content
                    )
                    print(metadata)
                    # Konvertiere Markdown zu HTML
                    html_content = markdown.markdown(content)

                    if Announcement.objects.filter(
                        title=metadata.get("title")
                    ).exists():
                        self.stdout.write(
                            self.style.NOTICE(
                                f"Title for parsed {filename} already exists."
                            )
                        )
                    else:
                        Announcement.objects.create(
                            category=1,
                            is_active=True,
                            starting_at=timezone.now(),
                            title=metadata.get("title", "Kein Titel"),
                            message=html_content,
                        )

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully parsed {filename} and created a announcement."
                            )
                        )

    def parse_frontmatter(self, filename, markdown_text):
        """Verarbeitet das Frontmatter (YAML) und extrahiert den Inhalt."""

        # Suche nach einem YAML-Block am Anfang der Datei (zwischen ---)
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", markdown_text, re.DOTALL)
        if match:
            frontmatter_content = match.group(1)  # Der YAML-Teil
            content = match.group(2)  # Der restliche Markdown-Inhalt

            try:
                # Parsen des YAML-Teils
                metadata = yaml.safe_load(frontmatter_content)
            except yaml.YAMLError as e:
                self.stdout.write(
                    self.style.ERROR(f"Fehler beim Parsen des Frontmatters: {e}")
                )
                metadata = {}

            return metadata, content
        else:
            # Kein Frontmatter vorhanden, gehe mit dem gesamten Text weiter
            return {}, markdown_text
