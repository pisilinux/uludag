#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import copy

from qt import *
from kdeui import *
from kdecore import *

from utility import *
from dialogs import *
from search import *
import domain
import ldapmodel

import ldap


class Browser(KListView):
    """Domain browser"""
    
    def __init__(self, parent, window):
        KListView.__init__(self, parent)
        self.addColumn("")
        self.header().hide()
        self.setRootIsDecorated(True)
        self.window = window
        
        self.menu_blank = QPopupMenu(self)
        self.menu_blank.insertItem(getIconSet("filenew", KIcon.Small), i18n("&New Domain"), self.slotNewDomain)
        
        self.menu_domain = QPopupMenu(self)
        self.menu_domain.insertItem(getIconSet("folder", KIcon.Small), i18n("&New Directory"), self.slotNewDirectory)
        self.menu_domain.insertSeparator()
        self.menu_domain.insertItem(getIconSet("remove", KIcon.Small), i18n("&Remove"), self.slotRemove)
        self.menu_domain.insertSeparator()
        self.menu_domain.insertItem(getIconSet("configure", KIcon.Small), i18n("&Configure"), self.slotConfigure)
        
        self.menu_domain.insertSeparator()
        self.menu_domain.insertItem(getIconSet("search", KIcon.Small), i18n("&Search"), self.slotSearch)
        
        self.menu_directory = QPopupMenu(self)
        self.menu_directory.insertItem(getIconSet("folder", KIcon.Small), i18n("&New Directory"), self.slotNewDirectory)
        self.menu_directory.insertSeparator()
        self.menu_directory.insertItem(getIconSet("remove", KIcon.Small), i18n("&Remove"), self.slotRemoveDirectory)
        self.menu_directory.insertSeparator()
        self.menu_directory.insertItem(getIconSet("reload", KIcon.Small), i18n("&Refresh"), self.slotRefresh)
        self.menu_directory.insertSeparator()
        self.menu_directory.insertItem(getIconSet("configure", KIcon.Small), i18n("&Properties"), self.slotDirectoryProperties)
        
        self.connect(self, SIGNAL("contextMenuRequested(QListViewItem*, const QPoint &, int)"), self.slotPopup)
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.slotExpand)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.slotCollapse)
        self.connect(self, SIGNAL("selectionChanged()"), self.slotNodeChanged)
        
        self.tipper = BrowserItemTip(self.viewport())
        self.tipper.list = self
        
        self.initDomains()
    
    def initDomains(self):
        dc = self.window.dc
        for connection in dc.connections:
            label = connection.label
            dn = connection.base_dn
            BrowserItem(self, self.window, dn, None, connection)
    
    def slotPopup(self, item, point, button):
        if item:
            if isinstance(item.parent(), BrowserItem):
                self.menu_directory.exec_loop(point)
            else:
                self.menu_domain.exec_loop(point)
        else:
            self.menu_blank.exec_loop(point)
    
    def slotConfigure(self):
        item = self.selectedItem()
        dd = DomainDialog(self, item.connection)
        if dd.exec_loop():
            try:
                item.reloadObject()
            except ldap.LDAPError:
                item.disableDomain()
            if item.connection.isModified():
                dc = self.window.dc
    
    def slotDirectoryProperties(self):
        item = self.selectedItem()
        connection = item.connection
        model_old = item.model.toEntry()
        od = ObjectDialog(self.window, item.dn, item.model)
        if od.exec_loop():
            model_new = od.model
            try:
                connection.modify(od.dn, model_old, model_new.toEntry())
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                item.parent().collapseNodes()
                item.parent().expandNodes()
    
    def slotSearch(self):
        item = self.selectedItem()
        if item:
            od = SearchDialog(self, item.connection, item.dn)
            od.exec_loop()
    
    def slotNewDomain(self):
        dd = DomainDialog(self)
        if dd.exec_loop():
            try:
                dd.connection.bind()
            except ldap.LDAPError:
                self.window.showCriticalError(i18n("Unable to connect to LDAP server."))
                return
            dn = dd.connection.base_dn
            self.window.dc.addConnection(dd.connection)
            BrowserItem(self, self.window, dn, None, dd.connection)
        elif not len(self.window.dc.connections):
            self.window.showInfo(i18n("You can add new domain by right clicking panel on left."))
    
    def slotNewDirectory(self):
        item = self.selectedItem()
        connection = item.connection
        od = ObjectDialog(self.window, item.dn, ldapmodel.DirectoryModel(connection=connection))
        if od.exec_loop():
            try:
                connection.add(od.dn, od.model.toEntry())
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                if item.isOpen():
                    item.collapseNodes()
                item.expandNodes()
    
    def slotRemoveDirectory(self):
        item = self.selectedItem()
        confirm = self.window.doubleConfirm(i18n("Remove directory?"), i18n("Are you sure you want to remove '%1' ?").arg(item.text(0)), i18n("This is not undoable. Are you sure you want to continue?"))
        if confirm:
            try:
                item.connection.delete(item.dn)
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                item.parent().collapseNodes()
                item.parent().expandNodes()
    
    def slotRemove(self):
        item = self.selectedItem()
        confirm = self.window.confirm(i18n("Remove domain?"), i18n("Are you sure you want to remove '%1' ?").arg(item.text(0)))
        if confirm:
            item.disableDomain()
            dc = self.window.dc
            dc.removeConnection(item.connection)
            self.takeItem(item)
    
    def slotRefresh(self):
        self.showObjects()
    
    def slotExpand(self, item):
        item.expandNodes()
    
    def slotCollapse(self, item):
        item.collapseNodes()
    
    def slotNodeChanged(self):
        self.showObjects()
    
    def showObjects(self):
        object_len = 0
        show_tab = None
        
        objects = [
            (self.window.computers, "pardusComputer", ldapmodel.ComputerModel, ldapmodel.ComputerPolicyModel, ldapmodel.ComputerInfoModel, "krdc", i18n("Computers (%1)")),
            (self.window.units, "organizationalUnit", ldapmodel.UnitModel, ldapmodel.UnitPolicyModel, None, "server", i18n("Units (%1)")),
            (self.window.users, "posixAccount", ldapmodel.UserModel, None, None, "user", i18n("Users (%1)")),
            (self.window.groups, "posixGroup", ldapmodel.GroupModel, None, None, "kontact_contacts", i18n("Groups (%1)")),
        ]
        
        for objectWidget, objectClass, objectModel, objectPolicy, objectInfo, icon, label in objects:
            objectWidget.clear()
            item = self.selectedItem()
            if item and isinstance(item.parent(), BrowserItem):
                try:
                    fields = [objectModel.name_field]
                    result = item.connection.search(item.dn, ldap.SCOPE_ONELEVEL, "objectClass=%s" % objectClass, fields)
                except ldap.LDAPError, e:
                    if e.__class__ in domain.LDAPCritical:
                        self.disableDomain()
                    else:
                        self.window.showError(e.args[0]["info"])
                else:
                    for dn, attrs in result:
                        model = objectModel(attrs, item.connection)
                        policy = None
                        if objectPolicy:
                            policy = objectPolicy(attrs, item.connection)
                        info = None
                        if objectInfo:
                            info = objectInfo(attrs, item.connection)
                        ObjectListItem(objectWidget, self.window, dn, model, policy, info, icon)
                    self.window.tab.setTabLabel(objectWidget, label.arg(len(result)))
                if len(result) > object_len:
                    show_tab = objectWidget
                    object_len = len(result)
        
        self.window.tab.showPage(show_tab)


