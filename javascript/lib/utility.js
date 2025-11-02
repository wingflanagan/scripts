/**
 * Pads an integer as a string with leading zeros.
 * 
 * @param   {int}   num   the number to pad with leading zeros
 * @param   {int}   size  the desired total length of the return string
 * @returns {string}      a string represent the input as a string padded with 
 *                        leading zeros
 */
function addLeadingZeros(num, size) {
  num = num.toString();
  while (num.length < size) num = "0" + num;
  return num;
}

// exports
module.exports.addLeadingZeros = addLeadingZeros;