# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bika.lims.interfaces import IDeactivable
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.catalog import SETUP_CATALOG
from senaite.diagnosis import messageFactory as _
from senaite.diagnosis.interfaces import ISymptom
from senaite.diagnosis.utils import check_code
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


class ISymptomSchema(model.Schema):
    """Schema interface
    """

    code = schema.TextLine(
        title=_(u"Code"),
        required=True,
    )

    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    gender = schema.Choice(
        title=_(u"Gender"),
        description=_(
            u"Gender this symptom applies to"
        ),
        source="senaite.patient.vocabularies.gender",
        default="",
        required=False,
    )

    severity_levels = schema.Bool(
        title=_(u"Severity levels permitted"),
        description=_(
            u"Select if patient can experience different stress levels of this "
            u"symptom (none, mild, moderate, severe)"
        ),
        required=False,
    )

    @invariant
    def validate_code(data):
        """Checks if the code for this symptom is unique
        """
        code = data.code

        # https://community.plone.org/t/dexterity-unique-field-validation
        context = getattr(data, "__context__", None)
        if context is not None:
            if context.code == code:
                # nothing changed
                return

        check_code(code, context, portal_type="Symptom")


@implementer(ISymptom, ISymptomSchema, IDeactivable)
class Symptom(Container):
    """Disease type
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()
    exclude_from_nav = True

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname
        """
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname
        """
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].set

    @security.protected(permissions.View)
    def getCode(self):
        accessor = self.accessor("code")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setCode(self, value):
        if value == self.code:
            # Nothing changed
            return

        try:
            check_code(value, self)
        except Invalid as ex:
            raise ValueError(ex.message)

        mutator = self.mutator("code")
        mutator(self, value)

    @security.protected(permissions.View)
    def getGender(self):
        accessor = self.accessor("gender")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGender(self, value):
        mutator = self.mutator("gender")
        mutator(self, value)

    @security.protected(permissions.View)
    def getSeverityLevels(self):
        accessor = self.accessor("severity_levels")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setSeverityLevels(self, value):
        mutator = self.mutator("severity_levels")
        mutator(self, value)
