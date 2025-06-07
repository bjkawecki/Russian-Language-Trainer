import json
import logging
import sys
import traceback

from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.words.models.feature import (
    AdjectiveFeature,
    AdverbFeature,
    NumeralFeature,
    PrepositionFeature,
    PronounFeature,
    SubstantiveFeature,
    VerbFeature,
)
from apps.words.models.inflection import (
    AdjectiveInflection,
    NumeralInflection,
    PronounInflection,
    SubstantiveInflection,
    VerbInflection,
)
from apps.words.models.translation import Translation
from apps.words.models.word import Word

logger = logging.getLogger("debug")


class _InflectionCreation:
    def create_inflection(self, word, inflection):
        wordclass = word.wordclass
        wordclasses_with_inflection = [
            "adjective",
            "numeral",
            "pronoun",
            "substantive",
            "verb",
        ]
        if wordclass in wordclasses_with_inflection:
            create_inflection = self._choose_create_inflection_method(wordclass)
            create_inflection(word=word, inflection=inflection)

    def _choose_create_inflection_method(self, wordclass: str):
        wordclass_methods = {
            Word.WordClass.ADJECTIVE: self._create_adjective_inflection,
            Word.WordClass.NUMERAL: self._create_numeral_inflection,
            Word.WordClass.PRONOUN: self._create_pronoun_inflection,
            Word.WordClass.VERB: self._create_verb_inflection,
            Word.WordClass.SUBSTANTIVE: self._create_substantive_inflection,
        }
        return wordclass_methods[wordclass]

    def _create_adjective_inflection(self, word, inflection: dict):
        inflection_obj, _ = AdjectiveInflection.objects.update_or_create(
            word=word, defaults={**inflection}
        )

    def _create_numeral_inflection(self, word, inflection: dict):
        inflection_obj, _ = NumeralInflection.objects.update_or_create(
            word=word, defaults={**inflection}
        )

    def _create_pronoun_inflection(self, word, inflection: dict):
        inflection_obj, _ = PronounInflection.objects.update_or_create(
            word=word, defaults={**inflection}
        )

    def _create_substantive_inflection(self, word, inflection: dict):
        inflection_obj, _ = SubstantiveInflection.objects.update_or_create(
            word=word, defaults={**inflection}
        )

    def _create_verb_inflection(self, word, inflection: dict):
        inflection_obj, _ = VerbInflection.objects.update_or_create(
            word=word, defaults={**inflection}
        )


class _FeatureCreation:
    def create_feature(self, word, feature):
        wordclass = word.wordclass
        wordclasses_with_feature = [
            "adjective",
            "adverb",
            "numeral",
            "preposition",
            "pronoun",
            "substantive",
            "verb",
        ]
        if wordclass in wordclasses_with_feature:
            create_feature = self._choose_create_feature_method(wordclass)
            create_feature(word=word, feature=feature)

    def _choose_create_feature_method(self, wordclass: str):
        wordclass_methods = {
            Word.WordClass.ADJECTIVE: self._create_adjective_feature,
            Word.WordClass.ADVERB: self._create_adverb_feature,
            Word.WordClass.NUMERAL: self._create_numeral_feature,
            Word.WordClass.PREPOSITION: self._create_preposition_feature,
            Word.WordClass.PRONOUN: self._create_pronoun_feature,
            Word.WordClass.VERB: self._create_verb_feature,
            Word.WordClass.SUBSTANTIVE: self._create_substantive_feature,
        }
        return wordclass_methods[wordclass]

    def _create_adjective_feature(self, word, feature: dict):
        feature_obj, _ = AdjectiveFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_adverb_feature(self, word, feature: dict):
        feature_obj, _ = AdverbFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_numeral_feature(self, word, feature: dict):
        feature_obj, _ = NumeralFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_preposition_feature(self, word, feature: dict):
        feature_obj, _ = PrepositionFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_pronoun_feature(self, word, feature: dict):
        feature_obj, _ = PronounFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_substantive_feature(self, word, feature: dict):
        feature_obj, _ = SubstantiveFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )

    def _create_verb_feature(self, word, feature: dict):
        feature_obj, _ = VerbFeature.objects.update_or_create(
            word=word, defaults={**feature}
        )


class _WordObject:
    def __init__(self):
        self.unique_name = ""
        self.base = None
        self.meta = None
        self.translation = None
        self.feature = None
        self.inflection = None

    def __str__(self):
        return self.base.get("lemma", None)


