import os
import platform
import subprocess

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class OpenFolderCmd(om.MPxCommand):
    kPluginCmdName = "quickOpenProjectFolder"
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return OpenFolderCmd()

    def doIt(self, args):
        self.redoIt()

    def redoIt(self):
        update_ui()

        if platform.system() == 'Windows':
            os_name = 'Windows'
        elif platform.system() == 'Darwin':
            os_name = 'macOS'
        elif platform.system() == 'Linux':
            os_name = 'Linux'
        else:
            os_name = '不明（非対応）'
        print('認識したOS: ' + os_name)

        project_info = get_project_info()
        print('現在のプロジェクト: ' + project_info[0])
        all_folder_name = ''
        for i in range(len(project_info) - 1):
            if i == len(project_info) - 2:
                all_folder_name += project_info[i + 1]
            else:
                all_folder_name += project_info[i + 1] + ', '
        print('プロジェクト内のフォルダ: ' + all_folder_name)

def initializePlugin(plugin):
    vendor = "Kakoi Keisuke"
    version = "1.0.0"
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

    job = cmds.scriptJob(event=['workspaceChanged', update_ui])
    update_ui()

def delete_ui():
    if job is not None and cmds.scriptJob(exists=job):
        cmds.scriptJob(kill=job)
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')

def update_ui():
    project_info = get_project_info()
    full_path_list = get_full_path_list(project_info)
    main_window = mel.eval('$gmw = $gMainWindow')
    if cmds.menu('ProjectFolder', exists=True):
        cmds.deleteUI('ProjectFolder')

    project_name = os.path.basename(os.path.normpath(project_info[0]))

    custom_menu = cmds.menu(
        'ProjectFolder',
        parent=main_window,
        label='▶' + project_name,
        tearOff=True
    )

    cmds.menuItem(
        label=project_name,
        parent=custom_menu,
        command=lambda x: open_folder(full_path_list[0]),
        image='QuickOpenProjectFolder_root.svg',
        annotation='プロジェクトのルートフォルダ ( ' + project_name + ' ) を開きます。'
    )
    for i in range(len(project_info) - 1):
        folder_name = os.path.basename(os.path.normpath(project_info[i + 1]))
        path_index = i + 1
        if i == len(project_info) - 2:
            cmds.menuItem(
                label=folder_name,
                parent=custom_menu,
                command=lambda x, idx=path_index: open_folder(full_path_list[idx]),
                image='QuickOpenProjectFolder_child_bottom.svg',
                annotation='フォルダ ' + project_info[i + 1] + ' を開きます。'
            )
        else:
            cmds.menuItem(
                label=folder_name,
                parent=custom_menu,
                command=lambda x, idx=path_index: open_folder(full_path_list[idx]),
                image='QuickOpenProjectFolder_child.svg',
                annotation='フォルダ ' + project_info[i + 1] + ' を開きます。'
            )
    cmds.menuItem(
        label='再読み込み',
        parent=custom_menu,
        command=lambda x: update_ui(),
        image='QuickOpenProjectFolder_reload.svg',
        annotation='プロジェクトフォルダ直下のフォルダを再検索し, リストを更新します。'
    )

def get_project_info():
    project_info = []
    project_path = cmds.workspace(query=True, rootDirectory=True)
    project_info.append(project_path)
    all_item = os.listdir(project_path)
    for i in range(len(all_item)):
        if os.path.isdir(project_path + all_item[i]):
            project_info.append(all_item[i])
    return project_info

def get_full_path_list(project_info):
    full_path_list = []
    for i in range(len(project_info)):
        if i == 0:
            full_path = project_info[i]
        else:
            full_path = os.path.join(project_info[0], project_info[i])
        full_path_list.append(full_path)
    return full_path_list

def open_folder(path):
    try:
        path = os.path.normpath(path)
        if platform.system() == 'Windows':
            subprocess.Popen(['explorer', path])
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        elif platform.system() == 'Linux':
            subprocess.Popen(['xdg-open', path])
        else:
            cmds.error('フォルダを開けませんでした。対応していないOSです。')
    except:
        cmds.error('フォルダを開く際にエラーが発生しました。')