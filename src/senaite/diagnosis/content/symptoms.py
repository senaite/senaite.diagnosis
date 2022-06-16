# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.diagnosis.interfaces import ISymptoms
from zope.interface import implementer


class ISymptomsSchema(model.Schema):
    """Schema interface
    """


@implementer(ISymptoms, ISymptomsSchema)
class Symptoms(Container):
    """Folder for Symptoms contents
    """
