# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:41:27 2020

@author: isabe
"""

"""
Created on Tue May 19 10:12:38 2020

@author: isabel Medina

It takes a give .md files and splits it by sections (up to 3 levels), and splits it 
up into separate files into the specific folder qith the sections name

Further work: 
    - save a full version of the big md file in the folder with updated info?
    - date in smaller md files?
    - create a contents table in the big md file
     

AS a function: 
    
    - pathIn is the path of the file to be split up,  it unpacks itself in its parent folder 
    further work : (++kwargs)
        - give a possible path out 
        - give the possibility to change the name of the split up md smaller files.

"""
### IMPORTS
import os
import re
import numpy as np
import sys

#def md_split(pathIn):
def main (pathIn, pathOut):
    '''
    returns the folder where the files have been split up
    '''
    ### INITIAL DEFINITIONS
    mdFileName= 'index.md'

    ### FUNCTIONS
    def createPath(path):
        ''' 
        checks if the files exists and if not it creates is 
        '''
        if os.path.exists(path) == False:
            os.makedirs(path)
        else:
            try:
                # if the admin permissions do not exist it doesnt allow you to delete the files...
                os.remove('Filename')
                os.mkdir(path)
            except OSError:
                if path != '':
                    print ('ERROR: Cannot delete file. Make sure your have enough credentials to delete this file or that no other process is using this file.\n')

            #if the folder does already exists delete it and re-create it, in case the md structure changed
                   
    def exportMD(md_text, path):
        #    html_text = markdown.markdown(md_text), want html, then use the markdown library
        file = open(path, 'w' , encoding="utf-8")
        file.writelines(md_text)
        #write lines maybe now that the new def is with line and not onley .read()
        file.close()

    def mdTitleHeader(mdLines, title):
        mdLines.insert(0, '---\n')
        mdLines.insert(0, 'title: ' + title + '\n')
        mdLines.insert(0, '---\n')
        return mdLines
    
    def mdOptionsHeader(mdLines, title):
        ##maybe add logo ? -> example of first page pdf template
        dypsloom_logo = 'https://dypsloom.gitlab.io/static/53a3d484cd35b5f266070dd951a1c75c/497c6/dypsloom-logo-color.png'
        mdLines.insert(0,'<div style="font-size: 3em; font-weight: bold; text-align: center"> ' + title + '</div>\n')
        mdLines.insert(1,' \n')
        #mdLines.insert(2,'![alt text]('+ dypsloom_logo +')\n') #shows on the side and not centered
        mdLines.insert(2, '<div align="center"><img src="'+ dypsloom_logo +'"></div>')
        mdLines.insert(3,' \n') 
        mdLines.insert(4,'<div style="page-break-before:always"></div>')
        mdLines.insert(5,' \n')
        mdLines.insert(6,'<div style="font-size: 1em; font-weight: bold;">Table of Contents</div>\n') 
        mdLines.insert(7,' \n')
        mdLines.insert(8,'[[TOC]]') 
        mdLines.insert(9,' \n') 
        mdLines.insert(10,'<div style="page-break-before:always"></div>')
        mdLines.insert(11,' \n')
        mdLines.insert(12,' \n')
        return mdLines

    #initial file paths
    if os.path.isfile(pathOut): 
        pwd = os.path.dirname(pathOut)
    else: 
        pwd = os.path.dirname(pathOut)
        #createPath(pwd)
    #os.chdir(os.path.basename(pathIn)) 
    #pathIn = os.path.basename(pathIn) 

    ## Set up of arrays
    H = np.array([], dtype= 'int')
    levels = np.array([], dtype= 'int')
    h = []
    ht = []
    
    ### CODE
    
    #open existing md file as lines 
    with open(pathIn, 'r', encoding="utf-8") as f:
        lines= f.readlines()
        
    #get index and names of the sections by level
    for line in range (0, len(lines)):
        #print (str(line))
        ln = lines[line]
        ln = ln.replace('\n', '')
        
        if ln.startswith('---'):
            ### ???
            endHeader = line
            print (endHeader)
        elif ln.startswith('title: '):
            titleln = ln.replace('title: ', '')
            titlef = titleln.replace(' ', '')
            #where thedirectories md files is goint to be split
            mainPath = os.path.join(pwd, titlef)
            #check if dir exists, if not create it
            createPath(mainPath)
            os.chdir(mainPath)
        elif ln.startswith('## ') | ln.startswith('### ')| ln.startswith('#### '):
            if ln.startswith('## '):
               levels = np.append(levels,1)
               lnTmp = ln.replace('## ', '')
                 
            elif ln.startswith('### '):
               levels = np.append(levels,2)
               lnTmp = ln.replace('### ', '')
                             
            elif ln.startswith('#### '):
               levels = np.append(levels,3)
               lnTmp = ln.replace('#### ', '')
            H = np.append(H, line)
            ht.append(lnTmp)
            lnTmp = lnTmp.replace(' ', '') 
            lnTmp =  re.sub('[^0-9a-zA-Z]+', '_', lnTmp)                
            h.append(lnTmp)

    #add last line as the end of the final section
    #H sould have one more entry than the ht or levels as it represents the
    #starting and ending point of each section    
    H = np.append (H, len(lines))
    # Set all countings to zero as it will be used to label the parent folders
    H1, H2, H3= 0, 1, 1 

    # save a copy of the full md file with formatting for pdf
    fullfile = os.path.join(os.getcwd(), (titlef +'_main.md'))
    mdTmp = lines[H[0]: H[-1]]
    mdTmp = mdOptionsHeader(mdTmp, titleln)
    exportMD(mdTmp, fullfile)

    #create tree and save corresponding chuncks of md files within 
    for i in range (0, len(levels)):
        #get current chunk of text and give add the corresponding title
        strt= H[i]
        end = H[i+1]
        mdTmp = lines[strt: end]
        mdTitleHeader(mdTmp, h[i])
        
        if levels[i] == 1:
            #if level 1, create folder and  go in 
            sectionIndex = "{0:03}".format(H1)
            folderTmp = sectionIndex + '-'+ h[i]
            pathTmpFolder= os.path.join(os.getcwd(), folderTmp)
            createPath(pathTmpFolder) 
            H1+=1
            H2=1
            H3=1
            #create an 000 folder if more sections are about to get displayed in a lower level
            if i <= len(levels)-2:
                if levels[i+1]!=1:
                    introPath = os.path.join(pathTmpFolder, '000-')
                    createPath(introPath)
                    pathFileTmp = os.path.join(introPath, mdFileName)
                    exportMD(mdTmp, pathFileTmp)
                else:
                    pathFileTmp = os.path.join(pathTmpFolder, mdFileName)
                    exportMD(mdTmp, pathFileTmp)
            else:
                    pathFileTmp = os.path.join(pathTmpFolder, mdFileName)
                    exportMD(mdTmp, pathFileTmp)
                
        elif levels [i] == 2:
            sectionIndex = "{0:03}".format(H2)
            folderTmp = sectionIndex + '-'+ h[i]
            pathTmpFolderChild= os.path.join(pathTmpFolder, folderTmp)
            createPath(pathTmpFolderChild) 
            H2+=1
            #create an 000 folder if more sections are about to get displayed in a lower level
            if i <= len(levels)-2:
                if (levels[i+1]>2):
                    introPath = os.path.join(pathTmpFolderChild, '000-')
                    createPath(introPath)
                    pathFileTmp = os.path.join(introPath, mdFileName)
                    exportMD(mdTmp, pathFileTmp)
                else:
                    pathFileTmp = os.path.join(pathTmpFolderChild, mdFileName)
                    exportMD(mdTmp, pathFileTmp)
            else:
                pathFileTmp = os.path.join(pathTmpFolderChild, mdFileName)
                exportMD(mdTmp, pathFileTmp)
            
        elif levels [i] == 3: 
            sectionIndex = "{0:03}".format(H3)
            folderTmp = sectionIndex + '-'+ h[i]
            pathTmpFolderChildren= os.path.join(pathTmpFolderChild, folderTmp)
            createPath(pathTmpFolderChildren) 
    
            H3+=1
            pathFileTmp = os.path.join(pathTmpFolderChildren, mdFileName)
            exportMD(mdTmp, pathFileTmp)
            
    #set working direcory again to the starting point
    #print to return it to the js file as a message
    print (os.chdir(os.path.dirname(os.getcwd())))
    print( fullfile)
    print (mainPath)

if __name__ == '__main__':
    # obtaining optional inputs from pythonshell:
    if sys.argv[2] != sys.argv[1]:
        #path out has been deffined in the pythonRun function
        main (sys.argv[1], sys.argv[2])
    else: 
        # no output path has been defined by the user, input path will be used as defaults unpack
        main(sys.argv[1], sys.argv[1])