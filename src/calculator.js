/**
 * Node.js CLI Calculator
 *
 * Supports the following operations:
 *   Basic:    add, subtract, multiply, divide
 *   Extended: modulo, power, squareRoot
 */

/**
 * Adds two numbers.
 * @param {number} a - First operand
 * @param {number} b - Second operand
 * @returns {number} Sum of a and b
 */
function add(a, b) {
  return a + b;
}

/**
 * Subtracts the second number from the first.
 * @param {number} a - First operand
 * @param {number} b - Second operand
 * @returns {number} Difference of a and b
 */
function subtract(a, b) {
  return a - b;
}

/**
 * Multiplies two numbers.
 * @param {number} a - First operand
 * @param {number} b - Second operand
 * @returns {number} Product of a and b
 */
function multiply(a, b) {
  return a * b;
}

/**
 * Divides the first number by the second.
 * @param {number} a - Dividend
 * @param {number} b - Divisor
 * @returns {number} Quotient of a divided by b
 * @throws {Error} If divisor is zero
 */
function divide(a, b) {
  if (b === 0) {
    throw new Error('Division by zero is not allowed');
  }
  return a / b;
}

/**
 * Returns the remainder of a divided by b (modulo operation).
 * @param {number} a - Dividend
 * @param {number} b - Divisor
 * @returns {number} Remainder of a divided by b
 * @throws {Error} If divisor is zero
 */
function modulo(a, b) {
  if (b === 0) {
    throw new Error('Modulo by zero is not allowed');
  }
  return a % b;
}

/**
 * Raises base to the given exponent.
 * @param {number} base - The base value
 * @param {number} exponent - The exponent value
 * @returns {number} base raised to the power of exponent
 */
function power(base, exponent) {
  return Math.pow(base, exponent);
}

/**
 * Returns the square root of n.
 * @param {number} n - The number to compute the square root of
 * @returns {number} Square root of n
 * @throws {Error} If n is negative
 */
function squareRoot(n) {
  if (n < 0) {
    throw new Error('Square root of a negative number is not defined');
  }
  return Math.sqrt(n);
}

module.exports = { add, subtract, multiply, divide, modulo, power, squareRoot };

// CLI interface — only runs when executed directly (not when required)
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log('Usage: node src/calculator.js <operation> <a> [b]');
    console.log('Operations: add, subtract, multiply, divide, modulo, power, squareRoot');
    process.exit(1);
  }

  const [operation, rawA, rawB] = args;
  const a = parseFloat(rawA);
  const b = rawB !== undefined ? parseFloat(rawB) : undefined;

  try {
    let result;
    switch (operation) {
      case 'add':        result = add(a, b); break;
      case 'subtract':   result = subtract(a, b); break;
      case 'multiply':   result = multiply(a, b); break;
      case 'divide':     result = divide(a, b); break;
      case 'modulo':     result = modulo(a, b); break;
      case 'power':      result = power(a, b); break;
      case 'squareRoot': result = squareRoot(a); break;
      default:
        console.error(`Unknown operation: ${operation}`);
        process.exit(1);
    }
    console.log(`Result: ${result}`);
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}
