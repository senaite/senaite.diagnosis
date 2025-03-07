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

from bika.lims import api
from plone.registry.interfaces import IRegistry
from senaite.core.api.workflow import update_workflow
from senaite.core.workflow import SAMPLE_WORKFLOW
from senaite.diagnosis import logger
from senaite.diagnosis import permissions
from senaite.diagnosis.config import PRODUCT_NAME
from senaite.diagnosis.config import PROFILE_ID
from zope.component import getUtility


# Tuples of (folder_id, folder_name, type)
SETUP_FOLDERS = [
    ("etiologic_agents", "Etiologic Agents", "EtiologicAgents"),
    ("diseases", "Diseases and Conditions", "Diseases"),
    ("symptoms", "Signs and Symptoms", "Symptoms"),
]

# Workflow updates
WORKFLOWS_TO_UPDATE = {
    SAMPLE_WORKFLOW: {
        "states": {
            "verified": {
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditDateOfDiagnosis: (),
                    permissions.FieldEditDateOfOnset: (),
                    permissions.FieldEditDiseases: (),
                    permissions.FieldEditEtiologicAgents: (),
                    permissions.FieldEditSymptoms: (),
                    permissions.FieldEditDiagnosis: (),
                    permissions.FieldEditAdditionalNotes: (),
                    permissions.FieldEditCaseStatus: (),
                    permissions.FieldEditCaseOutcome: (),
                }
            },
            "published": {
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditDateOfDiagnosis: (),
                    permissions.FieldEditDateOfOnset: (),
                    permissions.FieldEditDiseases: (),
                    permissions.FieldEditEtiologicAgents: (),
                    permissions.FieldEditSymptoms: (),
                    permissions.FieldEditDiagnosis: (),
                    permissions.FieldEditAdditionalNotes: (),
                    permissions.FieldEditCaseStatus: (),
                    permissions.FieldEditCaseOutcome: (),
                }
            },
            "rejected": {
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditDateOfDiagnosis: (),
                    permissions.FieldEditDateOfOnset: (),
                    permissions.FieldEditDiseases: (),
                    permissions.FieldEditEtiologicAgents: (),
                    permissions.FieldEditSymptoms: (),
                    permissions.FieldEditDiagnosis: (),
                    permissions.FieldEditAdditionalNotes: (),
                    permissions.FieldEditCaseStatus: (),
                    permissions.FieldEditCaseOutcome: (),
                }
            },
            "invalid": {
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditDateOfDiagnosis: (),
                    permissions.FieldEditDateOfOnset: (),
                    permissions.FieldEditDiseases: (),
                    permissions.FieldEditEtiologicAgents: (),
                    permissions.FieldEditSymptoms: (),
                    permissions.FieldEditDiagnosis: (),
                    permissions.FieldEditAdditionalNotes: (),
                    permissions.FieldEditCaseStatus: (),
                    permissions.FieldEditCaseOutcome: (),
                }
            },
            "cancelled": {
                "permissions": {
                    # Field permissions (read-only)
                    permissions.FieldEditDateOfDiagnosis: (),
                    permissions.FieldEditDateOfOnset: (),
                    permissions.FieldEditDiseases: (),
                    permissions.FieldEditEtiologicAgents: (),
                    permissions.FieldEditSymptoms: (),
                    permissions.FieldEditDiagnosis: (),
                    permissions.FieldEditAdditionalNotes: (),
                    permissions.FieldEditCaseStatus: (),
                    permissions.FieldEditCaseOutcome: (),
                }
            }
        }
    }
}


def setup_handler(context):
    """Generic setup handler
    """
    if context.readDataFile("{}.txt".format(PRODUCT_NAME)) is None:
        return

    logger.info("{} setup handler [BEGIN]".format(PRODUCT_NAME.upper()))
    portal = context.getSite()

    # Setup folders
    add_setup_folders(portal)

    # Configure visible navigation items
    setup_navigation_types(portal)

    # Setup workflows
    setup_workflows(portal)

    logger.info("{} setup handler [DONE]".format(PRODUCT_NAME.upper()))


def add_setup_folders(portal):
    """Adds the initial folders in setup
    """
    logger.info("Adding setup folders ...")

    setup = api.get_setup()
    pt = api.get_tool("portal_types")
    ti = pt.getTypeInfo(setup)

    # Disable content type filtering
    ti.filter_content_types = False

    for folder_id, folder_name, portal_type in SETUP_FOLDERS:
        if setup.get(folder_id) is None:
            logger.info("Adding folder: {}".format(folder_id))
            setup.invokeFactory(portal_type, folder_id, title=folder_name)

    # Enable content type filtering
    ti.filter_content_types = True

    logger.info("Adding setup folders [DONE]")


def setup_navigation_types(portal):
    """Add additional types for navigation
    """
    logger.info("Setup navigation types ...")
    registry = getUtility(IRegistry)
    key = "plone.displayed_types"
    display_types = registry.get(key, ())

    new_display_types = set(display_types)
    to_display = map(lambda f: f[2], SETUP_FOLDERS)
    new_display_types.update(to_display)
    registry[key] = tuple(new_display_types)
    logger.info("Setup navigation types [DONE]")


def setup_workflows(portal):
    """Setup workflow changes (status, transitions, permissions, etc.)
    """
    logger.info("Setup workflows ...")
    for wf_id, settings in WORKFLOWS_TO_UPDATE.items():
        update_workflow(wf_id, **settings)
    logger.info("Setup workflows [DONE]")


def pre_install(portal_setup):
    """Runs before the first import step of the *default* profile
    This handler is registered as a *pre_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} pre-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} pre-install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_uninstall(portal_setup):
    """Runs after the last import step of the *uninstall* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} uninstall handler [BEGIN]".format(PRODUCT_NAME.upper()))

    # https://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py
    profile_id = "profile-{}:uninstall".format(PRODUCT_NAME)
    context = portal_setup._getImportContext(profile_id)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} uninstall handler [DONE]".format(PRODUCT_NAME.upper()))
