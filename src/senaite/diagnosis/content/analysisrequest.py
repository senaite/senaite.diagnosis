# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DIAGNOSIS.
#
# SENAITE.DIAGNOSIS is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2022 by it's authors.
# Some rights reserved, see README and LICENSE.

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import IAnalysisRequest
from Products.CMFCore.permissions import View
from senaite.core.browser.widgets import DateTimeWidget
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.catalog import SETUP_CATALOG
from senaite.diagnosis import messageFactory as _
from senaite.diagnosis import permissions
from senaite.diagnosis.content.fields import ExtDateTimeField
from senaite.diagnosis.content.fields import ExtUIDReferenceField
from senaite.diagnosis.interfaces import ISenaiteDiagnosisLayer
from zope.component import adapter
from zope.interface import implementer

NEW_FIELDS = [

    ExtUIDReferenceField(
        "Symptoms",
        allowed_types=("Symptom", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditSymptoms,
        widget=ReferenceWidget(
            label=_(u"Signs and Symptoms"),
            description=_(
                u"Observed or detectable signs, and experienced symptoms of an "
                u"illness, injury, or condition"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
            showOn=True,
        )
    ),

    ExtDateTimeField(
        "DateOfOnset",
        required=False,
        read_permission=View,
        write_permission=permissions.FieldEditDateOfOnset,
        widget=DateTimeWidget(
            render_own_label=True,
            label=_(u"Date of Onset"),
            description=_(
                u"Date when the signs and symptoms were first noted"
            ),
            show_time=False,
            visible={
                "add": "edit"
            },
        ),
    ),

    ExtUIDReferenceField(
        "Diseases",
        allowed_types=("Disease", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditDiseases,
        widget=ReferenceWidget(
            label=_(u"Diseases or conditions"),
            description=_(
                u"Particular abnormal conditions that negatively affect the "
                u"structure or function of all or part of an organism. Often "
                u"known to be medical conditions that are associated with "
                u"specific signs and symptoms"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
            showOn=True,
        )
    ),

    ExtDateTimeField(
        "DateOfDiagnosis",
        required=False,
        read_permission=View,
        write_permission=permissions.FieldEditDateOfDiagnosis,
        widget=DateTimeWidget(
            render_own_label=True,
            label=_(u"Date of Diagnosis"),
            description=_(
                u"Date when the diagnosis, as the process of identifying a "
                u"disease, condition or injure from its signs and symptoms, "
                u"was determined"
            ),
            show_time=False,
            visible={
                "add": "edit"
            },
        ),
    ),

    ExtUIDReferenceField(
        "EtiologicAgents",
        allowed_types=("EtiologicAgent", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditEtiologicAgents,
        widget=ReferenceWidget(
            label=_(u"Etiologic agents"),
            description=_(
                u"Infectious agents (microorganisms or toxins) that cause or "
                u"may cause the disease or diseases"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
            showOn=True,
        )
    ),

]


@adapter(IAnalysisRequest)
@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    """Extends the Sample (aka AnalysisRequest) with additional fields
    """
    layer = ISenaiteDiagnosisLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):  # noqa CamelCase
        return NEW_FIELDS
