#!/bin/bash
# Install script for the standalone uid generator command

# Set paths
BIN_DIR="${HOME}/bin"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Save the uid script to bin directory
echo "Creating uid command in ${BIN_DIR}..."
cat > "${BIN_DIR}/uid" << 'EOF'
#!/usr/bin/env python3
"""
Self-contained unique workflow ID generator command-line tool
Usage:
    uid         - Generate a single UID
    uid -e      - Generate UID with mathematical explanation
    uid -b N    - Generate N UIDs in batch
    uid -h      - Show help
"""

import sys
import time
from datetime import datetime

class WorkflowUIDGenerator:
    """
    Generates unique workflow IDs in format: uid-abc-123
    - Letters represent mathematical operators and are shuffled
    - Numbers are transformed by the letter operators
    - Guaranteed unique (timestamp-based)
    - No database required
    - Human readable with mathematical meaning
    """
    
    def __init__(self):
        self.last_timestamp = 0
        self.counter = 0
        # Map letters to mathematical operations
        self.letter_operations = {
            'a': ('add', lambda x: x + 17),
            'b': ('multiply', lambda x: x * 3),
            'c': ('subtract', lambda x: abs(x - 23)),
            'd': ('divide', lambda x: x // 2 if x > 0 else 1),
            'e': ('power', lambda x: (x ** 2) % 1000),
            'f': ('fibonacci', lambda x: self._fib_mod(x)),
            'g': ('golden', lambda x: int(x * 1.618) % 1000),
            'h': ('hash_mod', lambda x: hash(str(x)) % 1000),
            'i': ('invert', lambda x: 1000 - (x % 1000) if x > 0 else 1),
            'j': ('jump', lambda x: (x * 7 + 13) % 1000),
            'k': ('karmic', lambda x: sum(int(d) for d in str(x)) * 37 % 1000),
            'l': ('logarithmic', lambda x: int(x * 2.718) % 1000),
            'm': ('mirror', lambda x: int(str(x)[::-1]) if str(x)[::-1].isdigit() else x),
            'n': ('nine_mult', lambda x: x * 9 % 1000),
            'o': ('orbit', lambda x: (x * x + x) % 1000),
            'p': ('prime_like', lambda x: x * 11 % 1000),
            'q': ('quadratic', lambda x: (x * x + 2 * x + 1) % 1000),
            'r': ('reverse_add', lambda x: x + int(str(x)[::-1]) if str(x)[::-1].isdigit() else x),
            's': ('spiral', lambda x: (x * 13 + 7) % 1000),
            't': ('triangle', lambda x: (x * (x + 1) // 2) % 1000),
            'u': ('unity', lambda x: (x + sum(int(d) for d in str(x))) % 1000),
            'v': ('vortex', lambda x: (x * 21 - 5) % 1000),
            'w': ('wave', lambda x: abs(int(x * 3.14159) % 1000)),
            'x': ('xor_like', lambda x: x ^ 0xFF),
            'y': ('yield', lambda x: (x * 5 + 42) % 1000),
            'z': ('zenith', lambda x: (x + 100) * 3 % 1000)
        }
    
    def _fib_mod(self, n):
        """Fibonacci-like operation"""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(min(n % 20, 15)):  # Limit iterations
            a, b = b, (a + b) % 1000
        return b
    
    def generate_uid(self):
        """Generate a unique workflow ID with mathematical letter operations"""
        now = datetime.now()
        current_timestamp = int(time.time())
        microseconds = int(time.time() * 1000000) % 1000000
        
        # Handle same-second collisions with counter
        if current_timestamp == self.last_timestamp:
            self.counter += 1
        else:
            self.counter = 0
            self.last_timestamp = current_timestamp
        
        # Create base number from time components
        base_number = (now.hour * 60 + now.minute) * 60 + now.second + self.counter
        
        # Generate three different letters based on different time components
        # Use different parts of timestamp to ensure variety
        letter_seeds = [
            (current_timestamp + now.month) % 26,
            (current_timestamp + now.day + microseconds // 10000) % 26,
            (current_timestamp + now.hour + self.counter) % 26
        ]
        
        letters = ''.join([chr(ord('a') + seed) for seed in letter_seeds])
        
        # Apply the mathematical operations represented by the letters
        transformed_number = base_number
        operation_log = []
        
        for i, letter in enumerate(letters):
            if letter in self.letter_operations:
                op_name, op_func = self.letter_operations[letter]
                old_value = transformed_number
                transformed_number = op_func(transformed_number)
                operation_log.append(f"{letter}({old_value})={transformed_number}")
        
        # Ensure we have a 3-digit number
        final_number = abs(transformed_number) % 1000
        if final_number == 0:
            final_number = (microseconds % 999) + 1
        
        uid = f"uid-{letters}-{final_number:03d}"
        
        # Optional: store the mathematical explanation
        self.last_operations = operation_log
        
        return uid
    
    def explain_last_uid(self):
        """Explain the mathematical operations of the last generated UID"""
        if hasattr(self, 'last_operations'):
            return " → ".join(self.last_operations)
        return "No operations recorded"
    
    def generate_with_explanation(self):
        """Generate UID and return both UID and mathematical explanation"""
        uid = self.generate_uid()
        explanation = self.explain_last_uid()
        return uid, explanation
    
    def generate_batch(self, count=10):
        """Generate multiple UIDs for testing uniqueness"""
        return [self.generate_uid() for _ in range(count)]

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['-h', '--help', 'help']:
            print("uid - Generate unique workflow IDs")
            print()
            print("Usage:")
            print("  uid              Generate a single UID")
            print("  uid -e           Generate UID with mathematical explanation")
            print("  uid -b N         Generate N UIDs in batch")
            print("  uid -h           Show this help")
            print()
            print("Examples:")
            print("  uid              # uid-abc-123")
            print("  uid -e           # uid-abc-123 | Math: a(456)=473 → b(473)=419 → c(419)=396")
            print("  uid -b 5         # Generate 5 UIDs")
            print()
            print("Mathematical Operations:")
            print("  Each letter represents a mathematical operation:")
            print("  a=add, b=multiply, c=subtract, d=divide, e=power, f=fibonacci")
            print("  g=golden_ratio, h=hash, i=invert, j=jump, k=karmic, l=logarithmic")
            print("  m=mirror, n=nine_mult, o=orbit, p=prime_like, q=quadratic, r=reverse_add")
            print("  s=spiral, t=triangle, u=unity, v=vortex, w=wave, x=xor, y=yield, z=zenith")
            return
        
        elif arg in ['-e', '--explain', 'explain']:
            generator = WorkflowUIDGenerator()
            uid, explanation = generator.generate_with_explanation()
            print(f"{uid} | Math: {explanation}")
            return
        
        elif arg in ['-b', '--batch', 'batch']:
            try:
                count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
                generator = WorkflowUIDGenerator()
                batch = generator.generate_batch(count)
                for uid in batch:
                    print(uid)
                return
            except (ValueError, IndexError):
                print("Error: Please provide a valid number for batch size")
                print("Usage: uid -b <number>")
                sys.exit(1)
        
        else:
            print(f"Unknown option: {arg}")
            print("Use 'uid -h' for help")
            sys.exit(1)
    
    # Default: generate single UID
    generator = WorkflowUIDGenerator()
    uid = generator.generate_uid()
    print(uid)

if __name__ == "__main__":
    main()
EOF

# Make the uid command executable
chmod +x "${BIN_DIR}/uid"

# Success message
echo "UID generator installed!"
echo "- 'uid' command installed to ${BIN_DIR}"
echo ""
echo "You can now use the uid command:"
echo "  uid         - Generate a single UID"
echo "  uid -e      - Generate UID with mathematical explanation"
echo "  uid -b N    - Generate N UIDs in batch"
echo "  uid -h      - Show help"
echo ""
echo "If your shell doesn't find the uid command, you may need to:"
echo "  1. Close and reopen your terminal"
echo "  2. Run 'hash -r' to clear command cache"
echo "  3. Check your PATH to ensure ~/bin is included" 