var fs = require("fs");
var path = require("path");
var yazl = require("yazl");

/**
 * Returns a list of files from an input list, that are older than a certain 
 * date.
 * 
 * Loops through the array of file FQNs supplied in the fileList parameter and 
 * filters them by birthtime (NOT modified time), returning them in another 
 * string string array.
 * 
 * @param   {string[]}  fileList      list of files from which to select
 * @param   {Date}      olderThanDate the date to compare the files against
 * @returns {string[]}                the list of filtered file FQNs
 */
function getFilesOlderThan(fileList, olderThanDate) {
  var result = [];

  // loop the input list
  for (var i = 0; i < fileList.length; i++) {    
    // like Unix, the information about the file is obtained through stat
    var fileStat = fs.statSync(fileList[i]);

    if (fileStat.isFile() && fileStat.birthtime < olderThanDate) {
      result.push(fileList[i]);
    }
  }

  return result;
}

/**
 * Returns a list of files and folders in a specified direcrory.
 * 
 * The function does not distinguish between files and folders because there are
 * several points where we want to delete the subfolders, as well as the files in 
 * the folder.
 * 
 * @param   {string}  folder  the folder in which to look for files and folders
 * @returns {string[]}        list of files and folders in the specified folder
 */
function getFiles(folder) {
  var result = [];

  try {
    var fileList = fs.readdirSync(folder);
    for (var i = 0; i < fileList.length; i++) {
      result.push(path.join(folder, fileList[i]));
    }
  } catch (error) {
    // do nothing - we want to return empty array if there is an issue
  }  

  return result;
}

/**
 * Deletes the files named in a string array.
 * 
 * Optionally, the function will recursively delete folders, as well, since temp
 * folders in Windows often contain temprary subfolders. as well. The default is
 * to leave them alone.
 * 
 * @param {string[]}  fileList  Fully-qualified names of the files to delete
 */
function deleteFiles(fileList, includFolders = false) {
  for (var i = 0; i < fileList.length; i++) { 
    try {   
      var fileStat = fs.statSync(fileList[i]);    

      if (fileStat.isFile()) {
        console.log("Deleting file " + fileList[i]);        
        fs.unlink(fileList[i], (err) => {
          if (err) console.log("Error deleting file " + fileList[i]);
        }) 
      }

      if (fileStat.isDirectory() && includFolders) {
        console.log("Deleting directory " + fileList[i]);
        fs.rm(fileList[i], { recursive: true, force: true }, (err) => {
          if (err) console.log("Error deleting directory " + fileList[i]);
        })
      }

    } catch (error) {
      console.log("Could not delete  " + fileList[i] + ", moving on...");
    }
  }
}

/**
 *  Archives list of files in a zip file, then deletes the originals.
 * 
 * @param {string}    zipFileName Name of the output archive
 * @param {string[]}  fileList    Files to archive
 */
function archiveFiles(zipFileName, fileList) {
  var zipFile = new yazl.ZipFile();

  for (var i = 0; i < fileList.length; i++) {
    var fileName = fileList[i];
    var fileBaseName = path.basename(fileName);
    zipFile.addFile(fileName, fileBaseName);
  }
  
  zipFile.end();
  zipFile.outputStream.pipe(fs.createWriteStream(zipFileName)).on("close", function() {
    console.log('zip file ' + zipFileName + ' created');
    deleteFiles(fileList, false);
  });  

}

// exports
module.exports.getFilesOlderThan = getFilesOlderThan;
module.exports.getFiles = getFiles;
module.exports.deleteFiles = deleteFiles;
module.exports.archiveFiles = archiveFiles;
module.exports.path = path;
module.exports.fs = fs;