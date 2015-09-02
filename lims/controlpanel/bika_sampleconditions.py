from dependencies.dependency import schemata
from dependencies import atapi
from dependencies.dependency import getToolByName
from lims.browser.bika_listing import BikaListingView
from lims.config import PROJECTNAME
from lims.interfaces import ISampleConditions
from dependencies.dependency import IViewView
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.permissions import ManageBika
from dependencies.dependency import IFolderContentsView
from dependencies.folder import ATFolder, ATFolderSchema
from dependencies.dependency import implements


class SampleConditionsView(BikaListingView):
    implements(IFolderContentsView, IViewView)

    def __init__(self, context, request):
        super(SampleConditionsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'SampleCondition',
                              'sort_on': 'sortable_title'}
        self.context_actions = {_('Add'): {
            'url': 'createObject?type_name=SampleCondition',
            'icon': '++resource++bika.lims.images/add.png'
        }}
        self.title = self.context.translate(_("Sample Conditions"))
        self.icon = self.portal_url + "/++resource++bika.lims.images/samplecondition_big.png"
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = False
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Sample Condition'),
                      'index': 'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description',
                            'toggle': True},
        }

        self.review_states = [
            {'id':'default',
             'title': _('All'),
             'contentFilter':{},
             'transitions':[{'id':'empty'}, ],
             'columns': ['Title', 'Description']},
        ]

    def folderitems(self):
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission(ManageBika, self.context):
            del self.review_states[0]['transitions']
            self.show_select_column = True
            self.review_states.append(
                {'id': 'active',
                 'title': _('Active'),
                 'contentFilter': {'inactive_state': 'active'},
                 'transitions': [{'id':'deactivate'}, ],
                 'columns': ['Title', 'Description']})
            self.review_states.append(
                {'id': 'inactive',
                 'title': _('Dormant'),
                 'contentFilter': {'inactive_state': 'inactive'},
                 'transitions': [{'id':'activate'}, ],
                 'columns': ['Title', 'Description']})

        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if 'obj' in items[x]:
                items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                     (items[x]['url'], items[x]['Title'])

        return items

schema = ATFolderSchema.copy()
class SampleConditions(ATFolder):
    implements(ISampleConditions)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)
atapi.registerType(SampleConditions, PROJECTNAME)
