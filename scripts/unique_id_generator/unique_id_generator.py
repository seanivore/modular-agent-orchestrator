import time
from datetime import datetime
import hashlib
import random
from typing import Dict, Any, Tuple, List

# Standard Mao imports (with fallback for standalone usage)
try:
    from orchestrator.cache.cache_system import CacheManager
    from orchestrator.error_handling import handle_errors
from pathlib import Path
    MAO_AVAILABLE = True
except ImportError:
    # Fallback for standalone usage outside Mao environment
    MAO_AVAILABLE = False
    CacheManager = None
    def handle_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

def estimate_cost(generation_params: Dict[str, Any] = None) -> Dict[str, float]:
    """
    Estimate computational cost for UID generation operations
    
    Args:
        generation_params: Parameters affecting generation complexity
        
    Returns:
        Dict with cost estimates (time, memory, operations)
    """
    generation_params = generation_params or {}
    
    batch_size = generation_params.get('batch_size', 1)
    include_explanation = generation_params.get('include_explanation', False)
    mathematical_complexity = generation_params.get('mathematical_complexity', 'standard')
    
    # Base cost per UID generation
    base_time_per_uid = 0.001  # Very fast generation
    base_memory_per_uid = 256  # bytes for string storage
    math_operations_per_uid = 3  # One operation per letter
    
    # Apply batch multiplier
    total_time = base_time_per_uid * batch_size
    total_memory = base_memory_per_uid * batch_size
    total_operations = math_operations_per_uid * batch_size
    
    # Apply explanation overhead
    if include_explanation:
        total_time *= 1.2
        total_memory *= 1.5  # Store operation logs
    
    # Apply complexity multiplier
    complexity_multipliers = {
        'simple': 0.8,
        'standard': 1.0,
        'complex': 1.3
    }
    multiplier = complexity_multipliers.get(mathematical_complexity, 1.0)
    
    total_time *= multiplier
    total_operations = int(total_operations * multiplier)
    
    return {
        'estimated_time_seconds': round(total_time, 4),
        'estimated_memory_bytes': int(total_memory),
        'estimated_math_operations': total_operations,
        'complexity_score': min(10, batch_size  /  100)  # 1-10 scale
    }

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
        
        # Mao integrations  
        self.cache = CacheManager() if CacheManager else None
        # Map letters to mathematical operations
        self.letter_operations = {
            'a': ('add', lambda x: x + 17),
            'b': ('multiply', lambda x: x * 3),
            'c': ('subtract', lambda x: abs(x - 23)),
            'd': ('divide', lambda x: x / /  2 if x > 0 else 1),
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
            't': ('triangle', lambda x: (x * (x + 1) / /  2) % 1000),
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
    
    @handle_errors(operation_name="uid_generation", return_dict=False)
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
            (current_timestamp + now.day + microseconds / /  10000) % 26,
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

# Convenience function for single use
def generate_workflow_uid():
    """Quick function to generate a single UID"""
    generator = WorkflowUIDGenerator()
    return generator.generate_uid()

def generate_workflow_uid_with_explanation():
    """Generate UID with mathematical explanation"""
    generator = WorkflowUIDGenerator()
    return generator.generate_with_explanation()

# Test the generator
if __name__ == "__main__":
    generator = WorkflowUIDGenerator()
    
    print("Sample UIDs with Mathematical Operations:")
    for i in range(10):
        uid, explanation = generator.generate_with_explanation()
        print(f"  {uid} | Math: {explanation}")
        # Small delay to show time-based variation
        time.sleep(0.001)
    
    print(f"\nLetter Operations Available: {len(generator.letter_operations)}")
    print("Sample operations:")
    for letter, (name, _) in list(generator.letter_operations.items())[:5]:
        print(f"  {letter} = {name}")
    
    print(r"\nBatch generation (rapid fire):")
    batch = generator.generate_batch(5)
    for uid in batch:
        print(f"  {uid}") 