# -*- coding: utf-8 -*-

from bika.lims.interfaces import IDoNotSupportSnapshots
from senaite.core.interfaces import IHideActionsMenu
from senaite.lims.interfaces import ISenaiteLIMS
from senaite.patient.interfaces import ISenaitePatientLayer
from zope.interface import Interface


class ISenaiteDiagnosisLayer(ISenaiteLIMS, ISenaitePatientLayer):
    """Zope 3 browser Layer interface specific for senaite.diagnosis
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class IContentFolder(IHideActionsMenu, IDoNotSupportSnapshots):
    """Marker interface for basic containers
    """


class IAetiologicAgents(IContentFolder):
    """Marker interface for container of Aetiologic Agents
    """


class IAetiologicAgent(Interface):
    """Marker interface for Aetiologic Agent objects
    """


class IDiseases(IContentFolder):
    """Marker interface for container of Diseases
    """


class IDisease(Interface):
    """Marker interface for Disease objects
    """


class ISymptoms(IContentFolder):
    """Marker interface for container of Symptoms
    """


class ISymptom(Interface):
    """Marker interface for Symptom objects
    """
