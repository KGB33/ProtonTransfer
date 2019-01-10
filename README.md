# ProtonTransfer

This is a command line tool that creates a novel proton indicator from a coordinate file (.xyz) to highlight proton movement in acid/base chemical reactions. Appends the indicator to the data then creates a new coordinate file. Commonly used in complex organic chemistry and water wire studies.


## Arguments:
* -i file name
  * The name of the data to be analyzed
* -g Boolean
  * Optional argument to display a graph of the Indicators distance from the origin



## Examples: 

    c:\...\data>python ProtonTransfer.py -i filename -g True
    c:\...\data>python ProtonTransfer.py -i filename
    
    

## Requirements:
* Pip install coming soon!

Alternatively:
* Python 3+
* Numpy

 ## Citations:
 
 * Formula to determine position of Proton Indicator from:
    * Pezeshki, Soroosh, and Hai Lin. “Adaptive-Partitioning QM/MM for Molecular Dynamics Simulations: 4. Proton Hopping in Bulk Water.” https://pubs.acs.org/doi/abs/10.1021/ct501019y. 
