const fs = require('fs');
const path = require('path');

function sanitizeNames(directory) {
    const entries = fs.readdirSync(directory);

    for (const entry of entries) {
        const fullPath = path.join(directory, entry);
        const stats = fs.statSync(fullPath);

        if (stats.isDirectory()) {
            // Process directory contents first
            sanitizeNames(fullPath);
            
            // Then check the directory name itself
            const newDirName = entry.replace(/´/g, '-');
            if (newDirName !== entry) {
                const newDirPath = path.join(directory, newDirName);
                try {
                    fs.renameSync(fullPath, newDirPath);
                    console.log(`Renamed directory: ${fullPath} -> ${newDirPath}`);
                } catch (error) {
                    console.error(`Error renaming directory: ${fullPath}`, error);
                }
            }
        } else {
            // Process file name
            const newFileName = entry.replace(/´/g, '-');
            if (newFileName !== entry) {
                const newFilePath = path.join(directory, newFileName);
                try {
                    fs.renameSync(fullPath, newFilePath);
                    console.log(`Renamed file: ${fullPath} -> ${newFilePath}`);
                } catch (error) {
                    console.error(`Error renaming file: ${fullPath}`, error);
                }
            }
        }
    }
}

// Get target directory from command line
const targetDir = process.argv[2];

if (!targetDir) {
    console.error('Please provide a directory path as an argument');
    process.exit(1);
}

if (!fs.existsSync(targetDir)) {
    console.error('Directory does not exist');
    process.exit(1);
}

console.log(`Starting sanitization in: ${targetDir}`);
sanitizeNames(targetDir);
console.log('Sanitization complete!');