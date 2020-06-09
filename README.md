---
title: Dypsloom Docu
author: Isabel Medina 
date: 03/05/2020
---
THIS IS A TRIAL MODULE PLEASE DONT USE


# mdSplit

Tool that divides the given -md file into a set of smaller md files. These are placed within a  directory tree that is created where the original .md file was located. Each of these folders are orderly listed with the sectons titled and its corresponding section of the md file is labeled with a title header.

Finally the big .md file is saved withing that new folder, and converted into a pdf.

the following command works - maybe this is the easiest way  

menneu mainmd.md  -o markdown-demo2.pdf

 for images maybe it is easier to add always  the full http path so it doest get mixed up, when the md files gets split 
or simply have a folder  i.e. "./content/documentation/images/.." where all stay there and can be allways referenced with a full path. 

 Issues to solve : 

  - watch to run the file everytime something gets changed
