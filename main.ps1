$path = Convert-Path .
$Name = Read-Host "Project_Name"
cd ".\3dvista_edit_code_new"

python extract_gui_data.py

python 3DVista_RPA.py $Name

python main.py --database $Name

python Preview.py $Name

cd $path