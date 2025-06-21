import hashlib

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

# Convenience functions
def generate_user_id(username):
    """Quick function to generate a user ID"""
    generator = UserIDGenerator()
    user_id, _ = generator.generate_user_id(username)
    return user_id

def generate_user_id_with_explanation(username):
    """Generate user ID with explanation"""
    generator = UserIDGenerator()
    return generator.generate_with_explanation(username)

# Test the generator
if __name__ == "__main__":
    generator = UserIDGenerator()
    
    test_usernames = ["seanivore", "alice", "bob123", "developer", "user"]
    
    print("User ID Generator Test:")
    print("======================")
    
    for username in test_usernames:
        try:
            user_id, explanation = generator.generate_with_explanation(username)
            print(f"\n{explanation}")
        except ValueError as e:
            print(f"\nError for '{username}': {e}")
    
    print("\n" + "="*50)
    print("Testing consistency (same username should give same ID):")
    for username in ["seanivore", "alice"]:
        ids = [generate_user_id(username) for _ in range(3)]
        print(f"{username}: {ids[0]} (consistent: {all(id == ids[0] for id in ids)})") 