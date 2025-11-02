// Import modules for file system access, path handling, Alpaca API, and CSV writing.
const fs = require('fs');
const path = require('path');
const Alpaca = require('@alpacahq/alpaca-trade-api');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

//==============================REAL==================================
//const API_KEY = 'AKI8W4HNIG9840A1QMQH';
//const API_SECRET = 'RgV8IMSvl2DTQAbsakIhg6MtuwEtHuDmzzkHcTaG';
//const BASE_URL = 'https://api.alpaca.markets';
//const PAPER = false;

//=============================PAPER==================================
const API_KEY = 'PKTW8AMKX80XHNMTNLVX';
const API_SECRET = 'UbEFDhKFpJJPn5ccSh3QM7Db1ahaDjb5pjYuZfA3';
const BASE_URL = 'https://paper-api.alpaca.markets';
const PAPER = true;

// List of stock symbols that the bot will monitor/trade.
const SYMBOLS = [
  //'AAPL',
  //'TSLA',
  //'GOOGL',
  //'AMZN',
  //'MSFT',
  //'INTC',
  'METU',
  'METD',
  'SOXL',
  'SOXS',
  'TSLL',
  'TSLQ',
  'PLTU',
  'PLTD'
];

// Trading parameters:
const SMA_PERIOD = 20;
const RSI_PERIOD = 14;
const RSI_OVERBOUGHT = 70;
const RSI_OVERSOLD = 30;
const RISK_FACTOR = 0.3;
const STOP_LOSS_PERCENT = 0.05;
const TAKE_PROFIT_PERCENT = 0.1;

// Define the file path for the CSV log that will record every trade.
const LOG_FILE = path.join(__dirname, 'trade_log.csv');

// to control whether the `market is closed` message shows
let marketIsClosed = false;

// Initialize the Alpaca API client with our API keys, trading mode, and base URL.
const alpaca = new Alpaca({
  keyId: API_KEY,
  secretKey: API_SECRET,
  paper: PAPER,
  baseUrl: BASE_URL
});

// Object to store purchase prices for potential future use (here for stop-loss/take-profit).
let purchasePrices = {};

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

// Set up CSV writer to log trade events. If the log file exists, new records will be appended.
const csvWriter = createCsvWriter({
  path: LOG_FILE,
  header: [
    { id: 'timestamp', title: 'Timestamp' },
    { id: 'symbol', title: 'Symbol' },
    { id: 'action', title: 'Action' },
    { id: 'quantity', title: 'Quantity' },
    { id: 'price', title: 'Price' },
    { id: 'sma', title: 'SMA' },
    { id: 'rsi', title: 'RSI' },
    { id: 'account_balance', title: 'Account Balance' }
  ],
  append: fs.existsSync(LOG_FILE),
});

function computeSMA(bars) {
  if (!bars || bars.length === 0) return NaN; // Handle empty or invalid input
  const total = bars.reduce((acc, bar) => {
    const close = Number(bar.ClosePrice); // Use 'ClosePrice' key
    if (isNaN(close)) {
      console.warn(`Invalid closing price in bar:`, bar);
      return acc + 0; // Treat invalid prices as 0
    }
    return acc + close;
  }, 0);
  return total / bars.length;
}

