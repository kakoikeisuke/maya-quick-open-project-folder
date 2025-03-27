import os
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class OpenFolderCmd(om.MPxCommand):
    kPluginCmdName = "openFolder"
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return OpenFolderCmd()

    def doIt(self, args):
        self.redoIt()

    def redoIt(self):
        test()

def initializePlugin(plugin):
    vendor = "Kakoi Keisuke"
    version = "1.1.0"
    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerCommand(
            OpenFolderCmd.kPluginCmdName, OpenFolderCmd.cmdCreator
        )
    except:
        cmds.error('コマンドの登録に失敗しました。')
    try:
        create_ui()
    except:
        cmds.error('メニューの作成に失敗しました。')

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(
            OpenFolderCmd.kPluginCmdName
        )
    except:
        cmds.error('コマンドの除去に失敗しました')
    try:
        delete_ui()
    except:
        cmds.error('メニューの削除に失敗しました。')

def create_ui():
    global job
    job = cmds.scriptJob(event=['workspaceChanged', update_ui()])

    project_info = get_project_info()

    main_window = mel.eval('$gmw = $gMainWindow')
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')

    project_name = os.path.basename(os.path.normpath(project_info[0]))

    custom_menu = cmds.menu('ProjectFolder', parent=main_window, label=project_name, tearOff=True)

    for i in range(len(project_info)-1):
        folder_name = os.path.basename(os.path.normpath(project_info[i+1]))
        cmds.menuItem(
            label=folder_name,
            parent=custom_menu,
            command='実行コマンド',
            image='アイコンパス',
            annotation=project_info[i+1] + ' を開きます。'
        )

def delete_ui():
    if cmds.scriptJob(exists=job):
        cmds.scriptJob(kill=job)
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')

def update_ui():
    delete_ui()
    create_ui()

def test():
    print('これでどう？')

def get_project_info():
    project_info = []
    project_path = cmds.workspace(query=True, rootDirectory=True)
    # project_name = os.path.basename(
    #     os.path.normpath(project_path)
    # )
    project_info.append(project_path)
    all_item = os.listdir(project_path)
    for i in range(len(all_item)):
        if os.path.isdir(project_path + all_item[i]):
            project_info.append(all_item[i])
    return project_info