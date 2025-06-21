#!/bin/bash
# Install script for the standalone user ID generator command

# Set paths
BIN_DIR="${HOME}/bin"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Save the meid script to bin directory
echo "Creating meid command in ${BIN_DIR}..."
cat > "${BIN_DIR}/meid" << 'EOF'
#!/usr/bin/env python3
"""
Self-contained user ID generator command-line tool
Usage:
    meid username       - Generate user ID for username
    meid -e username    - Generate user ID with explanation
    meid -h             - Show help
"""

import sys

class UserIDGenerator:
    """
    Generates deterministic user IDs in format: user-####
    - Uses character count and doubled count as base numbers
    - Applies mathematical operations for uniqueness
    - Same username always produces same user ID
    - Format: user-1234 (4 digits)
    """
    
    def __init__(self):
        # Mathematical operations similar to workflow IDs
        self.operations = {
            'add': lambda x, y: x + y,
            'multiply': lambda x, y: (x * y) % 10000,
            'fibonacci': lambda x, y: self._fib_mod(x + y),
            'golden': lambda x, y: int((x + y) * 1.618) % 10000,
            'spiral': lambda x, y: (x * 7 + y * 13) % 10000,
            'mirror': lambda x, y: self._mirror_add(x, y),
            'karmic': lambda x, y: (self._digit_sum(x) * 37 + self._digit_sum(y) * 23) % 10000,
        }
    
    def _fib_mod(self, n):
        """Fibonacci-like operation limited to 4 digits"""
        if n <= 1:
            return n % 10000
        a, b = 0, 1
        for _ in range(min(n % 15, 12)):  # Limit iterations
            a, b = b, (a + b) % 10000
        return b
    
    def _mirror_add(self, x, y):
        """Add numbers with their digit reversals"""
        x_str = str(x)
        y_str = str(y)
        x_rev = int(x_str[::-1]) if x_str[::-1].isdigit() else x
        y_rev = int(y_str[::-1]) if y_str[::-1].isdigit() else y
        return (x + x_rev + y + y_rev) % 10000
    
    def _digit_sum(self, n):
        """Sum of digits in a number"""
        return sum(int(d) for d in str(n))
    
    def generate_user_id(self, username):
        """Generate a deterministic user ID from username"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        # Clean username - only letters and numbers
        clean_username = ''.join(c.lower() for c in username if c.isalnum())
        if not clean_username:
            raise ValueError("Username must contain at least one letter or number")
        
        # Base numbers: character count and doubled
        char_count = len(clean_username)
        doubled_count = char_count * 2
        
        # Add ASCII values for more uniqueness
        ascii_sum = sum(ord(c) for c in clean_username)
        
        # Choose operations based on username characteristics
        operation_choices = []
        
        # Use first character to pick primary operation
        first_char_value = ord(clean_username[0]) % len(self.operations)
        operation_names = list(self.operations.keys())
        primary_op = operation_names[first_char_value]
        
        # Use last character for secondary operation
        last_char_value = ord(clean_username[-1]) % len(self.operations)
        secondary_op = operation_names[last_char_value]
        
        # Apply primary operation with base numbers
        result = self.operations[primary_op](char_count, doubled_count)
        
        # Apply secondary operation with ASCII sum
        result = self.operations[secondary_op](result, ascii_sum % 1000)
        
        # Ensure we have exactly 4 digits
        final_number = abs(result) % 10000
        
        # Ensure it's not 0000
        if final_number == 0:
            final_number = (ascii_sum + char_count) % 9999 + 1
        
        user_id = f"user-{final_number:04d}"
        
        return user_id, {
            'username': username,
            'clean_username': clean_username,
            'char_count': char_count,
            'doubled_count': doubled_count,
            'ascii_sum': ascii_sum,
            'primary_operation': primary_op,
            'secondary_operation': secondary_op,
            'final_number': final_number
        }
    
    def generate_with_explanation(self, username):
        """Generate user ID with detailed explanation"""
        user_id, details = self.generate_user_id(username)
        
        explanation = (
            f"Username '{details['username']}' -> {user_id}\n"
            f"Steps: {details['char_count']} chars -> doubled to {details['doubled_count']} -> "
            f"ASCII sum {details['ascii_sum']} -> {details['primary_operation']}+{details['secondary_operation']} -> "
            f"{details['final_number']:04d}"
        )
        
        return user_id, explanation

def main():
    if len(sys.argv) < 2:
        print("meid - Generate user IDs from usernames")
        print("")
        print("Usage:")
        print("  meid username       Generate user ID for username")
        print("  meid -e username    Generate user ID with explanation")
        print("  meid -h             Show this help")
        print("")
        print("Examples:")
        print("  meid seanivore      # user-1642")
        print("  meid -e alice       # user-1161 | Steps: 5 chars -> ...")
        print("")
        print("Mathematical Operations:")
        print("  Uses character count, doubled count, and ASCII values")
        print("  Applies fibonacci, golden ratio, spiral, mirror, karmic operations")
        print("  Same username always produces the same user ID")
        return
    
    arg = sys.argv[1].lower()
    
    if arg in ['-h', '--help', 'help']:
        main()  # Show help
        return
    
    elif arg in ['-e', '--explain', 'explain']:
        if len(sys.argv) < 3:
            print("Error: Please provide a username")
            print("Usage: meid -e username")
            sys.exit(1)
        
        username = sys.argv[2]
        generator = UserIDGenerator()
        try:
            user_id, explanation = generator.generate_with_explanation(username)
            print(f"{user_id} | {explanation}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    else:
        # First argument is the username
        username = sys.argv[1]
        generator = UserIDGenerator()
        try:
            user_id, _ = generator.generate_user_id(username)
            print(user_id)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
EOF

# Make the meid command executable
chmod +x "${BIN_DIR}/meid"

# Success message
echo "User ID generator installed!"
echo "- 'meid' command installed to ${BIN_DIR}"
echo ""
echo "You can now use the meid command:"
echo "  meid username       Generate user ID for username"
echo "  meid -e username    Generate user ID with explanation"
echo "  meid -h             Show help"
echo ""
echo "Examples:"
echo "  meid seanivore      # user-1642"
echo "  meid -e alice       # Shows mathematical steps"
echo ""
echo "Perfect for MAO welcome screen user registration!" 