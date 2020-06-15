# ProtonTransfer
######    _Developed By Kelton Bassingthwaite_


This is a command line tool that creates a novel proton indicator from a coordinate file (.xyz) to highlight proton movement in acid/base chemical reactions. It then appends the indicator to the data then creates a new coordinate file. This data is commonly used in complex organic chemistry and water wire studies.


## Getting Started

### Requirements:
* Python 3+
* numpy
* matplotlib

### Install

First, create and activate a virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

Then, install dependancies

```
pip install numpy matplotlib
pip install . -e
```

## Useage

The script reads in a `.xyz` file.
Appends the aproximate position of the loose proton to each step.
Then, if a graph is requested, plots the distance between the proton and (0, 0, 0).
Finaly, a new `.xyz` file is written with the modified steps.

### Arguments:
* -i file name
  * The path to and name of the data to be analyzed (without the .xyz extension)
* -g Boolean
  * Optional argument to display a graph of the Indicators distance from the origin

### Examples: 

    c:\...\data>python ProtonTransfer.py -i filename -g True
    c:\...\data>python ProtonTransfer.py -i filename
    

## Citations:
 
 * Formula to determine the position of Proton Indicator from:
    * Pezeshki, Soroosh, and Hai Lin. “Adaptive-Partitioning QM/MM for Molecular Dynamics Simulations: 4. Proton Hopping in Bulk Water.” https://pubs.acs.org/doi/abs/10.1021/ct501019y. 
    
 ## Other Readings
 
 ### Presentation by Talachutla & Bhat at CU Denver's 2020 RaCAS conferance
 > These two projects were developed separately.
   
   * [Poster](https://drive.google.com/file/d/1b_Ni4dAWEcMLm0aO7Q4cgcziREL8lSGV/view)
   * [Video](https://www.youtube.com/watch?v=pn2-7Wnq_X8&feature=youtu.be)
