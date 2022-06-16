# -*- coding: utf-8 -*-
import re
from zope.interface import Invalid
from senaite.core.catalog import SETUP_CATALOG
from bika.lims import api
from senaite.diagnosis import messageFactory as _


def is_valid_code(value):
    """Return whether the value can be used as code, without special characters
    except '-' and without empties
    """
    if not value:
        return False
    regex = r'^[a-zA-Z0-9\-]*$'
    if re.match(regex, value):
        return True
    return False


def check_code(code, context, portal_type=None, catalog=SETUP_CATALOG):
    """Raises an Invalid exception if the symptom code passed-in is not valid
    or not unique
    """
    if not is_valid_code(code):
        raise Invalid(_("Code cannot contain special characters or spaces"))

    if not portal_type:
        portal_type = api.get_portal_type(context)

    query = {"portal_type": portal_type}
    for brain in api.search(query, catalog):
        obj = api.get_object(brain)
        if obj.code == code:
            if obj != context:
                raise Invalid(_("Code must be unique"))
