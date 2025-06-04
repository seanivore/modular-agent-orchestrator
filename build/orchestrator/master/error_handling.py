"""
SFA v4.0.0 Shared Error Handling
Professional error handling patterns for all tools
"""

import time
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import traceback


class SFAError(Exception):
    """Base exception for SFA v4 tools"""
    def __init__(self, message: str, error_code: str = "SFA_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)


class ValidationError(SFAError):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        details = {"field": field, "value": str(value) if value is not None else None}
        super().__init__(message, "VALIDATION_ERROR", details)


class ProcessingError(SFAError):
    """Raised when tool processing fails"""
    def __init__(self, message: str, operation: str = None, stage: str = None):
        details = {"operation": operation, "stage": stage}
        super().__init__(message, "PROCESSING_ERROR", details)


class ResourceError(SFAError):
    """Raised when resource access fails"""
    def __init__(self, message: str, resource_type: str = None, resource_path: str = None):
        details = {"resource_type": resource_type, "resource_path": resource_path}
        super().__init__(message, "RESOURCE_ERROR", details)


class APIError(SFAError):
    """Raised when external API calls fail"""
    def __init__(self, message: str, api_name: str = None, status_code: int = None):
        details = {"api_name": api_name, "status_code": status_code}
        super().__init__(message, "API_ERROR", details)


def handle_errors(operation_name: str = "operation", 
                 return_dict: bool = True,
                 log_errors: bool = True) -> Callable:
    """
    Decorator for comprehensive error handling with professional patterns
    
    Args:
        operation_name: Name of the operation for error context
        return_dict: Whether to return error as dict (True) or raise (False)
        log_errors: Whether to log errors
        
    Returns:
        Decorated function with error handling
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except SFAError as e:
                # Handle known SFA errors
                error_info = {
                    "error": e.message,
                    "error_code": e.error_code,
                    "operation": operation_name,
                    "timestamp": e.timestamp,
                    "details": e.details
                }
                
                if log_errors:
                    logging.error(f"SFA Error in {operation_name}: {e.message}", extra=e.details)
                
                if return_dict:
                    return error_info
                else:
                    raise
            
            except FileNotFoundError as e:
                # Handle file/resource errors
                error_info = {
                    "error": f"File not found: {str(e)}",
                    "error_code": "FILE_NOT_FOUND",
                    "operation": operation_name,
                    "timestamp": datetime.now().isoformat(),
                    "details": {"file_path": str(e).split("'")[1] if "'" in str(e) else str(e)}
                }
                
                if log_errors:
                    logging.error(f"File not found in {operation_name}: {str(e)}")
                
                if return_dict:
                    return error_info
                else:
                    raise ResourceError(f"File not found: {str(e)}", "file", str(e))
            
            except PermissionError as e:
                # Handle permission errors
                error_info = {
                    "error": f"Permission denied: {str(e)}",
                    "error_code": "PERMISSION_DENIED",
                    "operation": operation_name,
                    "timestamp": datetime.now().isoformat(),
                    "details": {"resource": str(e)}
                }
                
                if log_errors:
                    logging.error(f"Permission denied in {operation_name}: {str(e)}")
                
                if return_dict:
                    return error_info
                else:
                    raise ResourceError(f"Permission denied: {str(e)}", "permission", str(e))
            
            except Exception as e:
                # Handle unexpected errors
                error_info = {
                    "error": f"Unexpected error: {str(e)}",
                    "error_code": "UNEXPECTED_ERROR",
                    "operation": operation_name,
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc() if log_errors else None
                    }
                }
                
                if log_errors:
                    logging.error(f"Unexpected error in {operation_name}: {str(e)}", exc_info=True)
                
                if return_dict:
                    return error_info
                else:
                    raise ProcessingError(f"Unexpected error: {str(e)}", operation_name)
        
        return wrapper
    return decorator


def retry_with_backoff(max_retries: int = 3,
                      base_delay: float = 1.0,
                      max_delay: float = 60.0,
                      backoff_factor: float = 2.0,
                      exceptions: tuple = (Exception,)) -> Callable:
    """
    Decorator for retry logic with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to retry on
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        # Final attempt failed
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    
                    logging.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s: {str(e)}")
                    time.sleep(delay)
            
            # All retries exhausted
            raise last_exception
        
        return wrapper
    return decorator


def validate_parameters(params: Dict[str, Any], 
                       required_fields: list = None,
                       field_types: Dict[str, type] = None,
                       field_validators: Dict[str, Callable] = None) -> Dict[str, Any]:
    """
    Comprehensive parameter validation with detailed error reporting
    
    Args:
        params: Parameters to validate
        required_fields: List of required field names
        field_types: Dict mapping field names to expected types
        field_validators: Dict mapping field names to validation functions
        
    Returns:
        Validated parameters dict
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(params, dict):
        raise ValidationError("Parameters must be a dictionary", "params", type(params))
    
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in params:
                raise ValidationError(f"Required field missing: {field}", field, None)
            
            if params[field] is None:
                raise ValidationError(f"Required field cannot be None: {field}", field, None)
    
    # Check field types
    if field_types:
        for field, expected_type in field_types.items():
            if field in params and params[field] is not None:
                if not isinstance(params[field], expected_type):
                    raise ValidationError(
                        f"Field {field} must be of type {expected_type.__name__}, got {type(params[field]).__name__}",
                        field, 
                        params[field]
                    )
    
    # Run custom validators
    if field_validators:
        for field, validator in field_validators.items():
            if field in params and params[field] is not None:
                try:
                    if not validator(params[field]):
                        raise ValidationError(f"Field {field} failed validation", field, params[field])
                except Exception as e:
                    raise ValidationError(f"Validation error for field {field}: {str(e)}", field, params[field])
    
    return params


def safe_file_operation(operation: Callable, 
                       file_path: str,
                       operation_name: str = "file operation",
                       create_dirs: bool = False) -> Any:
    """
    Safely execute file operations with comprehensive error handling
    
    Args:
        operation: Function to execute (should take file_path as first arg)
        file_path: Path to file
        operation_name: Name of operation for error context
        create_dirs: Whether to create parent directories if they don't exist
        
    Returns:
        Result of operation
        
    Raises:
        ResourceError: If file operation fails
    """
    try:
        # Create parent directories if requested
        if create_dirs:
            import os
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        return operation(file_path)
    
    except FileNotFoundError:
        raise ResourceError(f"File not found for {operation_name}: {file_path}", "file", file_path)
    
    except PermissionError:
        raise ResourceError(f"Permission denied for {operation_name}: {file_path}", "permission", file_path)
    
    except OSError as e:
        raise ResourceError(f"OS error during {operation_name}: {str(e)}", "os", file_path)
    
    except Exception as e:
        raise ProcessingError(f"Unexpected error during {operation_name}: {str(e)}", operation_name, "file_operation")


def graceful_degradation(fallback_value: Any = None,
                        fallback_function: Callable = None,
                        log_fallback: bool = True) -> Callable:
    """
    Decorator for graceful degradation when operations fail
    
    Args:
        fallback_value: Value to return if operation fails
        fallback_function: Function to call if operation fails
        log_fallback: Whether to log when fallback is used
        
    Returns:
        Decorated function with graceful degradation
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                if log_fallback:
                    logging.warning(f"Operation {func.__name__} failed, using fallback: {str(e)}")
                
                if fallback_function:
                    try:
                        return fallback_function(*args, **kwargs)
                    except Exception as fallback_error:
                        if log_fallback:
                            logging.error(f"Fallback function also failed: {str(fallback_error)}")
                        return fallback_value
                
                return fallback_value
        
        return wrapper
    return decorator


def format_error_for_ui(error_info: Dict[str, Any], verbose: bool = False) -> str:
    """
    Format error information for user-friendly display
    
    Args:
        error_info: Error information dictionary
        verbose: Whether to include detailed information
        
    Returns:
        Formatted error message
    """
    if not isinstance(error_info, dict) or "error" not in error_info:
        return "Unknown error occurred"
    
    message = f"❌ {error_info['error']}"
    
    if verbose:
        if "error_code" in error_info:
            message += f"\n   Code: {error_info['error_code']}"
        
        if "operation" in error_info:
            message += f"\n   Operation: {error_info['operation']}"
        
        if "timestamp" in error_info:
            message += f"\n   Time: {error_info['timestamp']}"
        
        if "details" in error_info and error_info["details"]:
            details = error_info["details"]
            for key, value in details.items():
                if value is not None and key != "traceback":
                    message += f"\n   {key.title()}: {value}"
    
    return message


def estimate_operation_cost(operation_type: str, 
                          complexity_factor: float = 1.0,
                          base_costs: Dict[str, float] = None) -> float:
    """
    Estimate cost for operations with error handling overhead
    
    Args:
        operation_type: Type of operation
        complexity_factor: Multiplier for operation complexity
        base_costs: Dict of base costs per operation type
        
    Returns:
        Estimated cost including error handling overhead
    """
    if base_costs is None:
        base_costs = {
            "file_operation": 0.001,
            "api_call": 0.01,
            "processing": 0.005,
            "validation": 0.0001
        }
    
    base_cost = base_costs.get(operation_type, 0.005)
    
    # Add small overhead for error handling
    error_handling_overhead = 0.0001
    
    return (base_cost * complexity_factor) + error_handling_overhead


# Configure logging for SFA v4
def setup_sfa_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Set up logging configuration for SFA v4 tools
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        filename=log_file
    )
    
    # Add console handler if logging to file
    if log_file:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(console_handler) 