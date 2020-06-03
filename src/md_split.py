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
def main ():
    #changes for pythonshell:
    #pathIn =(r'C:\\Users\\isabe\\Desktop\\npm_isa\\mainmd.md')
    pathIn= sys.argv[1]
    pwd = os.path.dirname(pathIn)    
    pathIn = os.path.basename(pathIn)
    '''
    returns the folder where the files have been split up
    '''
    ### INITIAL DEFINITIONS
    ## INPUTS
    #pwd = os.path.dirname(pathIn)    
    #pathIn = os.path.basename(pathIn)  
    
    #kwarg ? (change the options of the outcomming naming file)
    mdFileName= 'index.md'
    
    #Startin poit: work directory where all the parts are going to be saved 
    #pwd = os.getcwd()
    
    
    ### FUNCTIONS
    def createPath(path):
        ''' 
        checks if the iven files exists and if not it creates is 
        '''
        if os.path.exists(path) == False:
            os.mkdir(path)
        else:
            try:
                os.remove('Filename')
                os.mkdir(path)
            except OSError:
                print ('ERROR: Cannot delete file. Make sure your have enough credentials to delete this file or that no other process is using this file.\n')
                print (path)
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
            mainPath= os.path.join(pwd, titlef)
            #check if dir exists , if not create it
            createPath(mainPath)
            os.chdir(mainPath)
            # save a copy of the full md file
            fullfile = os.path.join(os.getcwd(), (titlef +'_main.md'))
            exportMD(lines, fullfile)
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
    #add last line as the endo of the final section
    #H sould have one more entry than the ht or levels as it represents the
    #starting and ending point of each section    
    H = np.append (H, len(lines))
    # Set all countings to zero as it will be used to label the parent folders
    H1, H2, H3= 0, 1, 1 

    #create tree and save corresponding chuncks of md files within 
    for i in range (0, len(levels)):
        #get current chunk of text and give add the corresponding title
        strt= H[i]
        end = H[i+1]
        mdTmp = lines[strt: end]
        mdTitleHeader(mdTmp, h[i])
        
        if levels[i] == 1:
            #if level 1 , create folder and  go in 
            sectionIndex = "{0:03}".format(H1)
            folderTmp = sectionIndex + '-'+ h[i]
            pathTmpFolder= os.path.join(os.getcwd(), folderTmp)
            createPath(pathTmpFolder) 
            #print (folderTmp)
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
            #print ('---' + h[i])
            sectionIndex = "{0:03}".format(H2)
            folderTmp = sectionIndex + '-'+ h[i]
            pathTmpFolderChild= os.path.join(pathTmpFolder, folderTmp)
            createPath(pathTmpFolderChild) 
            #print (folderTmp)
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
            #print ('-------' + h[i])    
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

    

# Start process

if __name__ == '__main__':
    main()