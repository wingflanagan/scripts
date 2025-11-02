#!/usr/bin/env node

const readline = require('readline');

// Process command-line arguments
const args = process.argv.slice(2);

// Default framerate
let framerate = 24;
let dropFrame = false;

// Help message
const helpMessage = `
Timecode Calculator

Usage: node app.js [framerate] [d]

Options:
  framerate   The frame rate of the project (e.g., 23.976, 24, 25, 29.97, etc.)
  d           Use drop-frame calculations (only applicable for certain frame rates)

Commands:
  Digits (0-9): Build timecode
  +, -, =      Operators
  c            Clear current calculation
  q            Quit the application
  h            Display this help message
  Backspace    Delete the last digit entered

Notes:
- The timecode is displayed in the format HH:MM:SS.FF
- As you type digits, they shift left, and new digits appear on the right
- Press + or - to add or subtract timecodes
- Press = to compute the result
`;

if (args.includes('--help') || args.includes('help') || args.includes('-h')) {
    console.log(helpMessage);
    process.exit(0);
}

// Parse framerate and drop-frame option
args.forEach(arg => {
    if (arg === 'd') {
        dropFrame = true;
    } else if (!isNaN(parseFloat(arg))) {
        framerate = parseFloat(arg);
    }
});

// Validating framerate
if (isNaN(framerate) || framerate <= 0) {
    console.error('Invalid framerate specified.');
    process.exit(1);
}

console.log(`Timecode Calculator started with framerate ${framerate}${dropFrame ? ' (drop-frame)' : ''}`);
console.log('Press h for help');
console.log(' ' + '00:00:00.00'); // Initial display with space for alignment
console.log('Type digits to build timecode.');

// Set up stdin
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

// Variables
let digitsBuffer = []; // Stores digits entered for current timecode
let operands = [];     // Stores timecodes (in frames)
let operators = [];    // Stores operators ('+' or '-')
let currentDisplay = '00:00:00.00';
let operatorPrefix = ''; // Holds the current operator prefix for display

process.stdin.on('keypress', (str, key) => {
    if (key && key.ctrl && key.name === 'c') {
        process.exit();
    } else if (key && key.name === 'q') {
        process.exit();
    } else if (key && key.name === 'h') {
        console.log('\n' + helpMessage);
        console.log(operatorPrefix + currentDisplay);
    } else if (key && key.name === 'backspace') {
        if (digitsBuffer.length > 0) {
            digitsBuffer.pop();
            updateDisplay();
        }
    } else if (key && key.name === 'c') {
        digitsBuffer = [];
        operands = [];
        operators = [];
        currentDisplay = '00:00:00.00';
        operatorPrefix = '';
        console.log('\nCleared.');
        console.log(' ' + currentDisplay); // Add space for alignment
    } else if (str === '+' || str === '-') {
        if (digitsBuffer.length === 0 && operands.length === 0) {
            console.log('\nNo timecode entered yet.');
            console.log(' ' + currentDisplay); // Add space for alignment
        } else {
            if (digitsBuffer.length > 0) {
                let frames = digitsBufferToFrames(digitsBuffer);
                operands.push(frames);
                digitsBuffer = [];
            }
            operators.push(str);
            operatorPrefix = str;
            currentDisplay = '00:00:00.00';
            process.stdout.write('\n' + operatorPrefix + currentDisplay);
        }
    } else if (str === '=') {
        if (digitsBuffer.length === 0 && operands.length === 0) {
            console.log('\nNo timecode entered yet.');
            console.log(operatorPrefix + currentDisplay);
        } else {
            if (digitsBuffer.length > 0) {
                let frames = digitsBufferToFrames(digitsBuffer);
                operands.push(frames);
                digitsBuffer = [];
            }
            // Perform calculation
            let resultFrames = operands[0];
            for (let i = 0; i < operators.length; i++) {
                let operator = operators[i];
                let operandFrames = operands[i + 1];
                if (operator === '+') {
                    resultFrames = resultFrames + operandFrames;
                } else if (operator === '-') {
                    // Subtract smaller from larger
                    resultFrames = Math.abs(resultFrames - operandFrames);
                }
            }
            // Convert resultFrames to timecode
            let resultTimecode = framesToTimecode(resultFrames);
            currentDisplay = formatTimecode(resultTimecode);
            console.log('\n=' + currentDisplay);
            // Prepare for next calculation
            digitsBuffer = [];
            operands = [resultFrames]; // Set the result as the first operand
            operators = [];
            operatorPrefix = ''; // Reset operator prefix
            // Display the result for further operations
            process.stdout.write(' ' + currentDisplay);
        }
    } else if ('0123456789'.includes(str)) {
        // It's a digit
        if (digitsBuffer.length >= 8) {
            digitsBuffer.shift(); // Remove the leftmost digit
        }
        digitsBuffer.push(str);
        updateDisplay();
    } else {
        // Ignore other keys
    }
});

