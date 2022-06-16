# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.diagnosis.interfaces import IAetiologicAgents
from zope.interface import implementer


class IAetiologicAgentsSchema(model.Schema):
    """Schema interface
    """


@implementer(IAetiologicAgents, IAetiologicAgentsSchema)
class AetiologicAgents(Container):
    """Folder for Aetiologic Agent contents
    """
