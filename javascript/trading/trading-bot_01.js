/**
 * Automated Trading Bot using Alpaca's API
 *
 * DISCLAIMER: This code is for experimental and educational purposes only.
 * Trading carries inherent risks. Use this code at your own risk – you could lose money.
 *
 * The bot uses a simple moving-average crossover algorithm and supports adjustable risk levels.
 *
 * Before running, install dependencies:
 *    npm install @alpacahq/alpaca-trade-api
 *
 * Then, fill in your Alpaca API key/secret below and adjust the configuration if needed.
 */

const Alpaca = require('@alpacahq/alpaca-trade-api');
const fs = require('fs');

// ======== CONFIGURATION =========

// *** Fill in your Alpaca API credentials here ***
const API_KEY = 'YOUR_API_KEY_HERE';
const API_SECRET = 'YOUR_API_SECRET_HERE';

// Set to true for paper trading; false if you have a live account (but caution!)
const PAPER = true;

// The symbol to trade – you can change this to your preferred stock.
const SYMBOL = 'AAPL';

// Risk level settings: change riskLevel from 0.1 (safe = 10% of available cash per trade)
// up to 0.5 (aggressive = 50% per trade) or adjust as needed.
const riskLevel = 0.1;  // e.g., 0.1 = 10% of cash available per trade

// Trading algorithm selection:
// 'movingAverageCrossover' or 'rsi' (the RSI method is stubbed and not fully implemented)
const algorithmType = 'movingAverageCrossover';

// Parameters for the moving average crossover algorithm
const fastPeriod = 9;   // number of bars for fast moving average
const slowPeriod = 21;  // number of bars for slow moving average

// Data settings
const timeframe = '5Min';      // bar timeframe; adjust as allowed by Alpaca
const barsNeeded = slowPeriod + 1;  // fetch a few extra bars for calculations

// How often to run the main loop (in milliseconds)
// Here, every 5 minutes (the same as the bar timeframe) is suggested.
const loopInterval = 5 * 60 * 1000;

// Log file for trade and status messages:
const logFile = 'trades.txt';

// ======== END CONFIGURATION =========


// Initialize Alpaca client
const alpaca = new Alpaca({
  keyId: API_KEY,
  secretKey: API_SECRET,
  paper: PAPER,
});

// Utility: Append a message with timestamp to the log file.
function logMessage(message) {
  const timestamp = new Date().toISOString();
  const fullMessage = `[${timestamp}] ${message}\n`;
  console.log(fullMessage.trim());
  fs.appendFile(logFile, fullMessage, (err) => {
    if (err) {
      console.error('Error writing to log file:', err);
    }
  });
}

// Check if the market is open
async function isMarketOpen() {
  try {
    const clock = await alpaca.getClock();
    return clock.is_open;
  } catch (err) {
    logMessage(`Error getting market clock: ${err}`);
    return false;
  }
}

// Fetch recent bar data for the symbol
async function fetchBarData() {
  try {
    // Note: Alpaca's getBars accepts a symbol and options.
    // We request the latest barsNeeded bars.
    const bars = await alpaca.getBars(timeframe, SYMBOL, { limit: barsNeeded });
    // The returned structure is an object with keys as symbols.
    if (!bars[SYMBOL] || bars[SYMBOL].length < barsNeeded) {
      throw new Error(`Not enough bar data received for ${SYMBOL}`);
    }
    return bars[SYMBOL];
  } catch (err) {
    logMessage(`Error fetching bar data: ${err}`);
    return null;
  }
}

// Calculate a simple moving average (SMA) for an array of numbers.
function calculateSMA(data) {
  const sum = data.reduce((acc, val) => acc + val, 0);
  return sum / data.length;
}

// Moving average crossover algorithm
// Returns: "buy", "sell", or "hold"
function movingAverageCrossover(bars) {
  // Extract closing prices
  const closes = bars.map(bar => bar.close);
  if (closes.length < slowPeriod) {
    logMessage('Not enough data to calculate moving averages.');
    return 'hold';
  }

  // Calculate fast and slow moving averages using the most recent "fastPeriod" and "slowPeriod" bars.
  const fastMA = calculateSMA(closes.slice(-fastPeriod));
  const slowMA = calculateSMA(closes.slice(-slowPeriod));

  logMessage(`Calculated MAs for ${SYMBOL}: FastMA = ${fastMA.toFixed(2)}, SlowMA = ${slowMA.toFixed(2)}`);

  // A simple signal:
  // If fast MA is above slow MA, signal to buy; if below, signal to sell.
  if (fastMA > slowMA) {
    return 'buy';
  } else if (fastMA < slowMA) {
    return 'sell';
  }
  return 'hold';
}

