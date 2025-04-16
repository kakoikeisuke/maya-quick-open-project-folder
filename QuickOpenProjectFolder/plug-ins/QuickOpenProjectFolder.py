import os
import platform
import subprocess
import json
from pathlib import Path

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
            os_name = message[language]["unknown_os"]
        print(message[language]["detected_os"] + os_name)

        project_info = get_project_info()
        print(message[language]["current_project"] + project_info[0])
        all_folder_name = ''
        for i in range(len(project_info) - 1):
            if i == len(project_info) - 2:
                all_folder_name += project_info[i + 1]
            else:
                all_folder_name += project_info[i + 1] + ', '
        print(message[language]["folders_in_project"] + all_folder_name)

def initializePlugin(plugin):
    vendor = "Kakoi Keisuke"
    version = "1.2.0"
    pluginFn = om.MFnPlugin(plugin, vendor, version)
    get_message()

    try:
        pluginFn.registerCommand(
            OpenFolderCmd.kPluginCmdName, OpenFolderCmd.cmdCreator
        )
    except:
        cmds.error(message[language]["command_registration_failure"])
    try:
        create_ui()
    except:
        cmds.error(message[language]["menu_creation_failure"])

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(
            OpenFolderCmd.kPluginCmdName
        )
    except:
        cmds.error(message[language]["command_deregister_failure"])
    try:
        delete_ui()
    except:
        cmds.error(message[language]["menu_deletion_failure"])

def get_message():
    global language
    language = cmds.about(uiLanguage=True)
    if language == 'ja_JP':
        pass
    else:
        language = 'en_US'
    module_path = Path(cmds.getModulePath(moduleName='QuickOpenProjectFolder'))
    message_json_path = module_path / 'i18n' / 'message.json'
    json_open = open(message_json_path, 'r', encoding='utf-8')
    global message
    message = json.load(json_open)

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
        annotation=message[language]["root_folder_annotation"]
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
                annotation=message[language]["folder_annotation"]
            )
        else:
            cmds.menuItem(
                label=folder_name,
                parent=custom_menu,
                command=lambda x, idx=path_index: open_folder(full_path_list[idx]),
                image='QuickOpenProjectFolder_child.svg',
                annotation=message[language]["folder_annotation"]
            )
    cmds.menuItem(
        label=message[language]["reload_menu"],
        parent=custom_menu,
        command=lambda x: update_ui(),
        image='QuickOpenProjectFolder_reload.svg',
        annotation=message[language]["reload_annotation"]
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
    path = os.path.normpath(path)
    if not os.path.exists(path):
        cmds.error(message[language]["folder_not_exists"])
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['explorer', path])
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        elif platform.system() == 'Linux':
            subprocess.Popen(['xdg-open', path])
        else:
            cmds.error(message[language]["open_folder_failure"])
    except:
        cmds.error(message[language]["open_folder_failure"])