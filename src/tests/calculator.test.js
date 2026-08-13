const { execFileSync } = require('child_process');
const path = require('path');

const {
  add,
  subtract,
  multiply,
  divide,
  modulo,
  power,
  squareRoot,
} = require('../calculator');

// Helper: run the calculator CLI and return stdout/stderr
function runCLI(args = []) {
  const script = path.resolve(__dirname, '../calculator.js');
  try {
    const stdout = execFileSync(process.execPath, [script, ...args], {
      encoding: 'utf8',
    });
    return { stdout: stdout.trim(), exitCode: 0 };
  } catch (err) {
    return {
      stdout: (err.stdout || '').trim(),
      stderr: (err.stderr || '').trim(),
      exitCode: err.status || 1,
    };
  }
}

describe('Basic Calculator Operations', () => {
  // --- add ---
  describe('add()', () => {
    test('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });
    test('adds a positive and a negative number', () => {
      expect(add(10, -4)).toBe(6);
    });
    test('adds two negative numbers', () => {
      expect(add(-3, -7)).toBe(-10);
    });
    test('adds zero to a number', () => {
      expect(add(5, 0)).toBe(5);
    });
    test('adds decimal numbers', () => {
      expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });
  });

  // --- subtract ---
  describe('subtract()', () => {
    test('subtracts two positive numbers', () => {
      expect(subtract(10, 4)).toBe(6);
    });
    test('subtracts a larger number from a smaller one', () => {
      expect(subtract(3, 7)).toBe(-4);
    });
    test('subtracts zero', () => {
      expect(subtract(5, 0)).toBe(5);
    });
    test('subtracts negative numbers', () => {
      expect(subtract(-3, -2)).toBe(-1);
    });
  });

  // --- multiply ---
  describe('multiply()', () => {
    test('multiplies two positive numbers', () => {
      expect(multiply(3, 4)).toBe(12);
    });
    test('multiplies by zero', () => {
      expect(multiply(99, 0)).toBe(0);
    });
    test('multiplies two negative numbers', () => {
      expect(multiply(-3, -4)).toBe(12);
    });
    test('multiplies a positive and a negative number', () => {
      expect(multiply(5, -3)).toBe(-15);
    });
    test('multiplies decimal numbers', () => {
      expect(multiply(2.5, 4)).toBe(10);
    });
  });

  // --- divide ---
  describe('divide()', () => {
    test('divides two positive numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });
    test('divides resulting in a decimal', () => {
      expect(divide(7, 2)).toBe(3.5);
    });
    test('divides negative by positive', () => {
      expect(divide(-12, 4)).toBe(-3);
    });
    test('divides zero by a number', () => {
      expect(divide(0, 5)).toBe(0);
    });
    test('throws an error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero is not allowed');
    });
  });
});

describe('Extended Calculator Operations', () => {
  // --- modulo ---
  describe('modulo()', () => {
    test('returns remainder of 10 % 3', () => {
      expect(modulo(10, 3)).toBe(1);
    });
    test('returns 0 when evenly divisible', () => {
      expect(modulo(9, 3)).toBe(0);
    });
    test('handles negative dividend', () => {
      expect(modulo(-10, 3)).toBe(-1);
    });
    test('throws an error when divisor is zero', () => {
      expect(() => modulo(10, 0)).toThrow('Modulo by zero is not allowed');
    });
  });

  // --- power ---
  describe('power()', () => {
    test('raises 2 to the power of 3', () => {
      expect(power(2, 3)).toBe(8);
    });
    test('raises a number to the power of 0', () => {
      expect(power(5, 0)).toBe(1);
    });
    test('raises a number to the power of 1', () => {
      expect(power(7, 1)).toBe(7);
    });
    test('raises a negative base to an even exponent', () => {
      expect(power(-3, 2)).toBe(9);
    });
    test('raises a number to a negative exponent', () => {
      expect(power(2, -2)).toBe(0.25);
    });
    test('raises 0 to the power of 0', () => {
      expect(power(0, 0)).toBe(1);
    });
  });

  // --- squareRoot ---
  describe('squareRoot()', () => {
    test('returns square root of 9', () => {
      expect(squareRoot(9)).toBe(3);
    });
    test('returns square root of 0', () => {
      expect(squareRoot(0)).toBe(0);
    });
    test('returns square root of 2 (irrational)', () => {
      expect(squareRoot(2)).toBeCloseTo(1.41421356);
    });
    test('returns square root of a perfect square', () => {
      expect(squareRoot(144)).toBe(12);
    });
    test('throws an error for negative numbers', () => {
      expect(() => squareRoot(-1)).toThrow(
        'Square root of a negative number is not defined'
      );
    });
  });
});
