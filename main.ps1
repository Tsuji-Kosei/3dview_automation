cd "\Users\root\Desktop\3DVista RPA\3dvista_edit_code_new"

$Name = Read-Host "Project_Name"

python 3DVista_RPA.py $Name

python main.py --copy $Name

$cwd = Split-Path $MyInvocation.MyCommand.path
cd $cwd