function computeRSI(bars) {
  const RSI_PERIOD = 14; // Adjust this based on your requirements
  if (!bars || bars.length < RSI_PERIOD) return null; // Not enough data
  
  let gains = 0, losses = 0;
  for (let i = 1; i < bars.length; i++) {
    const currentClose = Number(bars[i].ClosePrice) || 0; // Use 'ClosePrice'
    const previousClose = Number(bars[i - 1].ClosePrice) || 0; // Use 'ClosePrice'
    const change = currentClose - previousClose;
    if (change > 0) {
      gains += change;
    } else {
      losses -= change; // Accumulate positive losses (negative change becomes positive loss)
    }
  }
  const avgGain = gains / RSI_PERIOD;
  const avgLoss = losses / RSI_PERIOD;
  if (avgLoss === 0) return 100; // Avoid division by zero
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

/**
 * Fetch the latest trade price for
 *  a given symbol.
 */
async function getCurrentPrice(symbol) {
  try {
    // Omit feed parameter to use the default feed
    const trade = await alpaca.getLatestTrade(symbol);
    return parseFloat(trade.Price);
  } catch (error) {
    console.error(`Error fetching latest trade for ${symbol}:`, error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
    }
    return null;
  }
}

async function checkPosition(symbol) {
  try {
    const position = await alpaca.getPosition(symbol);
    return {
      inPosition: true,
      qty: parseFloat(position.qty),
      avgEntryPrice: parseFloat(position.avg_entry_price)
    };
  } catch (error) {
    return { inPosition: false, qty: 0, avgEntryPrice: null };
  }
}

/**
 * Fetch bars (historical price data) for the given symbol.
 * FIXED: Updated to handle API changes and add proper error handling.
 */
async function fetchBars(symbol) {
  let bars = [];
  try {
    for await (let bar of alpaca.getBarsV2(symbol, {
      timeframe: '1Min',
      limit: SMA_PERIOD + RSI_PERIOD,
      // feed: 'iex', // Removed to use default feed
    })) {
      bars.push(bar);
    }
    console.log(`Bars for ${symbol}:`, bars); // Debug
  } catch (error) {
    console.error(`Error fetching bars for ${symbol}:`, error);
    return null;
  }

  if (bars.length < SMA_PERIOD) {
    console.log(`Not enough bars received for ${symbol}. Required: ${SMA_PERIOD}, Received: ${bars.length}`);
    return null;
  }
  return bars;
}

async function logTrade(symbol, action, quantity, price, sma, rsi, accountBalance) {
  const timestamp = new Date().toISOString();
  await csvWriter.writeRecords([{ timestamp, symbol, action, quantity, price, sma, rsi, account_balance: accountBalance }]);
  console.log(`Logged: ${action} ${quantity} ${symbol} @ ${price}`);
}

async function tradingLoop() {
  try {
    const clock = await alpaca.getClock();
    if (!clock.is_open) {
      if (!marketIsClosed) {
        console.log('Market is closed. Next open time:', clock.next_open);
        marketIsClosed = true;
      }
      return;
    } else {
      marketIsClosed = false;
    }

    const account = await alpaca.getAccount();
    const availableCash = parseFloat(account.cash);
    console.log(`\n[${new Date().toISOString()}] Account Balance: $${availableCash.toFixed(2)}`);

    for (const SYMBOL of SYMBOLS) {
      const currentPrice = await getCurrentPrice(SYMBOL);
      if (!currentPrice) {
        console.log(`Skipping ${SYMBOL} due to missing price data.`);
        continue;
      }
      const bars = await fetchBars(SYMBOL);
      if (!bars) continue;
      await delay(1000); // 1-second delay between symbols

      const sma = computeSMA(bars.slice(-SMA_PERIOD));
      const rsi = computeRSI(bars.slice(-RSI_PERIOD));
      if (rsi === null) {
        console.log(`Not enough data to compute RSI for ${SYMBOL}`);
        continue;
      }
      console.log(`${SYMBOL}: Price = $${currentPrice.toFixed(2)}, SMA = $${sma.toFixed(2)}, RSI = ${rsi.toFixed(2)}`);

      const { inPosition, qty, avgEntryPrice } = await checkPosition(SYMBOL);

      if (inPosition) {
        const stopLossPrice = avgEntryPrice * (1 - STOP_LOSS_PERCENT);
        const takeProfitPrice = avgEntryPrice * (1 + TAKE_PROFIT_PERCENT);

        if (currentPrice <= stopLossPrice) {
          console.log(`STOP-LOSS triggered for ${SYMBOL}! Selling ${qty} shares at $${currentPrice.toFixed(2)}`);
          await alpaca.createOrder({
            symbol: SYMBOL,
            qty: qty,
            side: 'sell',
            type: 'market',
            time_in_force: 'gtc'
          });
          await logTrade(SYMBOL, 'STOP-LOSS SELL', qty, currentPrice, sma, rsi, account.cash);
          continue;
        }

        if (currentPrice >= takeProfitPrice) {
          console.log(`TAKE-PROFIT triggered for ${SYMBOL}! Selling ${qty} shares at $${currentPrice.toFixed(2)}`);
          await alpaca.createOrder({
            symbol: SYMBOL,
            qty: qty,
            side: 'sell',
            type: 'market',
            time_in_force: 'gtc'
          });
          await logTrade(SYMBOL, 'TAKE-PROFIT SELL', qty, currentPrice, sma, rsi, account.cash);
          continue;
        }
      }

      if (currentPrice > sma && !inPosition && rsi < RSI_OVERBOUGHT) {
        const maxInvestment = availableCash * RISK_FACTOR;
        const quantity = Math.floor(maxInvestment / currentPrice);
        if (quantity > 0) {
          console.log(`BUY Signal: Buying ${quantity} shares of ${SYMBOL} at $${currentPrice.toFixed(2)}`);
          await alpaca.createOrder({
            symbol: SYMBOL,
            qty: quantity,
            side: 'buy',
            type: 'market',
            time_in_force: 'gtc'
          });
          purchasePrices[SYMBOL] = currentPrice;
          await logTrade(SYMBOL, 'BUY', quantity, currentPrice, sma, rsi, account.cash);
        }
      }
      else if (inPosition && currentPrice < sma && rsi > RSI_OVERSOLD) {
        console.log(`SELL Signal: Selling ${qty} shares of ${SYMBOL} at $${currentPrice.toFixed(2)}`);
        await alpaca.createOrder({
          symbol: SYMBOL,
          qty: qty,
          side: 'sell',
          type: 'market',
          time_in_force: 'gtc'
        });
        await logTrade(SYMBOL, 'SELL', qty, currentPrice, sma, rsi, account.cash);
      }
      else {
        console.log(`No trade signal for ${SYMBOL}.`);
      }
    }
  } catch (err) {
    console.error('Error in trading loop:', err);
  }
}

async function startBot() {
  console.log('Starting Alpaca Trading Bot...');
  // Run immediately once
  await tradingLoop();
  // Then set interval
  setInterval(tradingLoop, 60 * 1000);
}

// Begin execution of the bot.
startBot();