class _WordBuilder:
    def __init__(self):
        self.word = _WordObject()

    def set_unique_name(self, unique_name):
        self.word.unique_name = unique_name
        return self

    def set_base(self, base):
        self.word.base = base
        return self

    def set_meta(self, meta):
        self.word.meta = meta
        return self

    def set_translation(self, translation):
        self.word.translation = translation
        return self

    def set_feature(self, feature):
        self.word.feature = feature
        return self

    def set_inflection(self, inflection):
        self.word.inflection = inflection
        return self

    def get_word(self):
        return self.word


class LoadCourseJSON:
    def __init__(self, json_file):
        self.json_file = json_file
        self.progress = 1
        self.fs = FileSystemStorage()
        self.json_file_fs_path = ""

    def _handle_json_file(self):
        json_file_name = self.json_file.name
        saved_json_file = self.fs.save(f"json/{json_file_name}", self.json_file)
        self.json_file_fs_path = self.fs.path(saved_json_file)
        return self.json_file_fs_path

    def _create_word_object(self, word):
        word_builder = _WordBuilder()
        try:
            word_object = (
                word_builder.set_unique_name(word.get("unique_name"))
                .set_base(word.get("base"))
                .set_meta(word.get("meta"))
                .set_translation(word.get("translation"))
                .set_feature(word.get("feature"))
                .set_inflection(word.get("inflection"))
                .get_word()
            )
        except Exception as err:
            logger.error(
                f"Unexpected {err=}, {type(err)=}, word {word}",
                traceback.format_exc(),
            )
            sys.exit(1)
        return word_object

    def _create_word_record(self, word_object):
        try:
            course_record, _ = Course.objects.get_or_create(
                name=word_object.meta.get("level")
            )
            deck_record, _ = Deck.objects.update_or_create(
                name=word_object.meta.get("topic"), course=course_record
            )
            word_record, created_word_record = Word.objects.update_or_create(
                unique_name=word_object.unique_name,
                defaults={
                    "deck": deck_record,
                    "course": course_record,
                    "audio": f"audio/{word_object.unique_name}.ogg",
                    **word_object.base,
                },
            )
        except Exception as err:
            logger.error(
                f"Unexpected {err=}, {type(err)=}, word {word_object}",
                traceback.format_exc(),
            )
            sys.exit(1)
        return word_record, created_word_record

    def _create_translation(self, translation_list, word_record):
        try:
            for element in translation_list:
                translation, _ = Translation.objects.get_or_create(name=element)
                translation.words.add(word_record)
        except Exception as err:
            logger.error(
                f"Unexpected {err=}, {type(err)=}, word {word_record}",
                traceback.format_exc(),
            )
            sys.exit(1)

    def _create_inflection(self, word_object, word_record):
        if word_object.inflection:
            try:
                inflection_creation = _InflectionCreation()
                inflection_creation.create_inflection(
                    word=word_record, inflection=word_object.inflection
                )
            except Exception as err:
                logger.error(
                    f"Unexpected {err=}, {type(err)=}, word {word_record}",
                    traceback.format_exc(),
                )
                sys.exit(1)

    def _create_feature(self, word_object, word_record):
        if word_object.feature:
            try:
                feature_creation = _FeatureCreation()
                feature_creation.create_feature(
                    word=word_record, feature=word_object.feature
                )
            except Exception as err:
                logger.error(
                    f"Unexpected {err=}, {type(err)=}, word {word_record}",
                    traceback.format_exc(),
                )
                sys.exit(1)

    def _log_creation_result(self, created_word_record, index, word_record):
        if created_word_record:
            logger.info(
                "{}: Successfully created new card object '{}'.".format(
                    index, word_record
                )
            )
        else:
            logger.info(
                "{}: Card object already exists: '{}'.".format(index, word_record)
            )

    def _set_progress(self, index):
        self.progress = index
        cache.set("course_progress", self.progress)

    def _clean_up(self):
        cache.delete("course_progress")
        logger.info("Reached end of file '{}'.".format(self.json_file))
        self.fs.delete(self.json_file_fs_path)

    def update_or_create_course(self) -> bool:
        """
        Create or update a collection of courses, decks and words with a json file,
        formatted as:[{"base": {...},"translation": [...],"meta": {...}, "feature": {...}}, "inflection": {...}}]
        """
        with open(self._handle_json_file()) as file:
            words = json.load(file)
        for index, word in enumerate(words, 1):
            with transaction.atomic():
                word_object = self._create_word_object(word)
                word_record, created_word_record = self._create_word_record(word_object)
                self._create_translation(word_object.translation, word_record)
                self._create_feature(word_object=word_object, word_record=word_record)
                self._create_inflection(
                    word_object=word_object, word_record=word_record
                )
                self._log_creation_result(created_word_record, index, word_record)
            self._set_progress(index)
        self._clean_up()
        return True