// Stub for an RSI-based algorithm (for future extension)
function rsiAlgorithm(bars) {
  // (Implementation of RSI logic would go here.)
  // For now, just return "hold".
  return 'hold';
}

// Determine which algorithm to use and return its signal.
function getTradeSignal(bars) {
  switch (algorithmType) {
    case 'movingAverageCrossover':
      return movingAverageCrossover(bars);
    case 'rsi':
      return rsiAlgorithm(bars);
    default:
      logMessage(`Unknown algorithm type "${algorithmType}" specified.`);
      return 'hold';
  }
}

// Check if we currently have an open position in SYMBOL
async function isInPosition() {
  try {
    // If we have no position, Alpaca will throw an error.
    await alpaca.getPosition(SYMBOL);
    return true;
  } catch (err) {
    return false;
  }
}

// Get the current market price (last close price from bar data is used here)
function getCurrentPrice(bars) {
  // Use the close of the most recent bar.
  return bars[bars.length - 1].close;
}

// Execute trade orders based on the signal.
async function executeTrade(signal, bars) {
  const price = getCurrentPrice(bars);
  const inPosition = await isInPosition();
  let account;

  try {
    account = await alpaca.getAccount();
  } catch (err) {
    logMessage(`Error fetching account details: ${err}`);
    return;
  }

  // Calculate how much cash is available (Alpaca provides a "cash" property)
  const availableCash = parseFloat(account.cash);
  // Determine how much to allocate in this trade
  const tradeAmount = availableCash * riskLevel;

  // Determine quantity based on current price (round down to whole shares)
  const qty = Math.floor(tradeAmount / price);
  if (qty < 1) {
    logMessage('Not enough funds to buy even one share.');
    return;
  }

  if (signal === 'buy' && !inPosition) {
    logMessage(`Signal: BUY. Attempting to buy ${qty} shares of ${SYMBOL} at ~$${price.toFixed(2)} each.`);
    try {
      const order = await alpaca.createOrder({
        symbol: SYMBOL,
        qty: qty,
        side: 'buy',
        type: 'market',
        time_in_force: 'day', // Order expires at the end of the trading day.
      });
      logMessage(`Buy order placed. Order ID: ${order.id}`);
    } catch (err) {
      logMessage(`Error placing buy order: ${err}`);
    }
  } else if (signal === 'sell' && inPosition) {
    logMessage(`Signal: SELL. Attempting to sell all shares of ${SYMBOL}.`);
    try {
      // Sell the entire position
      const order = await alpaca.createOrder({
        symbol: SYMBOL,
        qty: 'all',  // 'all' indicates to liquidate the position
        side: 'sell',
        type: 'market',
        time_in_force: 'day',
      });
      logMessage(`Sell order placed. Order ID: ${order.id}`);
    } catch (err) {
      logMessage(`Error placing sell order: ${err}`);
    }
  } else {
    logMessage(`No trade executed. Signal: ${signal}. In position: ${inPosition}`);
  }
}

// Main trading loop
async function runTradingBot() {
  logMessage('--------------------------------------');
  logMessage('Starting trading bot cycle.');

  const marketOpen = await isMarketOpen();
  if (!marketOpen) {
    logMessage('Market is closed. Waiting until market opens...');
    return;
  }

  const bars = await fetchBarData();
  if (!bars) {
    logMessage('Could not retrieve bar data. Skipping this cycle.');
    return;
  }

  const signal = getTradeSignal(bars);
  logMessage(`Trade signal for ${SYMBOL}: ${signal}`);

  await executeTrade(signal, bars);

  // Optionally, you could add additional status logging here (e.g., current account balance).
}

// Start the loop immediately then every loopInterval milliseconds
runTradingBot();
setInterval(runTradingBot, loopInterval);
