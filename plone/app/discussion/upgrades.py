from Products.CMFCore.utils import getToolByName
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


default_profile = 'profile-plone.app.discussion:default'


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(IDiscussionSettings)


def update_rolemap(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')


def upgrade_comment_workflows(context):
    context.runImportStepFromProfile(default_profile, 'workflow')
    catalog = getToolByName(context, 'portal_catalog')
    for brain in catalog(portal_type='Discussion Item'):
        comment = brain.getObject()
        comment.reindexObjectSecurity()