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
# Copyright 2022-2024 by it's authors.
# Some rights reserved, see README and LICENSE.

from archetypes.schemaextender.field import ExtensionField as ATExtensionField
from bika.lims.browser.fields import UIDReferenceField
from Products.Archetypes.Field import StringField
from Products.Archetypes.public import TextField
from senaite.core.browser.fields.datetime import DateTimeField


class ExtensionField(ATExtensionField):
    """Mix-in class to make Archetypes fields not depend on generated accessors
    and mutators, and use AnnotationStorage by default
    """

    def __init__(self, *args, **kwargs):
        super(ExtensionField, self).__init__(*args, **kwargs)


class ExtUIDReferenceField(ExtensionField, UIDReferenceField):
    """Field Extender of core's UIDReferenceField for AT types
    """


class ExtDateTimeField(ExtensionField, DateTimeField):
    """Field extender of core's DateTimeField
    """


class ExtStringField(ExtensionField, StringField):
    """Field extender of StringField
    """


class ExtTextField(ExtensionField, TextField):
    """Extended Text Field
    """
