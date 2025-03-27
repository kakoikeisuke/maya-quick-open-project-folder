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
    main_window = mel.eval('$gmw = $gMainWindow')
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')
    custom_menu = cmds.menu('ProjectFolder', parent=main_window, label='ProjectFolder', tearOff=True)
    cmds.menuItem(
        label='ここにフォルダ名',
        parent=custom_menu,
        command='ここにフォルダーを開くコード',
        image='アイコン',
        annotation='フォルダー名'
    )

def delete_ui():
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')

def test():
    print('これでどう？')