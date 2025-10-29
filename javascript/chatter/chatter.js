// chatter.js

const { OpenAIApi } = require('openai');
const fs = require('fs');

const config = {
  openaiKey: '<openai-key>',
  gptModel: 'text-davinci-003', 
  temperature: 0.5,
  maxTokens: 256
};

const conversation = [];
let logFileName; 

async function main() {

  const openai = new OpenAIApi(config.openaiKey);

  console.log('Ready...');
  console.log('Enter "clear" to start a new conversation, or "q" to quit.\n');
  
  while (true) {

    const input = await prompt('You: ');

    if (input.toLowerCase() === 'clear') {
      conversation.length = 0;
      logFileName = `conversation_${Date.now()}.txt`;
      printBot('Context cleared. Starting new chat.');
      continue;
    }
    
    if (input.toLowerCase() === 'q') {
      break; 
    }

    printBot('Thinking...');
    
    conversation.push({
      role: 'user',
      content: input
    });
    
    await logConversation(input);
    
    const response = await getResponse(openai, conversation);
    printBot(response);

    await logConversation(response);
  }
}

async function getResponse(openai, conversation) {
  const completion = await openai.createChatCompletion({
    model: config.gptModel, 
    messages: conversation,
    temperature: config.temperature,
    max_tokens: config.maxTokens
  });

  return completion.data.choices[0].message.content;
}

function printBot(text) {
  console.log('\x1b[32m%s\x1b[0m', `Bot: ${text}`); 
}

function prompt(text) {
  return new Promise(resolve => {
    process.stdout.write(text);
    process.stdin.on('data', data => {
      resolve(data.toString().trim());
      process.stdin.pause();
    });
  });
}

async function logConversation(text) {
  if (!logFileName) {
    logFileName = `conversation_${Date.now()}.txt`; 
  }
  
  await fs.promises.appendFile(logFileName, 
    `[${new Date().toISOString()}] ${text}\n`);
}

main();