function updateDisplay() {
    let timecodeStr = formatDigitsBuffer(digitsBuffer);
    currentDisplay = timecodeStr;
    process.stdout.clearLine();
    process.stdout.cursorTo(0);
    if (operatorPrefix) {
        process.stdout.write(operatorPrefix + currentDisplay);
    } else {
        // Add space for alignment
        process.stdout.write(' ' + currentDisplay);
    }
}

function formatDigitsBuffer(digitsBuffer) {
    let digits = digitsBuffer.join('').padStart(8, '0');
    let hh = digits.slice(0, 2);
    let mm = digits.slice(2, 4);
    let ss = digits.slice(4, 6);
    let ff = digits.slice(6, 8);

    return `${hh}:${mm}:${ss}.${ff}`;
}

function digitsBufferToFrames(digitsBuffer) {
    let digits = digitsBuffer.join('').padStart(8, '0');
    let hours = parseInt(digits.slice(0, 2), 10);
    let minutes = parseInt(digits.slice(2, 4), 10);
    let seconds = parseInt(digits.slice(4, 6), 10);
    let frames = parseInt(digits.slice(6, 8), 10);

    let timecode = { hours, minutes, seconds, frames };

    return timecodeToFrames(timecode);
}

function timecodeToFrames(tc) {
    let totalSeconds = tc.hours * 3600 + tc.minutes * 60 + tc.seconds;
    let totalFrames = totalSeconds * framerate + tc.frames;

    if (dropFrame) {
        // Drop-frame calculations (only for 29.97 and 59.94)
        if (framerate === 29.97 || framerate === 59.94) {
            let dropFrames = Math.round(framerate * 0.066666);
            let framesPerHour = Math.round(framerate * 3600);
            let framesPer24Hours = framesPerHour * 24;
            let framesPer10Minutes = Math.round(framerate * 600);
            let framesPerMinute = Math.round(framerate * 60) - dropFrames;

            let d = totalFrames;
            let frameNumber = d % framesPer24Hours;

            let droppedFrames = dropFrames * (Math.floor(frameNumber / framesPer10Minutes) * 9 + Math.floor((frameNumber % framesPer10Minutes - dropFrames) / framesPerMinute));

            totalFrames = totalFrames - droppedFrames;
        } else {
            console.warn('Drop-frame is only applicable for framerates 29.97 and 59.94.');
        }
    }

    return totalFrames;
}

function framesToTimecode(frames) {
    let frameRateInt = Math.round(framerate);
    if (dropFrame && (framerate === 29.97 || framerate === 59.94)) {
        // Drop-frame timecode calculations
        let dropFrames = Math.round(framerate * 0.066666);
        let framesPerHour = frameRateInt * 3600;
        let framesPer24Hours = framesPerHour * 24;
        let framesPer10Minutes = frameRateInt * 600;
        let framesPerMinute = frameRateInt * 60 - dropFrames;

        frames = frames % framesPer24Hours;

        let d = frames;

        let totalHours = Math.floor(d / framesPerHour);
        d = d % framesPerHour;

        let totalMinutes = Math.floor(d / framesPerMinute);
        d = d % framesPerMinute;

        // Account for dropped frames
        let totalDroppedFrames = dropFrames * (totalHours * 60 + totalMinutes - Math.floor(totalMinutes / 10) * 10);
        d += totalDroppedFrames;

        let totalSeconds = Math.floor(d / frameRateInt);
        let frame = d % frameRateInt;

        let minutes = totalMinutes % 60;
        let seconds = totalSeconds % 60;
        let hours = totalHours;

        return {
            hours,
            minutes,
            seconds,
            frames: frame
        };
    } else {
        // Non-drop-frame calculations
        let totalSeconds = Math.floor(frames / framerate);
        let remainingFrames = frames % framerate;

        let hours = Math.floor(totalSeconds / 3600);
        let minutes = Math.floor((totalSeconds % 3600) / 60);
        let seconds = totalSeconds % 60;
        let frame = Math.floor(remainingFrames);

        return { hours, minutes, seconds, frames: frame };
    }
}

function formatTimecode(timecode) {
    let hh = String(timecode.hours).padStart(2, '0');
    let mm = String(timecode.minutes).padStart(2, '0');
    let ss = String(timecode.seconds).padStart(2, '0');
    let ff = String(timecode.frames).padStart(2, '0');

    return `${hh}:${mm}:${ss}.${ff}`;
}

function framesToDigitsBuffer(frames) {
    let timecode = framesToTimecode(frames);
    let hh = String(timecode.hours).padStart(2, '0');
    let mm = String(timecode.minutes).padStart(2, '0');
    let ss = String(timecode.seconds).padStart(2, '0');
    let ff = String(timecode.frames).padStart(2, '0');

    let digitsStr = hh + mm + ss + ff;

    // Remove leading zeros if any
    digitsStr = digitsStr.replace(/^0+/, '');

    return digitsStr.split('');
}

