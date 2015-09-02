from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import schemata
from dependencies import atapi
from dependencies.dependency import registerType
from dependencies.dependency import permissions
from dependencies.dependency import getToolByName
from lims.browser import BrowserView
from lims.browser.bika_listing import BikaListingView
from lims.config import PROJECTNAME
from lims import bikaMessageFactory as _
from lims.utils import t
from dependencies.dependency import IViewView
from lims.content.bikaschema import BikaFolderSchema
from lims.interfaces import ICalculations
from dependencies.dependency import IFolderContentsView
from dependencies.folder import ATFolder, ATFolderSchema
from dependencies.dependency import implements

class CalculationsView(BikaListingView):
    implements(IFolderContentsView, IViewView)
    def __init__(self, context, request):
        super(CalculationsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'Calculation',
                              'sort_on': 'sortable_title'}
        self.context_actions = {_('Add'):
                                {'url':'createObject?type_name=Calculation',
                                 'icon': '++resource++bika.lims.images/add.png'}}
        self.title = self.context.translate(_("Calculations"))
        self.icon = self.portal_url + "/++resource++bika.lims.images/calculation_big.png"
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Calculation'),
                      'index': 'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description',
                            'toggle': True},
            'Formula': {'title': _('Formula'),
                        'index': 'getFormula',
                        'toggle': True},
        }

        self.review_states = [
            {'id':'default',
             'title': _('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate'}, ],
             'columns': ['Title',
                         'Description',
                         'Formula']},
            {'id':'inactive',
             'title': _('Dormant'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate'}, ],
             'columns': ['Title',
                         'Description',
                         'Formula']},
            {'id':'all',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Description',
                         'Formula']},
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['Title'])
            items[x]['Description'] = obj.Description()
            items[x]['Formula'] = obj.getMinifiedFormula()

        return items

schema = ATFolderSchema.copy()
class Calculations(ATFolder):
    implements(ICalculations)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(Calculations, PROJECTNAME)
