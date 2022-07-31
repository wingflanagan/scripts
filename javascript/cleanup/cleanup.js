var fileSystem = require("../lib/filesystem");
var util = require("../lib/utility");
var path = require("path");

/********************************************************************************
 * Main portion of the script - cleans files and folders unique to my setup, 
 * including archiving last month's log files and deleting them from the work-log 
 * folder to keep it nice and clean.
 * ******************************************************************************/

// places to go and things to see...
var userFolder = "c:\\Users\\jflana";
var oneDriveFolder = path.join(userFolder, "\\OneDrive - UW");
var workLogFolder = path.join(oneDriveFolder, "\\work-log\\");
var archiveFolder = path.join(workLogFolder, "archive\\");
var obsidianTrashFolder = path.join(workLogFolder, "\\.trash");
var workAttachmentsFolder = path.join(workLogFolder, "\\attachments");
var downloads = path.join(userFolder, "\\Downloads");
var shareXBase = path.join(oneDriveFolder, "\\Documents\\ShareX");
var shareXCache = path.join(shareXBase, "\\Screenshots");
var shareXLogs = path.join(shareXBase, "\\Logs");
var shareXBackup = path.join(shareXBase, "\\Backup");
var temp = process.env["TEMP"];
var tmp = process.env["TMP"];

// get the first day of the current month as a date
var currentDate = new Date();
var currentYear = currentDate.getFullYear();
var currentMonth = currentDate.getMonth();
var olderThanDate = new Date(currentYear, currentMonth, 1);

// get the files in work log older than the start of this month and archive them
var files = fileSystem.getFiles(workLogFolder);
files = fileSystem.getFilesOlderThan(files, olderThanDate);
var workfolderArchive = "work-log_" + currentYear + "_" + util.addLeadingZeros(currentMonth, 2) + ".zip";
workfolderArchive = path.join(archiveFolder, workfolderArchive);
fileSystem.archiveFiles(workfolderArchive, files);

// get the files in work attachments older than the start of this month and archive them
var files = fileSystem.getFilesOlderThan(fileSystem.getFiles(workAttachmentsFolder), olderThanDate);
var workAttachmentFolderArchive = "work-att_" + currentYear + "_" + util.addLeadingZeros(currentMonth, 2) + ".zip";
workAttachmentFolderArchive = path.join(archiveFolder, workAttachmentFolderArchive);
fileSystem.archiveFiles(workAttachmentFolderArchive, files);

// kill temp folders
fileSystem.deleteFiles(fileSystem.getFiles(temp), true);
fileSystem.deleteFiles(fileSystem.getFiles(tmp), true);
fileSystem.deleteFiles(fileSystem.getFiles(downloads), true);

// empty Obsidian trash
fileSystem.deleteFiles(fileSystem.getFiles(obsidianTrashFolder), true);

// delete ShareX cruft
fileSystem.deleteFiles(fileSystem.getFiles(shareXCache), true);
fileSystem.deleteFiles(fileSystem.getFiles(shareXLogs), true);
fileSystem.deleteFiles(fileSystem.getFiles(shareXBackup), true);