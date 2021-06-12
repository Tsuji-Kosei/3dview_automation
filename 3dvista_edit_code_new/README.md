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
* --distance
    * 画像を撮影した位置同士の距離がこの値よりも小さければ、3dview上で移動可能になる。デフォルト値は1.0となっている。
* --copy
    * 編集前のプロジェクトファイルをバックアップとして残すために、プロジェクト名+_copyという名前のコピーが生成される。

### directory structure

* projectフォルダーに編集する3dvistaのプロジェクトファイルが入っている。

* first.jsはGUIアプリで生成されるデータで、画像名と撮影した画像の位置座標が格納されている。

