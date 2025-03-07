# -*- coding: utf-8 -*-

from senaite.diagnosis import _
from senaite.diagnosis.vocabularies import SimpleVocabularyFactory


CASE_STATUSES_VOCABULARY_ID = "senaite.diagnosis.vocabularies.case.statuses"
CASE_OUTCOMES_VOCABULARY_ID = "senaite.diagnosis.vocabularies.case.outcomes"

CASE_STATUSES = (
    ("o", _("Outbreak")),
    ("c", _("Single case")),
    ("s", _("Survey")),
    ("u", _("Unknown")),
    ("", _("Not Specified")),
)

CASE_OUTCOMES = (
    ("d", _("Patient died")),
    ("h", _("Patient hospitalized")),
    ("", _("Not Specified")),
)

CaseStatusesVocabularyFactory = SimpleVocabularyFactory(CASE_STATUSES)
CaseOutcomesVocabularyFactory = SimpleVocabularyFactory(CASE_OUTCOMES)
