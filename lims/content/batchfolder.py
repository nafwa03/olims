from OLiMS.lims.utils import isActive
"""BatchFolder contains AR Batches.
"""
from OLiMS.dependencies.dependency import schemata
from OLiMS.dependencies.dependency import atapi
from OLiMS.dependencies.dependency import DisplayList
from OLiMS.dependencies.dependency import permissions
from OLiMS.dependencies.dependency import getToolByName
from OLiMS.lims.config import PROJECTNAME
from OLiMS.dependencies.dependency import ClassSecurityInfo
from OLiMS.lims.interfaces import IBatchFolder, IHaveNoBreadCrumbs
from OLiMS.dependencies.dependency import folder
from OLiMS.dependencies.dependency import implements
from OLiMS.lims import bikaMessageFactory as _
from OLiMS.lims.utils import t
import json

schema = folder.ATFolderSchema.copy()


class BatchFolder(folder.ATFolder):
    implements(IBatchFolder, IHaveNoBreadCrumbs)
    schema = schema
    displayContentsTab = False
    security = ClassSecurityInfo()

schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)

atapi.registerType(BatchFolder, PROJECTNAME)