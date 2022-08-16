#!/usr/bin/env python3

from fileinput import filename
import os
import sys;

def convertToProres(fullFileName, outputFolder):
    fileNameLength = len(fullFileName);
    lastDotPosition = fullFileName.rindex('.');
    lastSepPosition = fullFileName.rindex(os.path.sep);
    charsToRemove = fileNameLength - lastDotPosition;
    fileStem = fullFileName[:-charsToRemove];
    fileStem = fileStem[lastSepPosition + 1:];
    outFileName = os.path.join(outputFolder, fileStem + ".mov");

    commandTemplate = "ffmpeg -i {0} -vf scale=1920:1080 -c:v prores_ks -profile:v 3 -vendor apl0 -bits_per_mb 8000 -pix_fmt yuv422p10le {1}";
    command = commandTemplate.format(fullFileName, outFileName);

    os.system(command);

################################################################################
# MAIN PROGRAM
################################################################################
if __name__ == '__main__':
    MSG_USAGE = """\nUSAGE: {0} <file list> <output folder>
        file list: a text file containing the full path of each file to convert, one on each line
        output folder: the folder that receives the output files\n"""
    MSG_FILE_DOESNT_EXIST = "\nERROR: input file {0} does not exist!\n";
    MSG_FOLDER_DOESNT_EXIST = "\nERROR: output folder {0} does not exist!\n";

    # see if we have args
    if (len(sys.argv) < 3):
        print(MSG_USAGE.format(sys.argv[0]));
        exit;

    inputFileName = sys.argv[1];
    outputFolder = sys.argv[2];

    if (not os.path.exists(inputFileName)):
        print(MSG_FILE_DOESNT_EXIST.format(inputFileName));
        exit;

    if (not os.path.exists(outputFolder)):
        print(MSG_FOLDER_DOESNT_EXIST.format(outputFolder));
        exit;

    inputFile = open(inputFileName, "r");
    fileList = inputFile.readlines();

    for fileName in fileList:
        # strip the newline character, if there is one
        if (fileName.startswith("#")):
            continue;
        fileName = fileName.strip();
        if (os.path.exists(fileName)):
            convertToProres(fileName, outputFolder);
        else:
            print(fileName + " does not exist. Moving on...");
