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
# Copyright 2022-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from senaite.core.api import workflow as wapi
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import UpgradeUtils
from senaite.core.workflow import SAMPLE_WORKFLOW
from senaite.diagnosis import logger
from senaite.diagnosis import PRODUCT_NAME
from senaite.diagnosis.setuphandlers import setup_workflows

version = "1200"
profile = "profile-{0}:default".format(PRODUCT_NAME)


@upgradestep(PRODUCT_NAME, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(PRODUCT_NAME)

    if ut.isOlderVersion(PRODUCT_NAME, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            PRODUCT_NAME, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(PRODUCT_NAME, ver_from,
                                                   version))

    # -------- ADD YOUR STUFF BELOW --------

    logger.info("{0} upgraded to version {1}".format(PRODUCT_NAME, version))
    return True


def setup_permissions(tool):
    """Setup permissions
    """
    logger.info("Setup permissions ...")

    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup

    # import rolemap
    setup.runImportStepFromProfile(profile, "rolemap")

    # update sample workflow
    setup_workflows(portal)

    # update sample role mappings
    wf = wapi.get_workflow(SAMPLE_WORKFLOW)
    query = {"portal_type": "AnalysisRequest"}
    brains = api.search(query, SAMPLE_CATALOG)
    total = len(brains)
    for num, brain in enumerate(brains):
        if num and num % 100 == 0:
            logger.info("Processed objects: {}/{}".format(num, total))

        obj = api.get_object(brain)
        wf.updateRoleMappingsFor(obj)

        # Flush the object from memory
        obj._p_deactivate()

    logger.info("Setup permissions [DONE]")
