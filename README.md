# 3dvista Automation

this code allows to make 3dview automatically from several panorama images.

## Requrements

python3.6

### library

numpy
json

### usage
Run at command prompt

python3 main.py <options>
ex) python3 main.py sample --database --distance 2.0 --copy

### options
Required options
* name
    * please enter the name of project file without ".vtp"

Optional option
* --database
    * data with positonal relation between images (distance and angle) and information of additional images is output (database.js)
* --copy
    * output the copy file (the name is (project_name)_copy.vtp) to make backup

### directory structure

* at "project" folder, there is a 3dvista project file to edit

* at "Images" folder, there are the all images to make 3dview and coordinates.js (these are output from GUI APP)

### Explanation about code

* 3DVista_RPA allows to run 3dvista automaticaly and make project file with RPA

* Edit_script.py allows to edit the script.js in the priject file (this code add arrows and info on the project file)

* create_detabase.py allows to edit coordinate.js to make handling easier

* cal_dis_angle allows to calcurate the angle between images from the coordinates

* make_project.py is allows to do file handling (e.g. compress and decompress a zipped file)

* main.py is allowed to compile options

### structure of script.js
