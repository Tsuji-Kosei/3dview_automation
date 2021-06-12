# 3dvista Automation

複数枚の写真の座標情報から、3dviewを自動で作成するプログラムです

## Requrements

python3.6

### library

numpy
json

### usage

コードから実行
python3 main.py <options>
ex) python3 main.py sample --database --distance 2.0 --copy

### options
必須オプション
* name
    * .vtpを抜いたプロジェクトファイル名を入力する

任意オプション
* --database
    * 画像と画像の位置関係(距離と角度)のデータが出力される(database.js)
* --copy
    * 編集前のプロジェクトファイルをバックアップとして残すために、プロジェクト名+_copyという名前のコピーが生成される。

### directory structure

* projectフォルダーに編集する3dvistaのプロジェクトファイルが入っている。

* first.jsはGUIアプリで生成されるデータで、画像名と撮影した画像の位置座標が格納されている。

### Explanation about code

* 3DVista_RPAは3dvistaを自動的に起動し、RPAで操作をするためのコード

* Edit_script.pyは3DVistaで生成したプロジェクトファイルの中のscript.jsを編集するコード

* create_detabase.pyは、GUIアプリから得たjsonファイルをEdit_script.pyのコードに対応するように変種するためのコード

* cal_dis_angleは座標情報から、繋がっている写真の方角を計算するためのコード

* make_project.pyは、3DVista_RPAで生成したプロジェクトファイルを、矢印やinformationがついたプロジェクトファイルに変換するためのコード。(zipの解答やファイル操作を主に行っている)

* main.pyは、オプションがまとめられている。

### structure of script.js
