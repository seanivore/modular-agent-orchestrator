# UserManager Documentation

## Overview

The `UserManager` class implements Mao's UserID-first architecture as specified in MAO_FLOW.md. This system uses Account IDs (email or phone numbers) as the primary unique identifier, generating deterministic UserIDs in the format `user-####` for directory organization and internal references.

## Architecture Philosophy

### UserID-First Design
The system prioritizes UserID as the internal identifier while maintaining Account ID as the human-facing unique key. This approach ensures:

- **Consistency**: Same Account ID always generates the same UserID
- **Uniqueness**: Account IDs guarantee user uniqueness by design
- **Organization**: UserID-based directories create clean file system structure
- **Privacy**: UserIDs can be shared internally without exposing personal Account IDs

### Directory Structure

```
configs/user/
├── user-1234/           # UserID-based directory naming
│   ├── user-1234.json   # User profile with Account ID and metadata
│   ├── memories/        # User memory storage
│   └── analytics/       # User analytics data
└── user-5678/
    ├── user-5678.json
    ├── memories/
    └── analytics/
```

## Core Methods

### User Creation

#### `create_user(account_id: str, first_name: str = "", last_name: str = "", metadata: Dict[str, Any] = None) -> Dict[str, Any]`

Creates a new user with UserID generated from Account ID. The Account ID must be a valid email or phone number.

**Process:**
1. Validates and normalizes Account ID format
2. Checks for existing users with same Account ID
3. Generates deterministic UserID using internal mapping (TODO: replace with meid script)
4. Creates UserID-based directory structure
5. Saves user data and establishes session

**Example:**
```python
manager = UserManager()
result = manager.create_user(
    account_id="sean@example.com",
    first_name="Sean",
    last_name="Developer",
    metadata={"role": "admin"}
)
# Returns: {"success": True, "user_data": {"user_id": "user-5253", ...}}
```

### User Lookup

#### `get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]`

Loads user data by UserID. This is the most efficient lookup method for internal operations.

#### `find_user_by_account_id(account_id: str) -> Optional[Dict[str, Any]]`

Finds user by Account ID (email or phone). This is the primary method for user discovery and authentication workflows.

**Process:**
1. Normalizes Account ID format
2. Checks cache for Account ID → UserID mapping
3. Falls back to scanning user directories if not cached
4. Caches successful mappings for future lookups

### User Management

#### `update_user_settings(user_id: str, settings_changes: Dict[str, Any]) -> Dict[str, Any]`

Updates user settings with delta-only storage. Only settings that differ from application defaults are stored, minimizing file size and maintaining clean user profiles.

#### `list_users() -> List[Dict[str, Any]]`

Returns all users from UserID-based directories. Validates directory names match UserID format before processing.

#### `search_users(search_term: str) -> List[Dict[str, Any]]`

Comprehensive user search across UserID, Account ID, and name fields. Prioritizes exact Account ID matches before performing broader search.

## Session Management

### `set_session_user(user_id: str) -> Dict[str, Any]`

Establishes user session using UserID. Updates user's last login timestamp and creates session state file.

### `get_session_user() -> Optional[Dict[str, Any]]`

Retrieves current session user data. Validates session integrity and cleans up invalid sessions automatically.

## Account ID Processing

### Email Validation
Supports standard email formats with regex validation:
- Alphanumeric characters, dots, underscores, plus signs, hyphens
- Valid domain format with TLD
- Case-insensitive processing

### Phone Number Normalization
Processes phone numbers by:
- Removing all non-digit characters (spaces, hyphens, parentheses)
- Validating length between 10-15 digits
- Storing as digit-only string for consistency

## UserID Generation

### Current Implementation
The system currently uses MD5 hashing of the Account ID to generate deterministic 4-digit UserIDs:

```python
def _generate_user_id_from_account_id(self, account_id: str) -> str:
    hash_object = hashlib.md5(account_id.encode())
    # Extract digits and create 4-digit number
    return f"user-{user_number:04d}"
```

### Future Implementation
This will be replaced with the actual `meid` script integration as specified in MAO_FLOW.md for production deployment.

## Cache Integration

The system implements dual caching strategies:

- **User Data Cache**: `user_data_{user_id}` → Full user profile
- **Account Mapping Cache**: `account_to_userid_{account_id}` → UserID for fast lookup

This reduces file system operations and improves performance for repeated lookups.

## Error Handling

All public methods use the `@handle_errors` decorator with appropriate error types:

- **ValueError**: Invalid input format (empty Account ID, invalid email/phone)
- **APIError**: System errors (UserID generation failure, file operations)

Methods return consistent dictionary responses with `success` boolean and descriptive `message` fields.

## Backward Compatibility

### Deprecated Methods
- `load_user(username)` → Use `find_user_by_account_id(account_id)`
- `find_user(search_term)` → Use `search_users(search_term)`

These methods remain available during transition but will be removed in future versions.

## Integration Points

### Memory MCP
User data integrates with Memory MCP using UserID as the primary entity identifier:
- User profiles stored as entities
- Account IDs stored as searchable observations
- Session context maintained through UserID references

### Analytics System
User analytics reference UserID for data organization:
- Cost tracking by UserID
- Session metrics tied to UserID
- Workflow history organized by UserID

### CLI Commands
Supports MAO_FLOW.md specified slash commands:
- `/user user-1234` - Switch to specific UserID
- `/my-memories` - Access current user's memories
- `/view-user` - Display current user profile

## Development Guidelines

### Creating New User Operations
1. Always use UserID as primary parameter for internal operations
2. Provide Account ID lookup methods for user-facing operations
3. Implement proper input validation and normalization
4. Use caching for performance optimization
5. Follow delta-only storage for settings updates

### Testing Considerations
- Test Account ID normalization with various email/phone formats
- Verify UserID consistency (same Account ID → same UserID)
- Validate directory structure creation and file naming
- Test cache invalidation and session management

## Security Considerations

### Account ID Privacy
- Account IDs stored in user files but not exposed in directory names
- UserIDs provide internal reference without revealing personal information
- Session files contain both UserID and Account ID for verification

### Input Validation
- Account ID format validation prevents injection attacks
- UserID format validation ensures consistent internal references
- File path validation prevents directory traversal

## Performance Characteristics

### Time Complexity
- User creation: O(1) with successful Account ID validation
- UserID lookup: O(1) with caching, O(n) cold cache
- Account ID lookup: O(1) with caching, O(n) cold cache scanning
- User listing: O(n) where n = number of users

### Space Complexity
- Per-user storage: Minimal with delta-only settings
- Cache overhead: Proportional to active users
- Directory structure: Linear growth with user base

## Migration Strategy

### From Username-Based System
1. Identify existing username-based user directories
2. Extract Account ID from user files (email field)
3. Generate UserID from Account ID
4. Migrate directories from `username/` to `user-####/`
5. Update file names from `user_username.json` to `user-####.json`
6. Update cache keys to UserID format
7. Preserve all user data during migration

This migration maintains data integrity while transitioning to the new architecture specified in MAO_FLOW.md.