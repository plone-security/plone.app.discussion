# -*- coding: utf-8 -*-
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import logging


default_profile = 'profile-plone.app.discussion:default'
logger = logging.getLogger('plone.app.discussion')


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(IDiscussionSettings)


def update_rolemap(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')


def upgrade_comment_workflows(context):
    context.runImportStepFromProfile(default_profile, 'workflow')
    catalog = getToolByName(context, 'portal_catalog')
    for brain in catalog(portal_type='Discussion Item'):
        try:
            comment = brain.getObject()
            comment.reindexObjectSecurity()
        except (AttributeError, KeyError):
            logger.info('Could not reindex comment %s' % brain.getURL())
