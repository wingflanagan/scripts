#!/usr/bin/env node

// includes
const { spawn } = require('child_process');
const { exit } = require('process');
const readline = require('readline');
const fileSystem = require('../lib/filesystem');

/**
 * Converts a video file named in the inFileName parameter to ProRes 422 by 
 * calling ffmpeg to convert the file and write it to the ourput folder using the 
 * same file name with a new 'mov' extension.
 * 
 * @param {string} inFileName   The name of the file to convert
 * @param {string} outputFolder The folder to write the converted file to
 */
function convertToProres(inFileName, outputFolder) {
    const lastDotPosition = inFileName.lastIndexOf('.');
    const lastSepPosition = inFileName.lastIndexOf(fileSystem.path.sep);    
    const fileStem = inFileName.substring(lastSepPosition,lastDotPosition);
    const outFileName = fileSystem.path.join(outputFolder, fileStem + '.mov');

    const command = 'ffmpeg';
    const commandArgs = ['-i', inFileName, '-vf', 'scale=1920:1080', '-c:v', 'prores_ks', '-profile:v', 
        '3', '-vendor', 'apl0', '-bits_per_mb', '8000', '-pix_fmt', 'yuv422p10le', outFileName];

    const prop = spawn(command, commandArgs);
    
    prop.stdout.on('data', output => {1
        console.log(output.toString())
    });

    prop.stderr.on('data', output => {
        console.log(output.toString());
    });

    prop.on('error',  error => console.log('Process exited with error: ', error.toString()));
}

// eliminate the first two params (which are the exec program - node - and the name of the script)
const args = process.argv.slice(2);

// make sure we have the right number of args passed in
if (args.length != 2) {
    console.log('Error: wrong number of arguments\n\nUsage: convert2prores.js <file list> <destination folder>');
}

const listFileName = args[0];
const outputFolder = args[1];

// check for the existence of the list file and output path
if (!fileSystem.fs.existsSync(listFileName)) {
    console.log(`Error: input file ${listFileName} does not exist`);
    exit();
}

if (!fileSystem.fs.existsSync(outputFolder)) {
    console.log(`Error: output folder ${outputFolder} does not exist`);
    exit();
}

// read the list file and convert the files listed
const reader = readline.createInterface({
    input: fileSystem.fs.createReadStream(listFileName),
    output: process.stdout,
    console: false
});

reader.on('line', line => convertToProres(line, args[1]));
