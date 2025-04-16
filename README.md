# Quick Open Project Folder
プロジェクトフォルダーに素早くアクセスできるメニューを追加するMayaプラグインモジュールです。  

![](/README_resource/screenshot.png)
## インストール
`QuickOpenProjectFolder.mod`ファイルと`QuickOpenProjectFolder`フォルダが`zip`ファイルに圧縮されています。  
`MAYA_MODULE_PATH`に登録された同一ディレクトリ内に`QuickOpenProjectFolder.mod`ファイルと`QuickOpenProjectFolder`フォルダを配置することで, Mayaプラグインモジュールとして認識できるようになります。  
この状態でMaya内のプラグインマネージャからロードすることが可能です。
## 使用方法
このプラグインがロードされると, Mayaのメニューに`▶プロジェクト名`の項目が追加されます。  

プロジェクトフォルダが  
```
C:\Users\username\Documents\maya\projects\sampleProject
```
の場合, `▶sampleProject`という項目が追加されます。  

この項目を選択すると, プロジェクトフォルダ直下にあるフォルダのリストが表示されます。  
フォルダ名をクリックすると, そのフォルダが開かれます。
## 挙動
### フォルダリストの更新タイミング
メニューの項目名, メニュー内のフォルダリストは以下のタイミングで更新されます。
- プラグインがロードされたとき
- プロジェクトフォルダが変更されたとき
- コマンド (`quickOpenProjectFolder`) で呼び出されたとき
- メニューアイテムから「再読み込み」が実行されたとき  
### 言語
Mayaの言語設定に応じて, 注釈などの言語が変更されます。  
Maya本体が`ja_JP`の場合は日本語, それ以外の場合 (`en_US`, `zh_CN`) は英語となります。
## 動作確認環境
Windows 11 Pro 24H2  
Autodesk Maya 2025.3 (Python 3.11.4) (ja_JP, en_US)  
Autodesk Maya 2026 (Python 3.11.9) (ja_JP, en_US)