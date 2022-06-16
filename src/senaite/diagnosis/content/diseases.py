# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.diagnosis.interfaces import IDiseases
from zope.interface import implementer


class IDiseasesSchema(model.Schema):
    """Schema interface
    """


@implementer(IDiseases, IDiseasesSchema)
class Diseases(Container):
    """Folder for Diseases contents
    """
