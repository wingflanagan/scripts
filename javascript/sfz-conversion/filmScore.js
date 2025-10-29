// minimal-test.js

const blessed = require('blessed');

const screen = blessed.screen({
  smartCSR: true,
  title: 'Minimal Test'
});

const form = blessed.form({
  parent: screen,
  keys: true,
  mouse: true,
  input: true,
  left: 'center',
  top: 'center',
  width: '50%',
  height: '50%',
  border: 'line',
  label: ' Minimal Test ',
  padding: { left: 1, right: 1, top: 1, bottom: 1 }
});

const inputLabel = blessed.box({
  parent: form,
  top: 2,
  left: 2,
  content: 'Enter text:'
});

const textInput = blessed.textbox({
  parent: form,
  name: 'testInput',
  inputOnFocus: true,
  keys: true,
  mouse: true,
  top: 2,
  left: 15,
  width: 30,
  height: 1,
  border: { type: 'line' },
  style: {
    focus: {
      border: { fg: 'green' }
    }
  }
});

textInput.focus();

screen.key(['escape', 'q', 'C-c'], function() {
  return process.exit(0);
});

screen.render();
