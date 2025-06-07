import json
import logging

from django.core.files.storage import FileSystemStorage
from django.db import transaction

from apps.proverbs.models import Proverb

logger = logging.getLogger("django")


class LoadProverbsJSONMixin:
    def save_proverbs_from_file(self, json_file):
        """
        Handles saving or updating proverbs from a JSON file.
        """
        file_path = self._save_temp_file(json_file)
        success = True
        try:
            proverbs = self._load_proverbs_from_file(file_path)
            self._update_or_create_proverbs(proverbs)
        except Exception as e:
            logger.error(f"Failed to process proverbs file: {e}")
            raise
        finally:
            self._delete_temp_file(file_path)
        return success

    def _save_temp_file(self, json_file):
        """Save the uploaded file temporarily and return its path."""
        fs = FileSystemStorage()
        file_name = fs.save(f"json/{json_file.name}", json_file)
        return fs.path(file_name)

    def _load_proverbs_from_file(self, file_path):
        """Load proverbs from a JSON file."""
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON file: {file_path}. Error: {e}")
                raise ValueError("The provided file is not a valid JSON.")

    @transaction.atomic
    def _update_or_create_proverbs(self, proverbs):
        """Update or create proverbs in the database."""
        for proverb_dict in proverbs:
            try:
                self._process_proverb(proverb_dict)
            except KeyError as e:
                logger.warning(f"Missing expected key in proverb: {e}. Skipping entry.")
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Skipping entry.")

    def _process_proverb(self, proverb_dict):
        """Process a single proverb dictionary."""
        Proverb.objects.update_or_create(
            proverb_id=proverb_dict["proverb_id"],
            defaults={
                "proverb": proverb_dict["proverb"],
                "translation": proverb_dict["translation"],
                "explanation": proverb_dict["explanation"],
                "equivalent": proverb_dict["equivalent"],
            },
        )
        logger.info(f"Proverb processed: {proverb_dict['proverb_id']}")

    def _delete_temp_file(self, file_path):
        """Delete the temporary file."""
        fs = FileSystemStorage()
        fs.delete(file_path)