class BrowserItemTip(QToolTip):
    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item and not isinstance(item.parent(), BrowserItem):
            rect = self.list.itemRect(item)
            args = [
                item.connection.label,
                item.connection.host,
            ]
            self.tip(self.list.itemRect(item), i18n("<strong>%1</strong><br>Host: %2").arg(*args))


class BrowserItem(QListViewItem):
    """Domain tree element.
       Requires a parent node object, window object and DN for the node.
       Non-root nodes require a label, root nodes require a connection object."""
    
    def __init__(self, parent, window, dn, model, connection=None):
        self.window = window
        self.dn = dn
        self.model = model
        if connection:
            self.connection = connection
        else:
            self.connection = parent.connection
        self.label = ""
        if self.model:
            self.label = unicode(model.fields["label"])
        QListViewItem.__init__(self, parent, self.label)
        self.setExpandable(True)
        self.initObject()
    
    def initObject(self):
        """Initialize domain object. Gets label from domain server, if it's a root node."""
        if isinstance(self.parent(), BrowserItem):
            self.setState("node_close")
        else:
            try:
                self.connection.bind()
            except ldap.LDAPError, e:
                self.disableDomain()
                return
            try:
                results = self.connection.search(self.dn, ldap.SCOPE_BASE, "objectClass=organization")
                dn, attrs = results[0]
                label = unicode(attrs["o"][0])
                self.setText(0, label)
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    self.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                self.setState("active")
    
    def reloadObject(self):
        """Reset connection and initialize domain object again."""
        self.connection.unbind()
        self.connection.bind()
        self.initObject()
    
    def getRootNode(self):
        """Find root node."""
        item = self
        while True:
            if not isinstance(item.parent(), BrowserItem):
                return item
            item = item.parent()
    
    def disableDomain(self):
        """Disable domain tree. Used when connection errors occur."""
        self.connection.unbind()
        root = self.getRootNode()
        root.setState("error")
        root.clearNodes()
        root.setOpen(False)
    
    def setState(self, state):
        """Set state of a node. (root: [active, error], others: [node_open, node_close]"""
        self.state = state
        if state == "active":
            self.setPixmap(0, getIcon("connect_established.png", KIcon.Small))
        #elif state == "passive":
        #    self.setPixmap(0, getIcon("connect_creating.png", KIcon.Small))
        elif state == "error":
            self.setPixmap(0, getIcon("connect_no.png", KIcon.Small))
        elif state == "node_open":
            self.setPixmap(0, getIcon("folder_open.png", KIcon.Small))
        elif state == "node_close":
            self.setPixmap(0, getIcon("folder.png", KIcon.Small))
    
    def getChildren(self):
        """Give sub-organizations. Returns False on error"""
        try:
            return self.connection.search(self.dn, ldap.SCOPE_ONELEVEL, "objectClass=organization")
        except ldap.LDAPError, e:
            desc = e.args[0]["info"]
            if not self.firstChild():
                self.setOpen(False)
            if e.__class__ in domain.LDAPCritical:
                self.disableDomain()
            else:
                self.window.showError(e.args[0]["info"])
            return False
    
    def expandNodes(self):
        if isinstance(self.parent(), BrowserItem):
            self.setState("node_open")
            self.setOpen(True)
        else:
            try:
                self.reloadObject()
            except ldap.LDAPError, e:
                if not self.firstChild():
                    self.setOpen(False)
                if e.__class__ in domain.LDAPCritical:
                    self.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
                return
        
        organizations = self.getChildren()
        if organizations == False:
            if not self.firstChild():
                self.setOpen(False)
        else:
            self.clearNodes()
            for organization in organizations:
                dn, attrs = organization
                model = ldapmodel.DirectoryModel(attrs, self.connection)
                BrowserItem(self, self.window, dn, model)
            
            if not len(organizations):
                self.setOpen(False)
    
    def clearNodes(self):
        kid = self.firstChild()
        while kid:
            tmp = kid.nextSibling()
            self.takeItem(kid)
            kid = tmp
    
    def collapseNodes(self):
        if isinstance(self.parent(), BrowserItem):
            self.setState("node_close")


