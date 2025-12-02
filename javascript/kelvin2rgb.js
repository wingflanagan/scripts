#!/usr/bin/env node

// Simple CLI: convert black-body color temperature (Kelvin) to sRGB
// Usage: node kelvin2rgb.js 6500

function kelvinToRGB(kelvin) {
  // Clamp to a sane range
  let temp = Math.max(1000, Math.min(40000, kelvin)) / 100;

  let red, green, blue;

  // Red
  if (temp <= 66) {
    red = 255;
  } else {
    red = temp - 60;
    red = 329.698727446 * Math.pow(red, -0.1332047592);
    red = Math.max(0, Math.min(255, red));
  }

  // Green
  if (temp <= 66) {
    green = 99.4708025861 * Math.log(temp) - 161.1195681661;
  } else {
    green = temp - 60;
    green = 288.1221695283 * Math.pow(green, -0.0755148492);
  }
  green = Math.max(0, Math.min(255, green));

  // Blue
  if (temp >= 66) {
    blue = 255;
  } else if (temp <= 19) {
    blue = 0;
  } else {
    blue = temp - 10;
    blue = 138.5177312231 * Math.log(blue) - 305.0447927307;
    blue = Math.max(0, Math.min(255, blue));
  }

  return {
    r: Math.round(red),
    g: Math.round(green),
    b: Math.round(blue),
  };
}

function toHex(n) {
  const s = n.toString(16);
  return s.length === 1 ? "0" + s : s;
}

function printUsage() {
  console.log("Usage: kelvin2rgb <temperature-in-K>");
  console.log("Example: kelvin2rgb 6500");
}

// --- CLI handling ---

const arg = process.argv[2];

if (!arg || arg === "-h" || arg === "--help") {
  printUsage();
  process.exit(arg ? 0 : 1);
}

const kelvin = Number(arg);

if (!Number.isFinite(kelvin) || kelvin <= 0) {
  console.error("Error: temperature must be a positive number (Kelvin).");
  printUsage();
  process.exit(1);
}

const { r, g, b } = kelvinToRGB(kelvin);

const hex = "#" + toHex(r) + toHex(g) + toHex(b);
const rf = (r / 255).toFixed(4);
const gf = (g / 255).toFixed(4);
const bf = (b / 255).toFixed(4);

console.log(`Input temperature: ${kelvin} K`);
console.log("");
console.log("8-bit sRGB:");
console.log(`  R: ${r}`);
console.log(`  G: ${g}`);
console.log(`  B: ${b}`);
console.log("");
console.log("Normalized (0–1), good for shaders/emissive inputs:");
console.log(`  R: ${rf}`);
console.log(`  G: ${gf}`);
console.log(`  B: ${bf}`);
console.log("");
console.log(`Hex: ${hex}`);