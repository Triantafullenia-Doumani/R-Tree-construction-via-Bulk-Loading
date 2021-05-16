# R-Tree-construction-via-Bulk-Loading

This program calculates the MBRs of objects and then bulk
loading the tree after sorting the MBRs using a space fill curve
(space-filling curve), more specifically the z-order. These curves are functions,
which map a multidimensional vector to a number in the one-dimensional
space. Two spatially close objects are very likely to
correspond to nearby prices. 

Consequently, two MBRs that are close to space will most likely enter the same leaf of the tree.

Examples of input files are given. Coords.txt and offset.txt

The coords.txt contains point coordinates in the form (x, y). 
  
The offset.txt contains entries of the form (id), (startOffset), (endOffset) where id is the unique identifier of a polygon
object and start offset (respectively end offset) is the no. line in the coords.txt file
where the coordinates of the points that form the begin (respectively end)
each object.
  
command line : python3 R-Tree-construction-via-Bulk-Loading.py coords.txt offsets.txt