class ObjectList(KListView):
    def __init__(self, parent, window, object_type):
        KListView.__init__(self, parent)
        self.addColumn(i18n("Name"))
        self.addColumn(i18n("Description"))
        #self.header().hide()
        self.setResizeMode(KListView.LastColumn)
        self.setRootIsDecorated(False)
        self.setSelectionMode(QListView.Extended)
        self.window = window
        self.type = object_type
        
        self.menu_item = QPopupMenu(self)
        self.id_menu = [
            self.menu_item.insertItem(getIconSet("filenew", KIcon.Small), i18n("&New"), self.slotNewItem),
            self.menu_item.insertSeparator(),
            self.menu_item.insertItem(getIconSet("remove", KIcon.Small), i18n("&Remove"), self.slotRemove),
            self.menu_item.insertSeparator(),
            self.menu_item.insertItem(getIconSet("info", KIcon.Small), i18n("&Information"), self.slotInfo),
            self.menu_item.insertItem(getIconSet("services", KIcon.Small), i18n("&Policy"), self.slotPolicy),
            self.menu_item.insertItem(getIconSet("configure", KIcon.Small), i18n("&Configuration"), self.slotProperties),
        ]
        
        self.connect(self, SIGNAL("contextMenuRequested(QListViewItem*, const QPoint&, int)"), self.slotPopup)
    
    def slotPopup(self, item, point, col):
        browser = self.window.browser
        selected = browser.selectedItem()
        if not selected or not isinstance(selected.parent(), BrowserItem):
            return
        for i in self.id_menu:
            self.menu_item.setItemVisible(i, True)
        items = self.selectedItems()
        if len(items):
            """
            if len(items) > 1:
                for i in self.id_menu[3:]:
                    self.menu_item.setItemVisible(i, False)
            """
            if not items[0].info:
                self.menu_item.setItemVisible(self.id_menu[4], False)
            if not items[0].policy:
                self.menu_item.setItemVisible(self.id_menu[5], False)
        else:
            for i in self.id_menu[1:]:
                self.menu_item.setItemVisible(i, False)
        self.menu_item.exec_loop(point)
    
    def slotNewItem(self):
        browser = self.window.browser
        item = browser.selectedItem()
        connection = item.connection
        dn = item.dn
        if self.type == "computer":
            model = ldapmodel.ComputerModel(connection=connection)
        elif self.type == "unit":
            model = ldapmodel.UnitModel(connection=connection)
        elif self.type == "user":
            model = ldapmodel.UserModel(connection=connection)
        elif self.type == "group":
            model = ldapmodel.GroupModel(connection=connection)
        od = ObjectDialog(self.window, dn, model)
        if od.exec_loop():
            try:
                connection.add(od.dn, od.model.toEntry())
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                browser.showObjects()
    
    def getObjectDetails(self, dn):
        browser = self.window.browser
        connection = browser.selectedItem().connection
        return connection.search(dn, ldap.SCOPE_BASE)[0][1]
    
    def slotProperties(self):
        browser = self.window.browser
        connection = browser.selectedItem().connection
        items = self.selectedItems()
        for item in items:
            attrs = self.getObjectDetails(item.dn)
            if item.model:
                item.model = item.model.__class__(attrs)
        item = items[0]
        if len(items) > 1:
            multiple = True
            od = ObjectDialog(self.window, item.dn, item.model.__class__(), multiple=True)
        else:
            multiple = False
            model_old = copy.deepcopy(item.model)
            od = ObjectDialog(self.window, item.dn, item.model)
        if od.exec_loop():
            model_new = od.model
            try:
                # Modify attributes
                if multiple:
                    fields = model_new.fields.keys()
                    if not fields:
                        return
                    for item in items:
                        connection.modify(item.dn, item.model.toEntry(multiple=True, only_fields=fields), model_new.toEntry(multiple=True))
                else:
                    connection.modify(od.dn, model_old.toEntry(), model_new.toEntry())
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                browser.showObjects()
    
    def slotPolicy(self):
        browser = self.window.browser
        connection = browser.selectedItem().connection
        items = self.selectedItems()
        for item in items:
            attrs = self.getObjectDetails(item.dn)
            if item.policy:
                item.policy = item.policy.__class__(attrs)
        item = items[0]
        if not item.policy:
            return
        if len(items) > 1:
            multiple = True
            od = ObjectDialog(self.window, item.dn, item.policy.__class__(), multiple=True, unset=True)
        else:
            multiple = False
            model_old = copy.deepcopy(item.policy)
            od = ObjectDialog(self.window, item.dn, item.policy, unset=True)
        if od.exec_loop():
            model_new = od.model
            try:
                if multiple:
                    fields = model_new.fields.keys()
                    if not fields:
                        return
                    for item in items:
                        connection.modify(item.dn, item.policy.toEntry(multiple=True, only_fields=fields), model_new.toEntry(multiple=True))
                else:
                    connection.modify(od.dn, model_old.toEntry(), model_new.toEntry())
            except ldap.LDAPError, e:
                if e.__class__ in domain.LDAPCritical:
                    item.disableDomain()
                else:
                    self.window.showError(e.args[0]["info"])
            else:
                browser.showObjects()
    
    def slotInfo(self):
        browser = self.window.browser
        connection = browser.selectedItem().connection
        items = self.selectedItems()
        for item in items:
            attrs = self.getObjectDetails(item.dn)
            if item.info:
                item.info = item.info.__class__(attrs)
        item = items[0]
        if not item.info:
            return
        if len(items) > 1:
            pass
        else:
            od = ObjectDialog(self.window, item.dn, item.info, infowin=True)
            od.exec_loop()
    
    def slotRemove(self):
        browser = self.window.browser
        items = self.selectedItems()
        if len(items) == 1:
            label = items[0].text(0)
            confirm = self.window.doubleConfirm(i18n("Remove object?"), i18n("Are you sure you want to remove '%1' ?").arg(label), i18n("This is not undoable. Are you sure you want to continue?"))
        elif len(items) < 10:
            labels = [" - %s" % item.text(0) for item in items]
            labels = "\n".join(labels)
            confirm = self.window.doubleConfirm(i18n("Remove objects?"), i18n("Are you sure you want to remove these objects?\n%1").arg(labels), i18n("This is not undoable. Are you sure you want to continue?"))
        else:
            count = len(items)
            confirm = self.window.doubleConfirm(i18n("Remove objects?"), i18n("Are you sure you want to remove %1 objects?").arg(count), i18n("This is not undoable. Are you sure you want to continue?"))
        if confirm:
            connection = browser.selectedItem().connection
            failed = []
            for item in items:
                try:
                    connection.delete(item.dn)
                except ldap.LDAPError, e:
                    if e.__class__ in domain.LDAPCritical:
                        item.disableDomain()
                        return
                    else:
                        failed.append((item, e.args[0]["info"]))
            if len(failed):
                failed = [" - %s (%s)" % (item.label, message) for item, message in failed]
                failed = "\n".join(failed)
                self.window.showWarning(i18n("Unable to delete these objects:\n%1").arg(failed))
            else:
                count = len(items)
                self.window.showInfo(i18n("Removed %1 objects.").arg(count))
                browser.showObjects()


class ObjectListItem(KListViewItem):
    def __init__(self, parent, window, dn, model, policy, info, icon):
        self.window = window
        self.dn = dn
        self.model = model
        self.policy = policy
        self.info = info
        if model.fields.get("label", ""):
            label = unicode(model.fields["label"])
        else:
            label = model.name
        if model.fields.get("description", ""):
            description = unicode(model.fields["description"])
        else:
            description = ""
        KListViewItem.__init__(self, parent, label)
        self.setPixmap(0, getIcon(icon, KIcon.Small))
        self.setText(0, label)
        self.setText(1, description)
