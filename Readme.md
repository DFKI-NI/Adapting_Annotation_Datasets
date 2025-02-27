# Adapting Annotation Datasets - Waste Detection Across Models and Scales

## Description of the Software

The code presented in this repository is divided into two sections, separated into two folders.

1. Handling different spatial and spectral resolutions of image datasets while maintaining the placement of annotations. (Python)
2. Adapting annotation dataset categories. Use segment-based annotations to create other AI employable datasets. (R_Markdown)
3. Interacting with CVAT (Python)

## 1. Handling different spatial and spectral resolutions of image datasets while maintaining the placement of annotations. (Python)

First you use the [Harmonize Data Notebook](./Handling_Resolution_-_Maintaining_Annotation/Harmonize_Data_different_resolution_new.ipynb) to create your scaled annotation files. Then you can use the [Combine Data Notebook](./Handling_Resolution_-_Maintaining_Annotation/Combine_data_different_resolutions.ipynb) to combine all the single annotation files to one combined annotation file.

### [Harmonize Data](./Handling_Resolution_-_Maintaining_Annotation/Harmonize_Data_different_resolution_new.ipynb)

This Notebook contains two functions.

* `write_new_annotations(annotations: list, scale: float)`: Write annotation data to json format
* `get_filename(path: str):`: Get the base file name form a file path

The code generates a list of all paths to the JSON files located within a specified directory. For each JSON file, the code prints the file name and loads its content into a dictionary. The annotations and images from the COCO data set are then extracted and a list of image file names is generated. For each scale in a predefined list, new annotations are generated using a specific function, and the COCO data dictionary is updated. A new file name is generated based on the current time, the original file name, and the scale in question, with the objective of ensuring that the resulting name is compatible with the file system. Subsequently, the updated COCO data is written to a new JSON file, and a confirmation message is displayed.

### [Combine Data](./Handling_Resolution_-_Maintaining_Annotation/Combine_data_different_resolutions.ipynb)

This Notebook contains two functions:

* `get_filename(path: str):`: Get the base file name form a file path
* `merge_coco_json(json_files: list, output_file: str)`: Merge and write COCO annotation files

The code performs a loop through each annotation file. The file name is extracted without the extension. Subsequently, the corresponding scaled files are collated, and the original annotation file is appended to this list. A list of paths to COCO JSON files for merging is then prepared. An output file name is generated based on the current time and the original file name, ensuring that the name is compatible with the file system. The COCO JSON files are then merged and the resulting file is saved to the specified output path. The final step is to display a confirmation message indicating the location where the merged file is saved.

### Requirements

Checkout the [Requirement file](./Handling_Resolution_-_Maintaining_Annotation/requirements.txt) in this directory.
You can use it with the following command:

```bash
pip install -r requirements.txt
```

## 2. Adapting annotation dataset categories. Use segment-based annotations to create other AI employable datasets. (R_Markdown)

Please open the folder [R_Markdown](./Adapting_Categories_-_Translate_to_other_Datasets/) to see the example files and the R Markdown Script.
The Script is designed to work with annotation files based (Json COCO format) on multiple images.
The example file, as extracted in the folder with the script, demonstrates the compiling and execution in general, while providing explanation and visualizations of the performed steps and generated outputs.

### [Adapting_and_Translating_Annotation_Datasets.Rmd](./Adapting_Categories_-_Translate_to_other_Datasets/Adapting_and_Translating_Annotation_Datasets.Rmd)

### Dependencies

* R version 4.3.2: GPL (≥ 3)
* RStudio 2023.12.1: Posit End User License Agreement

R Packages

* rmarkdown: GPL-3
* dplyr: MIT
* knitr: GPL-2 | GPL-3
* rjson: GPL-2
* sf: GPL-2 | MIT
* stringr: MIT
* terra: GPL (≥ 3)

## 3. Interacting with CVAT (Python)

The goal was to upload several files to our on-site CVAT instance without having to do it manually. For our project, we had four people working there, so we have four slots in the scripts, but this number can vary depending on your needs.

We've got three different Python scripts. All of these scripts need to be set up with the same environment settings from the [.env file](./Dataupload_CVAT/.env). One just sends the image folders to your CVAT instance, one assigns tasks to your team members, and one assigns jobs to your team members.

The .env file contains:

* Username
* Password

### Upload images

With the python script [send_images_to_cvat.py](./Dataupload_CVAT/send_images_to_cvat.py) you can send images to your CVAT instance. The script expects the following parameters in the script:

* taskpreset: the name for your tasks
* images_folder: where your subfolders are for each task
* host: The ip and port of your CVAT instance
* Project_id: The Id of your Project
* slug: The shortname (slug) of your organization if the project exists in an organization

### Upload images + assign tasks

It's basically the same as in [Upload Images] (#upload-images), but now you can also assign your team members with their usernames and how many tasks you want to give them. The tasks are then automatically assigned while they are uploaded to CVAT.
The script can be found [here](./Dataupload_CVAT/send_images_and_assignees.py).

### Requirements for CVAT API

Checkout the [Requirement file](./Dataupload_CVAT/requirements.txt) in this directory.
You can use it with the following command:

```bash
pip install -r requirements.txt
```

## License

The example data and code in this repository is released under the BSD-3 license.

## Funding

Funded by the German Federal Ministry for the Environment, Nature Conservation, Nuclear Safety and Consumer Protection (BMUV) based on a resolution of the German Bundestag (Grant No. 67KI21014A).

## Authors/Maintainers

* Felix Becker (<felix.becker@dfki.de>) - Python Notebooks (Method 1)
* Robert Retting (<robert.rettig@dfki.de>) - R_Markdown Script (Method 2)
