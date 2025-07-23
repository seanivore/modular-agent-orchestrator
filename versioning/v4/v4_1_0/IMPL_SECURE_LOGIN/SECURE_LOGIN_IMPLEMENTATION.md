# Section 4.1.0: Secure Email-Based Login with Passkey Integration
*Implementing modern authentication with emotional UX intelligence and seamless user experience*

---

## Implementation Overview

The MAO v4.1.0 secure login system transforms authentication from username-based to email-based with passkey integration, enabling unique user identification, subscription management, hosted API key storage, and emotional UX intelligence. This implementation eliminates duplicate user issues while providing the smooth, memorable authentication experience demonstrated by modern platforms like Porkbun.

---

## Core Authentication Architecture

### Email-as-Username System
Instead of traditional usernames that can cause duplicates, the system uses email addresses as the primary user identifier while maintaining the deterministic UserID system for analytics anonymization.

**Why Email-Based Authentication:**
- **Natural Uniqueness**: Email addresses are inherently unique
- **Subscription Ready**: Already required for payment processing
- **Modern UX Standard**: Users expect email-based login in 2025
- **Passkey Compatible**: Email addresses work seamlessly with passkey protocols
- **API Key Management**: Enables hosted credential management through web interface

### Passkey Integration Strategy
Aggressively passkey-first approach. Passwords are digital archaeology - it's 2025, users should use modern authentication.

**Passkey-First UX Flow:**
1. User enters email address
2. System checks for existing passkey credentials
3. If passkey exists: authenticate with biometrics/PIN
4. If no passkey: guide user through passkey setup
5. **No password fallback**: Help users set up passkeys instead
6. Seamless mobile experience with Touch ID/Face ID/fingerprint

**Philosophy: Passkeys or Passkeys**
Every device manufactured in the last 5 years has biometric authentication. Users shouldn't need to remember `P@ssw0rd123!` like it's 1995. We help users embrace modern security instead of enabling digital archaeology.

### UserID Generation from Email
The existing mathematical UserID generation system adapts perfectly to email input instead of username input, maintaining all existing functionality while solving the duplicate problem.

**Email → UserID Process:**
- Email address replaces username as input to `generate_user_id()`
- Same deterministic mathematical operations apply
- Same `user-####` format maintained
- Same anonymization layer for analytics
- Backwards compatible with existing UserID system

---

## Technical Implementation Details

### Database Schema Modifications

**Current User Data Structure:**
```json
{
  "username": "seanivore",
  "user_id": "user-1642", 
  "first_name": "Sean",
  "last_name": "Horvath",
  "email": "sean@august.style",
  "dob": "1987-07-21",
  "created_at": "2025-06-26T04:28:05.688803",
  "last_login": "2025-06-26T04:28:05.688809"
}
```

**Updated User Data Structure:**
```json
{
  "email": "sean@august.style",
  "user_id": "user-1642",
  "first_name": "Sean", 
  "last_name": "Horvath",
  "display_name": "Sean",
  "passkey_enabled": true,
  "passkey_credential_id": "credential_abc123",
  "subscription_tier": "pro",
  "api_keys": {
    "anthropic": "encrypted_key_data",
    "openai": "encrypted_key_data"
  },
  "created_at": "2025-06-26T04:28:05.688803",
  "last_login": "2025-06-26T04:28:05.688809"
}
```

### Authentication Flow Architecture

**Login Process Flow:**
1. **Email Entry**: User enters email address in login form
2. **Account Lookup**: System searches for existing account by email
3. **Authentication Method Detection**: System checks available auth methods
4. **Passkey First**: If passkey available, attempt passkey authentication
5. **Password Fallback**: If passkey fails/unavailable, show password field
6. **Session Creation**: Generate secure session with UserID anonymization
7. **Context Loading**: Load user settings, workflows, and session state

**Registration Process Flow:**
1. **Email Validation**: Verify email format and availability in real-time
2. **Bot Protection**: Cloudflare Turnstile verification (elegant, no clicking bikes!)
3. **User Details**: Collect first name, optional last name, display preferences
4. **Instant Account Creation**: Create account immediately (no annoying email verification!)
5. **UserID Generation**: Generate deterministic UserID from email
6. **Passkey Setup**: Strongly encourage passkey enrollment for security
7. **Welcome Flow**: Initialize default settings and onboarding with AI greeting

### File System Adaptations

**Current Directory Structure:**
```
configs/user/seanivore/
├── user_seanivore.json
├── memories/
└── analytics/
```

**Updated Directory Structure:**
```
configs/user/sean_august_style/  # Email converted to filesystem-safe format
├── user_sean_august_style.json
├── memories/
├── analytics/
└── credentials/
    ├── api_keys.encrypted
    └── passkey_data.json
```

### Username Manager Modifications

**Key Changes Required:**

1. **Email Parameter Replacement**:
   - Replace `username` parameter with `email` in all methods
   - Update function signatures: `create_user(email, first_name, last_name)`
   - Maintain backwards compatibility during transition

2. **UserID Generation Update**:
   - Update call to `generate_user_id(email)` instead of `generate_user_id(username)`
   - Email preprocessing for mathematical consistency
   - Validation for email format before UserID generation

3. **Directory Path Conversion**:
   - Convert email to filesystem-safe directory name
   - Handle special characters (@ → _at_, . → _dot_)
   - Example: `sean@august.style` → `sean_at_august_dot_style`

4. **Session Management**:
   - Update session data to use email as primary identifier
   - Maintain UserID for analytics anonymization
   - Store display preferences for personalized greetings

### Passkey Integration Implementation

**WebAuthn Integration:**
```javascript
// Passkey Registration
async function registerPasskey(email, displayName) {
    const publicKeyCredentialCreationOptions = {
        challenge: generateChallenge(),
        rp: {
            name: "Modular Agent Orchestrator",
            id: "mao.app"
        },
        user: {
            id: stringToArrayBuffer(email),
            name: email,
            displayName: displayName || email.split('@')[0]
        },
        pubKeyCredParams: [
            {alg: -7, type: "public-key"},
            {alg: -257, type: "public-key"}
        ],
        authenticatorSelection: {
            authenticatorAttachment: "platform",
            userVerification: "required"
        },
        timeout: 60000,
        attestation: "direct"
    };
    
    const credential = await navigator.credentials.create({
        publicKey: publicKeyCredentialCreationOptions
    });
    
    return credential;
}

// Passkey Authentication  
async function authenticatePasskey(email) {
    const publicKeyCredentialRequestOptions = {
        challenge: generateChallenge(),
        allowCredentials: await getCredentialsForEmail(email),
        timeout: 60000,
        userVerification: "required"
    };
    
    const assertion = await navigator.credentials.get({
        publicKey: publicKeyCredentialRequestOptions
    });
    
    return assertion;
}
```

**Backend Verification:**
```python
# Passkey Verification System
class PasskeyManager:
    def __init__(self):
        self.rp_id = "mao.app"
        self.rp_name = "Modular Agent Orchestrator"
    
    def verify_registration(self, email: str, credential_data: dict) -> bool:
        """Verify passkey registration and store credential"""
        try:
            # Verify WebAuthn registration
            verification = verify_registration_response(
                credential=credential_data,
                expected_challenge=self.get_challenge(email),
                expected_origin="https://mao.app",
                expected_rp_id=self.rp_id
            )
            
            if verification.verified:
                # Store credential data
                self.store_credential(email, verification.credential_data)
                return True
            return False
        except Exception as e:
            logger.error(f"Passkey registration failed: {e}")
            return False
    
    def verify_authentication(self, email: str, assertion_data: dict) -> bool:
        """Verify passkey authentication"""
        try:
            stored_credential = self.get_credential(email)
            if not stored_credential:
                return False
            
            verification = verify_authentication_response(
                credential=assertion_data,
                expected_challenge=self.get_challenge(email),
                expected_origin="https://mao.app",
                expected_rp_id=self.rp_id,
                credential_public_key=stored_credential['public_key'],
                credential_current_sign_count=stored_credential['sign_count']
            )
            
            if verification.verified:
                # Update sign count
                self.update_sign_count(email, verification.new_sign_count)
                return True
            return False
        except Exception as e:
            logger.error(f"Passkey authentication failed: {e}")
            return False
```

---

## Emotional UX Intelligence Integration

### Contextual Status Words <-- **HARDCODED OPTIONS INSTEAD OF AI IMPROV?!**
Implementing the "budgeting," "celebrating," "flibbergitting" concept throughout the authentication and session experience.

**Status Word Generation System:**
```python
class EmotionalUXManager:
    def __init__(self):
        self.status_contexts = {
            "login": ["authenticating", "welcoming", "recognizing", "greeting"],
            "processing": ["pondering", "calculating", "orchestrating", "weaving"],
            "working": ["crafting", "building", "creating", "developing"],
            "analyzing": ["investigating", "discovering", "exploring", "understanding"],
            "celebrating": ["rejoicing", "cheering", "applauding", "beaming"],
            "waiting": ["patience-ing", "zen-ing", "mellowing", "breathing"],
            "error": ["troubleshooting", "problem-solving", "debugging", "untangling"]
        }
        
        self.whimsical_variants = [
            "flibbergitting", "wonderfying", "magnificating", "brilliantizing",
            "spectacularizing", "amazifying", "incredibleating", "fantasticizing"
        ]
    
    def get_contextual_status(self, operation: str, user_context: dict = None) -> str:
        """Generate contextually relevant status word"""
        context_key = self._determine_context(operation, user_context)
        
        # 80% contextual, 20% whimsical for surprise and delight
        if random.random() < 0.8:
            return random.choice(self.status_contexts.get(context_key, ["working"]))
        else:
            return random.choice(self.whimsical_variants)
    
    def _determine_context(self, operation: str, user_context: dict) -> str:
        """Determine appropriate context based on operation and user state"""
        if "login" in operation.lower():
            return "login"
        elif "error" in operation.lower():
            return "error"
        elif user_context and user_context.get("recent_success"):
            return "celebrating"
        elif "analyze" in operation.lower():
            return "analyzing"
        else:
            return "processing"
```

### AI-Generated Personalized Greeting System <-- **Ah ha I see**
```python
class AIPersonalizedGreetingManager:
    def __init__(self):
        self.llm_client = AnthropicClient()  # or whatever LLM client
        self.context_analyzer = UserContextAnalyzer()
        
    async def generate_greeting(self, user_data: dict, session_context: dict = None) -> str:
        """Generate completely novel, AI-powered contextual greeting every time"""
        
        # Gather contextual information
        context = self._build_greeting_context(user_data, session_context)
        
        # Create dynamic prompt for AI greeting generation
        prompt = self._build_greeting_prompt(context)
        
        # Generate novel greeting with AI
        greeting = await self.llm_client.generate_text(
            prompt=prompt,
            max_tokens=50,
            temperature=0.8,  # Higher creativity for novel responses
            stop_sequences=["\n", ".", "!"]
        )
        
        return greeting.strip()
    
    def _build_greeting_context(self, user_data: dict, session_context: dict) -> dict:
        """Build rich context for AI greeting generation"""
        name = user_data.get("display_name") or user_data.get("first_name") or "friend"
        
        context = {
            "user_name": name,
            "time_of_day": self._get_time_context(),
            "day_of_week": datetime.now().strftime("%A"),
            "season": self._get_season(),
            "last_activity": user_data.get("last_activity_type"),
            "recent_success": session_context.get("recent_success") if session_context else None,
            "user_mood_indicators": self._analyze_recent_interactions(user_data),
            "current_weather_vibe": self._get_weather_context(),  # Optional: weather API
            "user_timezone": user_data.get("timezone", "UTC"),
            "workflow_count": session_context.get("active_workflows", 0) if session_context else 0
        }
        
        return context
    
    def _build_greeting_prompt(self, context: dict) -> str:
        """Build dynamic prompt for AI to generate novel greeting"""
        return f"""Generate a warm, creative, and contextually relevant greeting for {context['user_name']}.

Context:
- Time: {context['time_of_day']} on {context['day_of_week']}
- Season: {context['season']}
- Recent activity: {context.get('last_activity', 'first visit today')}
- Mood indicators: {context.get('user_mood_indicators', 'neutral')}
- Active workflows: {context.get('workflow_count', 0)}

Requirements:
- Be completely original and never use canned phrases
- Sound natural and conversational, not corporate
- Include subtle emotional intelligence
- Reference contextual elements when relevant
- Keep it concise but warm
- Avoid exclamation overuse
- Sound like a creative AI assistant, not a chatbot

Generate a single, novel greeting that feels personal and contextually aware:"""

    def _analyze_recent_interactions(self, user_data: dict) -> str:
        """Analyze recent user interactions to understand mood/energy"""
        # This would analyze recent commands, success rates, time patterns, etc.
        # to understand user's current working style and energy
        recent_commands = user_data.get("recent_commands", [])
        success_rate = user_data.get("recent_success_rate", 0.5)
        
        if success_rate > 0.8:
            return "productive and accomplished"
        elif success_rate < 0.3:
            return "working through challenges"
        else:
            return "focused and methodical"
    
    def _get_weather_context(self) -> str:
        """Optional: Get general weather vibe for more contextual greetings"""
        # Could integrate with weather API or just use general seasonal patterns
        season = self._get_season()
        time_context = self._get_time_context()
        
        weather_vibes = {
            "winter_morning": "crisp and energizing",
            "spring_afternoon": "fresh and inspiring", 
            "summer_evening": "warm and relaxed",
            "fall_late": "cozy and contemplative"
        }
        
        key = f"{season}_{time_context}"
        return weather_vibes.get(key, "pleasant")
```

---

## API Key Management System

### Hosted Credential Storage
Moving API key management to the web interface eliminates the complexity of terminal/mobile credential management while improving security.

**Web Interface for API Keys:**
```python
class HostedAPIKeyManager:
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
        self.supported_providers = {
            "anthropic": {"name": "Anthropic (Claude)", "required": True},
            "openai": {"name": "OpenAI (GPT)", "required": False},
            "google": {"name": "Google AI", "required": False},
            "cohere": {"name": "Cohere", "required": False}
        }
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key for secure storage"""
        from cryptography.fernet import Fernet
        cipher_suite = Fernet(self.encryption_key)
        encrypted_key = cipher_suite.encrypt(api_key.encode())
        return encrypted_key.decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key for use"""
        from cryptography.fernet import Fernet
        cipher_suite = Fernet(self.encryption_key)
        decrypted_key = cipher_suite.decrypt(encrypted_key.encode())
        return decrypted_key.decode()
    
    def store_api_key(self, user_id: str, provider: str, api_key: str) -> dict:
        """Store encrypted API key for user"""
        if provider not in self.supported_providers:
            return {"success": False, "error": f"Unsupported provider: {provider}"}
        
        try:
            encrypted_key = self.encrypt_api_key(api_key)
            user_data = self.load_user_by_id(user_id)
            
            if "api_keys" not in user_data:
                user_data["api_keys"] = {}
            
            user_data["api_keys"][provider] = {
                "encrypted_key": encrypted_key,
                "created_at": datetime.now().isoformat(),
                "last_used": None
            }
            
            self.save_user_data(user_id, user_data)
            
            return {
                "success": True,
                "message": f"{self.supported_providers[provider]['name']} API key stored securely"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to store API key: {str(e)}"}
```

**CLI Integration with Hosted Keys:**
```python
class CLICredentialManager:
    def __init__(self):
        self.api_key_manager = HostedAPIKeyManager()
    
    def get_api_key_for_request(self, user_id: str, provider: str) -> str:
        """Retrieve and decrypt API key for CLI usage"""
        user_data = self.load_user_by_id(user_id)
        api_keys = user_data.get("api_keys", {})
        
        if provider not in api_keys:
            raise ValueError(f"No {provider} API key configured. Please add it at https://mao.app/settings")
        
        encrypted_key = api_keys[provider]["encrypted_key"]
        return self.api_key_manager.decrypt_api_key(encrypted_key)
    
    def check_api_key_availability(self, user_id: str) -> dict:
        """Check which API keys are available for user"""
        user_data = self.load_user_by_id(user_id)
        api_keys = user_data.get("api_keys", {})
        
        availability = {}
        for provider, config in self.api_key_manager.supported_providers.items():
            availability[provider] = {
                "configured": provider in api_keys,
                "required": config["required"],
                "name": config["name"]
            }
        
        return availability
```

---

## Migration Strategy

### Backwards Compatibility
Ensuring smooth transition from username-based to email-based system without breaking existing installations.

**Migration Process:**
1. **Phase 1: Dual Support** (v4.1.0)
   - Support both username and email login
   - Automatic email collection for existing users
   - UserID generation works with both inputs
   
2. **Phase 2: Email Encouragement** (v4.1.1)
   - Prompt existing users to add email if missing
   - Show benefits of email-based login
   - Enable passkey setup for users with emails
   
3. **Phase 3: Email Primary** (v4.2.0)
   - Email becomes primary login method
   - Username maintained for display/legacy compatibility
   - Full passkey integration deployment

**Migration Script:**
```python
class UserMigrationManager:
    def __init__(self):
        self.username_manager = UsernameManager()
    
    def migrate_username_to_email(self, username: str, email: str) -> dict:
        """Migrate existing username-based user to email-based"""
        try:
            # Load existing user data
            user_data = self.username_manager.load_user(username)
            if not user_data:
                return {"success": False, "error": "User not found"}
            
            # Check if email is already in use
            existing_email_user = self.find_user_by_email(email)
            if existing_email_user:
                return {"success": False, "error": "Email already in use"}
            
            # Update user data structure
            migrated_data = {
                "email": email,
                "user_id": user_data["user_id"],  # Keep existing UserID
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "display_name": user_data.get("username", email.split('@')[0]),
                "legacy_username": user_data.get("username"),  # Keep for reference
                "passkey_enabled": False,
                "created_at": user_data.get("created_at"),
                "last_login": datetime.now().isoformat(),
                "migration_date": datetime.now().isoformat()
            }
            
            # Create new email-based directory structure
            self.create_email_based_structure(email, migrated_data)
            
            # Migrate memories and analytics
            self.migrate_user_data(username, email)
            
            # Update session if this is current user
            current_session = self.username_manager.get_session_user()
            if current_session and current_session.get("username") == username:
                self.set_email_session(email)
            
            return {
                "success": True,
                "message": f"Successfully migrated {username} to {email}",
                "new_structure": migrated_data
            }
            
        except Exception as e:
            return {"success": False, "error": f"Migration failed: {str(e)}"}
```

---

## Security Implementation

### Encryption and Data Protection
Implementing enterprise-grade security for credential storage and user data protection.

**Encryption Strategy:**
```python
class SecurityManager:
    def __init__(self):
        self.key_derivation = self._setup_key_derivation()
        self.session_manager = SecureSessionManager()
    
    def _setup_key_derivation(self):
        """Setup PBKDF2 key derivation for encryption keys"""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._get_application_salt(),
            iterations=100000
        )
    
    def encrypt_sensitive_data(self, data: str, user_id: str) -> str:
        """Encrypt sensitive data with user-specific key derivation"""
        from cryptography.fernet import Fernet
        
        # Derive user-specific key
        user_key = self.key_derivation.derive(user_id.encode())
        cipher_suite = Fernet(base64.urlsafe_b64encode(user_key))
        
        encrypted_data = cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str, user_id: str) -> str:
        """Decrypt sensitive data with user-specific key derivation"""
        from cryptography.fernet import Fernet
        
        # Derive same user-specific key
        user_key = self.key_derivation.derive(user_id.encode())
        cipher_suite = Fernet(base64.urlsafe_b64encode(user_key))
        
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = cipher_suite.decrypt(decoded_data)
        return decrypted_data.decode()
```

### Session Security
```python
class SecureSessionManager:
    def __init__(self):
        self.session_timeout = 24 * 60 * 60  # 24 hours
        self.refresh_threshold = 2 * 60 * 60  # 2 hours
    
    def create_secure_session(self, email: str, user_id: str) -> dict:
        """Create secure session with automatic refresh"""
        session_token = self._generate_session_token()
        refresh_token = self._generate_refresh_token()
        
        session_data = {
            "session_token": session_token,
            "refresh_token": refresh_token,
            "email": email,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        # Store session securely
        self._store_session(session_token, session_data)
        
        return {
            "session_token": session_token,
            "refresh_token": refresh_token,
            "expires_in": self.session_timeout
        }
    
    def validate_session(self, session_token: str) -> dict:
        """Validate session and refresh if needed"""
        session_data = self._load_session(session_token)
        if not session_data:
            return {"valid": False, "error": "Session not found"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        if datetime.now() > expires_at:
            self._invalidate_session(session_token)
            return {"valid": False, "error": "Session expired"}
        
        # Check if refresh needed
        last_activity = datetime.fromisoformat(session_data["last_activity"])
        if (datetime.now() - last_activity).seconds > self.refresh_threshold:
            # Refresh session
            session_data["last_activity"] = datetime.now().isoformat()
            session_data["expires_at"] = (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat()
            self._store_session(session_token, session_data)
        
        return {"valid": True, "session_data": session_data}
```

---

## Registration Form and Bot Protection

### Cloudflare Turnstile Integration
Implementing the elegant "I'm not a robot" verification without the awful "click on traffic lights" experience.

**Shadcn/ui Inspired Registration Form:**
```html
<!-- Beautiful Registration Form (No Email Verification Nonsense!) -->
<div class="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 px-4">
    <div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[420px]">
        <!-- Header -->
        <div class="flex flex-col space-y-2 text-center">
            <h1 class="text-2xl font-semibold tracking-tight">Create your account</h1>
            <p class="text-sm text-slate-600">Enter your details to get started with MAO</p>
        </div>
        
        <!-- Form Card -->
        <div class="rounded-lg border bg-white p-8 shadow-sm">
            <form id="registration-form" class="space-y-4">
                <!-- Email Field -->
                <div class="space-y-2">
                    <label for="email" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                        Email
                    </label>
                    <input 
                        type="email" 
                        id="email" 
                        name="email" 
                        required 
                        class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="sean@august.style"
                    >
                    <div id="email-feedback" class="text-xs text-slate-500"></div>
                </div>
                
                <!-- Name Fields Row -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <label for="firstName" class="text-sm font-medium leading-none">
                            First name
                        </label>
                        <input 
                            type="text" 
                            id="firstName" 
                            name="firstName" 
                            required 
                            class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                            placeholder="Sean"
                        >
                    </div>
                    
                    <div class="space-y-2">
                        <label for="lastName" class="text-sm font-medium leading-none text-slate-600">
                            Last name <span class="text-slate-400">(optional)</span>
                        </label>
                        <input 
                            type="text" 
                            id="lastName" 
                            name="lastName" 
                            class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                            placeholder="Horvath"
                        >
                    </div>
                </div>
                
                <!-- Display Name Field -->
                <div class="space-y-2">
                    <label for="displayName" class="text-sm font-medium leading-none text-slate-600">
                        How should MAO greet you? <span class="text-slate-400">(optional)</span>
                    </label>
                    <input 
                        type="text" 
                        id="displayName" 
                        name="displayName" 
                        class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="Sean, or whatever you prefer"
                    >
                    <p class="text-xs text-slate-500">MAO will use this for personalized AI-generated greetings</p>
                </div>
                
                <!-- Authentication Method Choice (Porkbun Style!) -->
                <div class="space-y-3">
                    <label class="text-sm font-medium leading-none">Authentication Method</label>
                    <div class="space-y-3">
                        <!-- Passkey Option (Recommended) -->
                        <div class="relative">
                            <input type="radio" id="auth-passkey" name="authMethod" value="passkey" class="peer sr-only" checked>
                            <label for="auth-passkey" class="flex items-center justify-between w-full p-4 text-sm font-medium text-slate-900 bg-white border-2 border-slate-200 rounded-lg cursor-pointer peer-checked:border-slate-900 peer-checked:bg-slate-50 hover:text-slate-900 hover:bg-slate-50">
                                <div class="flex items-center">
                                    <svg class="w-5 h-5 mr-3 text-slate-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M9 12l2 2 4-4"/>
                                        <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"/>
                                        <path d="M3 12v6c0 .552.448 1 1 1h16c.552 0 1-.448 1-1v-6"/>
                                    </svg>
                                    <div>
                                        <div class="font-medium">Use Passkey</div>
                                        <div class="text-xs text-slate-500">Secure biometric login (Touch ID, Face ID, etc.)</div>
                                    </div>
                                </div>
                                <div class="px-2 py-1 text-xs font-medium text-emerald-700 bg-emerald-100 rounded">Recommended</div>
                            </label>
                        </div>
                        
                        <!-- Email Only Option (Fallback) -->
                        <div class="relative">
                            <input type="radio" id="auth-email" name="authMethod" value="email" class="peer sr-only">
                            <label for="auth-email" class="flex items-center justify-between w-full p-4 text-sm font-medium text-slate-900 bg-white border-2 border-slate-200 rounded-lg cursor-pointer peer-checked:border-slate-900 peer-checked:bg-slate-50 hover:text-slate-900 hover:bg-slate-50">
                                <div class="flex items-center">
                                    <svg class="w-5 h-5 mr-3 text-slate-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                        <polyline points="22,6 12,13 2,6"/>
                                    </svg>
                                    <div>
                                        <div class="font-medium">Email Only</div>
                                        <div class="text-xs text-slate-500">We'll help you set up a passkey later</div>
                                    </div>
                                </div>
                            </label>
                        </div>
                    </div>
                </div>
                
                <!-- Turnstile Widget -->
                <div class="space-y-2">
                    <div class="cf-turnstile flex justify-center" data-sitekey="YOUR_TURNSTILE_SITE_KEY"></div>
                </div>
                
                <!-- Passkey Notice -->
                <div class="rounded-md border border-emerald-200 bg-emerald-50 p-4">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-emerald-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.236 4.53L8.23 10.661a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-emerald-700">
                                <strong>Instant access!</strong> We'll set up a passkey for secure, passwordless login right after you create your account.
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Submit Button (Dynamic Text) -->
                <button 
                    type="submit" 
                    id="submit-button"
                    class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-slate-900 text-slate-50 hover:bg-slate-800 h-10 px-4 py-2 w-full"
                    disabled
                >
                    <span id="button-text">Create Account with Passkey</span>
                    <div id="button-loading" class="hidden ml-2">
                        <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2Z"></path>
                        </svg>
                        <span class="ml-2">Creating...</span>
                    </div>
                </button>
                
                <!-- Login Link -->
                <div class="text-center">
                    <p class="text-sm text-slate-600">
                        Already have an account? 
                        <a href="/login" class="font-medium text-slate-900 hover:underline">Sign in</a>
                    </p>
                </div>
            </form>
        </div>
        
        <!-- Terms -->
        <p class="px-8 text-center text-xs text-slate-600">
            By creating an account, you agree to our{' '}
            <a href="/terms" class="underline underline-offset-4 hover:text-slate-900">Terms of Service</a>
            {' '}and{' '}
            <a href="/privacy" class="underline underline-offset-4 hover:text-slate-900">Privacy Policy</a>
        </p>
    </div>
</div>

<!-- Login Form (Equally Beautiful) -->
<div class="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 px-4">
    <div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[420px]">
        <!-- Header -->
        <div class="flex flex-col space-y-2 text-center">
            <h1 class="text-2xl font-semibold tracking-tight">Welcome back</h1>
            <p class="text-sm text-slate-600">Sign in to your MAO account</p>
        </div>
        
        <!-- Form Card -->
        <div class="rounded-lg border bg-white p-8 shadow-sm">
            <form id="login-form" class="space-y-6">
                <!-- Email Field -->
                <div class="space-y-2">
                    <label for="login-email" class="text-sm font-medium leading-none">Email</label>
                    <input 
                        type="email" 
                        id="login-email" 
                        name="email" 
                        required
                        class="flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2"
                        placeholder="sean@august.style"
                    >
                </div>
                
                <!-- Authentication Method Choice -->
                <div class="space-y-3">
                    <label class="text-sm font-medium leading-none">Authentication Method</label>
                    <div class="space-y-3">
                        <!-- Passkey Option (Primary) -->
                        <div class="relative">
                            <input type="radio" id="login-auth-passkey" name="loginAuthMethod" value="passkey" class="peer sr-only" checked>
                            <label for="login-auth-passkey" class="flex items-center justify-between w-full p-4 text-sm font-medium text-slate-900 bg-white border-2 border-slate-200 rounded-lg cursor-pointer peer-checked:border-slate-900 peer-checked:bg-slate-50 hover:text-slate-900 hover:bg-slate-50">
                                <div class="flex items-center">
                                    <svg class="w-5 h-5 mr-3 text-slate-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M9 12l2 2 4-4"/>
                                        <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"/>
                                        <path d="M3 12v6c0 .552.448 1 1 1h16c.552 0 1-.448 1-1v-6"/>
                                    </svg>
                                    <div>
                                        <div class="font-medium">Use Passkey</div>
                                        <div class="text-xs text-slate-500">Touch ID, Face ID, fingerprint, or PIN</div>
                                    </div>
                                </div>
                            </label>
                        </div>
                        
                        <!-- Email Only Option -->
                        <div class="relative">
                            <input type="radio" id="login-auth-email" name="loginAuthMethod" value="email" class="peer sr-only">
                            <label for="login-auth-email" class="flex items-center justify-between w-full p-4 text-sm font-medium text-slate-900 bg-white border-2 border-slate-200 rounded-lg cursor-pointer peer-checked:border-slate-900 peer-checked:bg-slate-50 hover:text-slate-900 hover:bg-slate-50">
                                <div class="flex items-center">
                                    <svg class="w-5 h-5 mr-3 text-slate-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                                        <polyline points="22,6 12,13 2,6"/>
                                    </svg>
                                    <div>
                                        <div class="font-medium">Don't have a passkey?</div>
                                        <div class="text-xs text-slate-500">We'll help you set one up</div>
                                    </div>
                                </div>
                            </label>
                        </div>
                    </div>
                </div>
                
                <!-- Submit Button -->
                <button 
                    type="submit"
                    id="login-submit-button"
                    class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-slate-900 text-slate-50 hover:bg-slate-800 h-10 px-4 py-2 w-full"
                >
                    <span id="login-button-text">Sign in with Passkey</span>
                </button>
            </form>
        </div>
    </div>
</div>

<!-- Include Turnstile Script -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
```

**JavaScript Form Handling:**
```javascript
class RegistrationFormManager {
    constructor() {
        this.form = document.getElementById('registration-form');
        this.submitButton = document.getElementById('submit-button');
        this.turnstileToken = null;
        
        this.initializeForm();
    }
    
    initializeForm() {
        // Handle Turnstile callback
        window.turnstileCallback = (token) => {
            this.turnstileToken = token;
            this.validateForm();
        };
        
        // Handle form validation
        this.form.addEventListener('input', () => this.validateForm());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Handle authentication method selection
        this.initializeAuthMethodSelection();
        
        // Handle passkey-first login flows
        this.initializePasskeyFlow();
        
        // Configure Turnstile
        window.onloadTurnstileCallback = () => {
            turnstile.render('.cf-turnstile', {
                sitekey: 'YOUR_TURNSTILE_SITE_KEY',
                callback: 'turnstileCallback',
                'error-callback': () => {
                    console.error('Turnstile verification failed');
                    this.showError('Verification failed. Please try again.');
                }
            });
        };
    }
    
    validateForm() {
        const email = document.getElementById('email').value;
        const firstName = document.getElementById('firstName').value;
        const isValidEmail = this.isValidEmail(email);
        const hasRequiredFields = email && firstName;
        const hasTurnstileToken = !!this.turnstileToken;
        
        this.submitButton.disabled = !(isValidEmail && hasRequiredFields && hasTurnstileToken);
    }
    
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.turnstileToken) {
            this.showError('Please complete the security verification.');
            return;
        }
        
        this.setLoading(true);
        
        try {
            // Get selected authentication method
            const selectedAuthMethod = document.querySelector('input[name="authMethod"]:checked').value;
            
            // Collect form data
            const formData = {
                email: document.getElementById('email').value,
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                displayName: document.getElementById('displayName').value,
                authMethod: selectedAuthMethod,
                turnstileToken: this.turnstileToken
            };
            
            // Create account first
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Store session token
                localStorage.setItem('mao_session_token', result.session_token);
                
                if (selectedAuthMethod === 'passkey') {
                    // Immediately set up passkey after account creation
                    await this.setupPasskeyFlow(result.user);
                } else {
                    // Email-only flow - account created, user can set up passkey later
                    this.showSuccess(
                        `Welcome to MAO, ${result.user.first_name}! Your account is ready.`
                    );
                    
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                }
                
            } else {
                this.showError(result.message || 'Registration failed. Please try again.');
            }
            
        } catch (error) {
            console.error('Registration error:', error);
            this.showError('Something went wrong. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }
    
    async setupPasskeyFlow(user) {
        try {
            // Check if browser supports passkeys
            if (!window.PublicKeyCredential) {
                this.showError('Your browser doesn\'t support passkeys. Redirecting to dashboard...');
                setTimeout(() => window.location.href = '/dashboard', 2000);
                return;
            }
            
            this.showSuccess(`Account created! Setting up your passkey now...`);
            
            // Get passkey registration options from server
            const response = await fetch('/api/auth/passkey/register-options', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('mao_session_token')}`
                },
                body: JSON.stringify({ email: user.email })
            });
            
            const options = await response.json();
            
            // Create passkey
            const credential = await navigator.credentials.create({
                publicKey: options.publicKey
            });
            
            // Send credential to server for storage
            const verifyResponse = await fetch('/api/auth/passkey/register', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('mao_session_token')}`
                },
                body: JSON.stringify({
                    credential: {
                        id: credential.id,
                        rawId: Array.from(new Uint8Array(credential.rawId)),
                        response: {
                            attestationObject: Array.from(new Uint8Array(credential.response.attestationObject)),
                            clientDataJSON: Array.from(new Uint8Array(credential.response.clientDataJSON))
                        },
                        type: credential.type
                    }
                })
            });
            
            const verifyResult = await verifyResponse.json();
            
            if (verifyResult.success) {
                this.showSuccess(`Passkey set up successfully! Welcome to MAO, ${user.first_name}!`);
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                this.showError('Passkey setup failed, but your account is created. You can set it up later in settings.');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            }
            
        } catch (error) {
            console.error('Passkey setup error:', error);
            this.showError('Passkey setup was cancelled, but your account is created. You can set it up later in settings.');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 2000);
        }
    }
    
    initializeAuthMethodSelection() {
        // Handle radio button changes for auth method (Porkbun style!)
        const authMethodRadios = document.querySelectorAll('input[name="authMethod"]');
        const buttonText = document.getElementById('button-text');
        
        authMethodRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                if (radio.value === 'passkey') {
                    buttonText.textContent = 'Create Account with Passkey';
                } else {
                    buttonText.textContent = 'Create Account';
                }
            });
        });
    }
    
    initializePasskeyFlow() {
        // Handle passkey login button
        const passkeyButton = document.getElementById('passkey-login');
        if (passkeyButton) {
            passkeyButton.addEventListener('click', () => this.handlePasskeyLogin());
        }
        
        // Handle email fallback form (guides to passkey setup)
        const emailLoginForm = document.getElementById('email-login-form');
        if (emailLoginForm) {
            emailLoginForm.addEventListener('submit', (e) => this.handleEmailFallback(e));
        }
    }
    
    async handlePasskeyLogin() {
        try {
            // Check if browser supports passkeys
            if (!window.PublicKeyCredential) {
                this.showError('Your browser doesn\'t support passkeys. Please update your browser for modern security.');
                return;
            }
            
            // Get authentication options from server
            const response = await fetch('/api/auth/passkey/authenticate-options', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const options = await response.json();
            
            // Start passkey authentication
            const credential = await navigator.credentials.get({
                publicKey: options.publicKey
            });
            
            // Send credential to server for verification
            const verifyResponse = await fetch('/api/auth/passkey/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    credential: {
                        id: credential.id,
                        rawId: Array.from(new Uint8Array(credential.rawId)),
                        response: {
                            authenticatorData: Array.from(new Uint8Array(credential.response.authenticatorData)),
                            clientDataJSON: Array.from(new Uint8Array(credential.response.clientDataJSON)),
                            signature: Array.from(new Uint8Array(credential.response.signature))
                        },
                        type: credential.type
                    }
                })
            });
            
            const result = await verifyResponse.json();
            
            if (result.success) {
                localStorage.setItem('mao_session_token', result.session_token);
                window.location.href = '/dashboard';
            } else {
                this.showError(result.message || 'Passkey authentication failed.');
            }
            
        } catch (error) {
            console.error('Passkey login error:', error);
            this.showError('Passkey authentication was cancelled or failed. Use the email option below to set up a passkey.');
        }
    }
    
    async handleEmailFallback(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        if (!email) {
            this.showError('Please enter your email address.');
            return;
        }
        
        try {
            // Check if user exists and has passkey
            const response = await fetch('/api/auth/check-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            
            const result = await response.json();
            
            if (result.userExists) {
                if (result.hasPasskey) {
                    // User has passkey but it failed - guide them to try again
                    this.showError('You have a passkey set up for this email. Please use the "Sign in with Passkey" button above.');
                } else {
                    // User exists but no passkey - guide to setup
                    this.showSuccess('Account found! Let\'s set up a passkey for secure login...');
                    setTimeout(() => {
                        window.location.href = `/setup-passkey?email=${encodeURIComponent(email)}`;
                    }, 1500);
                }
            } else {
                // User doesn't exist - guide to registration
                this.showError('No account found for this email. Please create an account first.');
                setTimeout(() => {
                    // Pre-fill registration form
                    const registerEmail = document.getElementById('email');
                    if (registerEmail) {
                        registerEmail.value = email;
                        registerEmail.focus();
                    }
                }, 2000);
            }
            
        } catch (error) {
            console.error('Email check error:', error);
            this.showError('Unable to check account status. Please try again.');
        }
    }
    
    setLoading(loading) {
        this.submitButton.disabled = loading;
        document.getElementById('button-text').style.display = loading ? 'none' : 'inline';
        document.getElementById('button-loading').style.display = loading ? 'inline' : 'none';
    }
    
    showError(message) {
        // Implement error display (toast, alert, etc.)
        console.error('Registration error:', message);
    }
    
    showSuccess(message) {
        // Implement success display
        console.log('Registration success:', message);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new RegistrationFormManager();
});
```

**Backend Turnstile Verification:**
```python
class TurnstileVerificationManager:
    def __init__(self):
        self.secret_key = os.getenv('TURNSTILE_SECRET_KEY')
        self.verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    
    async def verify_turnstile_token(self, token: str, ip_address: str) -> dict:
        """Verify Turnstile token with Cloudflare"""
        try:
            verification_data = {
                'secret': self.secret_key,
                'response': token,
                'remoteip': ip_address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.verify_url, data=verification_data) as response:
                    result = await response.json()
                    
                    return {
                        'success': result.get('success', False),
                        'error_codes': result.get('error-codes', []),
                        'challenge_ts': result.get('challenge_ts'),
                        'hostname': result.get('hostname')
                    }
                    
        except Exception as e:
            logger.error(f"Turnstile verification failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_verification_valid(self, verification_result: dict) -> bool:
        """Check if Turnstile verification is valid"""
        return verification_result.get('success', False)

class RegistrationEndpoint:
    def __init__(self):
        self.turnstile = TurnstileVerificationManager()
        self.email_manager = EmailVerificationManager()
    
    async def handle_registration(self, request_data: dict, ip_address: str) -> dict:
        """Handle user registration with Turnstile verification"""
        
        # Verify Turnstile token first
        turnstile_result = await self.turnstile.verify_turnstile_token(
            request_data.get('turnstileToken'),
            ip_address
        )
        
        if not self.turnstile.is_verification_valid(turnstile_result):
            return {
                'success': False,
                'message': 'Verification failed. Please try again.',
                'error_code': 'TURNSTILE_FAILED'
            }
        
        # Validate email format
        email = request_data.get('email', '').strip().lower()
        if not self._is_valid_email(email):
            return {
                'success': False,
                'message': 'Please enter a valid email address.',
                'error_code': 'INVALID_EMAIL'
            }
        
        # Check if email already exists
        if await self._email_exists(email):
            return {
                'success': False,
                'message': 'An account with this email already exists.',
                'error_code': 'EMAIL_EXISTS'
            }
        
        # Create account immediately (no email verification nonsense!)
        user_data = {
            'email': email,
            'first_name': request_data.get('firstName', ''),
            'last_name': request_data.get('lastName', ''),
            'display_name': request_data.get('displayName', '') or request_data.get('firstName', ''),
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat(),
            'passkey_enabled': False,  # Will be updated when passkey is created
            'subscription_tier': 'free'
        }
        
        # Generate deterministic UserID
        user_id = self._generate_user_id(email)
        user_data['user_id'] = user_id
        
        # Create user account
        account_created = await self._create_user_account(user_data)
        
        if not account_created:
            return {
                'success': False,
                'message': 'Failed to create account. Please try again.',
                'error_code': 'ACCOUNT_CREATION_FAILED'
            }
        
        # Generate session for immediate login
        session_token = await self._create_session(user_data)
        
        return {
            'success': True,
            'message': 'Account created successfully!',
            'user': {
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'user_id': user_data['user_id'],
                'display_name': user_data['display_name']
            },
            'session_token': session_token,
            'next_step': 'passkey_setup'  # Redirect to passkey setup
        }
```

---

## User Experience Flow

### Login Experience Design
Creating the memorable, friction-free experience inspired by the Porkbun UX.

**Login Flow States:**
1. **Email Entry State**
   - Clean, focused email input
   - Real-time email validation
   - Status: "recognizing..."
   
2. **Authentication Method Detection**
   - Invisible background check for available methods
   - Status: "authenticating..." or whimsical variant
   
3. **Passkey First Attempt**
   - Automatic passkey prompt if available
   - Graceful fallback without user confusion
   - Status: "securing..."
   
4. **Password Fallback**
   - Only shown if passkey fails/unavailable
   - Clear explanation: "Let's try your password instead"
   - Status: "verifying..."
   
5. **Success State**
   - Personalized greeting with user's name
   - Contextual welcome message
   - Status: "celebrating!"

**Registration Flow States:**
1. **Email and Identity Collection**
   - Email, first name, optional last name
   - Display name preference
   - Status: "preparing..."
   
2. **Passkey Setup Offer**
   - Clear explanation of benefits
   - Optional but strongly encouraged
   - Status: "securing..."
   
3. **Account Creation**
   - UserID generation and explanation
   - Directory structure creation
   - Status: "orchestrating..."
   
4. **Welcome and Onboarding**
   - Personalized welcome
   - Quick feature tour
   - Status: "celebrating!"

### Mobile Experience Optimization
```javascript
// Mobile-optimized passkey flow
class MobileAuthManager {
    constructor() {
        this.isMobile = this.detectMobile();
        this.touchOptimized = true;
    }
    
    async optimizedPasskeyFlow(email) {
        if (this.isMobile) {
            // Mobile-specific passkey handling
            return await this.mobilePasskeyAuth(email);
        } else {
            // Desktop passkey handling
            return await this.desktopPasskeyAuth(email);
        }
    }
    
    async mobilePasskeyAuth(email) {
        // Optimize for touch and biometric
        const options = {
            ...this.basePasskeyOptions,
            authenticatorSelection: {
                authenticatorAttachment: "platform",
                userVerification: "required",
                residentKey: "preferred"  // Better mobile experience
            },
            timeout: 120000  // Longer timeout for mobile
        };
        
        return await navigator.credentials.get({publicKey: options});
    }
}
```

---

## Implementation Checklist

### Phase 1: Core Email Authentication (v4.1.0)
- [ ] Update UsernameManager to EmailManager
- [ ] Modify user data schema
- [ ] Implement email-based UserID generation
- [ ] Create migration scripts for existing users
- [ ] Update CLI commands to use email
- [ ] Implement backwards compatibility
- [ ] Add email validation and verification

### Phase 2: Passkey Integration (v4.1.1)
- [ ] Implement WebAuthn server components
- [ ] Create passkey registration flow
- [ ] Build passkey authentication flow
- [ ] Add passkey management UI
- [ ] Implement fallback mechanisms
- [ ] Test cross-platform compatibility
- [ ] Add passkey recovery options

### Phase 3: Hosted API Key Management (v4.1.2)
- [ ] Build encryption system for API keys
- [ ] Create web interface for key management
- [ ] Implement CLI integration with hosted keys
- [ ] Add support for multiple providers
- [ ] Build key rotation and security features
- [ ] Create usage analytics and monitoring
- [ ] Implement key sharing for team accounts

### Phase 4: Emotional UX Intelligence (v4.1.3)
- [ ] Implement contextual status word system
- [ ] Create personalized greeting engine
- [ ] Add whimsical variant generation
- [ ] Build context-aware messaging
- [ ] Implement user preference learning
- [ ] Add time-based contextual messages
- [ ] Create celebration and encouragement systems

### Phase 5: Advanced Security Features (v4.1.4)
- [ ] Implement multi-factor authentication
- [ ] Add device management and trust
- [ ] Build advanced session management
- [ ] Create security audit logging
- [ ] Implement breach detection
- [ ] Add privacy controls and data export
- [ ] Build compliance and GDPR features

---

## Success Metrics

### User Experience Metrics
- **Authentication Success Rate**: Target >99.5%
- **Login Time**: Target <3 seconds average
- **Passkey Adoption**: Target >70% of new users
- **User Satisfaction**: Target >4.8/5 (measured via "audible reaction" test)
- **Support Ticket Reduction**: Target 60% decrease in auth-related issues

### Technical Performance Metrics  
- **System Uptime**: Target 99.9%
- **API Response Time**: Target <200ms average
- **Encryption Performance**: Target <50ms for key operations
- **Mobile Performance**: Target <2 seconds on mobile networks
- **Security Audit Score**: Target 95%+ compliance

### Business Impact Metrics
- **Subscription Conversion**: Target 25% increase
- **User Retention**: Target 40% increase in 30-day retention
- **API Key Management Adoption**: Target 80% of users
- **Customer Support Load**: Target 50% reduction
- **Revenue per User**: Target 30% increase

---

## Future Enhancements

### Advanced Authentication Features
- **Biometric Integration**: Face ID, Touch ID, Windows Hello
- **Hardware Security Keys**: FIDO2/WebAuthn hardware token support  
- **Social Login**: GitHub, Google, Microsoft integration
- **Enterprise SSO**: SAML, OIDC for business customers

### Enhanced UX Intelligence
- **Predictive Greetings**: AI-powered contextual messages
- **Mood Detection**: Adjust interface based on user patterns
- **Productivity Coaching**: Gentle suggestions based on usage
- **Celebration Automation**: Automatic recognition of achievements

### Advanced Security
- **Zero-Knowledge Architecture**: End-to-end encryption for all data
- **Decentralized Identity**: Integration with Web3 identity standards
- **Advanced Threat Detection**: ML-powered security monitoring
- **Privacy-First Analytics**: Differential privacy for user insights

---

*This implementation transforms MAO from a powerful local tool into a secure, modern platform ready for subscription services, team collaboration, and enterprise deployment. The email-based authentication with passkey integration provides the foundation for a seamless, secure, and delightfully emotional user experience that will set MAO apart in the AI tool landscape.*

---

## Complete Passkey Implementation Examples

### WebAuthn Registration Flow
```javascript
// Complete passkey registration implementation
class PasskeyRegistrationManager {
    constructor() {
        this.apiBaseUrl = '/api/auth';
    }
    
    async startRegistration(userEmail, displayName) {
        try {
            // Get registration options from server
            const optionsResponse = await fetch(`${this.apiBaseUrl}/passkey/registration/begin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: userEmail, displayName })
            });
            
            const options = await optionsResponse.json();
            
            if (!options.success) {
                throw new Error(options.message || 'Failed to get registration options');
            }
            
            // Convert challenge and user ID to ArrayBuffer
            const publicKeyCredentialCreationOptions = {
                ...options.publicKey,
                challenge: this.base64ToArrayBuffer(options.publicKey.challenge),
                user: {
                    ...options.publicKey.user,
                    id: this.base64ToArrayBuffer(options.publicKey.user.id)
                }
            };
            
            // Create the credential
            const credential = await navigator.credentials.create({
                publicKey: publicKeyCredentialCreationOptions
            });
            
            if (!credential) {
                throw new Error('Failed to create passkey');
            }
            
            // Prepare credential data for server
            const credentialData = {
                id: credential.id,
                rawId: this.arrayBufferToBase64(credential.rawId),
                response: {
                    attestationObject: this.arrayBufferToBase64(credential.response.attestationObject),
                    clientDataJSON: this.arrayBufferToBase64(credential.response.clientDataJSON)
                },
                type: credential.type,
                clientExtensionResults: credential.getClientExtensionResults()
            };
            
            // Verify registration with server
            const verifyResponse = await fetch(`${this.apiBaseUrl}/passkey/registration/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: userEmail,
                    credential: credentialData
                })
            });
            
            const result = await verifyResponse.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Passkey registration failed');
            }
            
            return {
                success: true,
                message: 'Passkey created successfully!',
                credentialId: credential.id
            };
            
        } catch (error) {
            console.error('Passkey registration error:', error);
            return {
                success: false,
                message: error.message || 'Failed to create passkey'
            };
        }
    }
    
    async startAuthentication(userEmail = null) {
        try {
            // Get authentication options from server
            const optionsResponse = await fetch(`${this.apiBaseUrl}/passkey/authentication/begin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: userEmail }) // null for usernameless flow
            });
            
            const options = await optionsResponse.json();
            
            if (!options.success) {
                throw new Error(options.message || 'Failed to get authentication options');
            }
            
            // Convert challenge and credential IDs to ArrayBuffer
            const publicKeyCredentialRequestOptions = {
                ...options.publicKey,
                challenge: this.base64ToArrayBuffer(options.publicKey.challenge),
                allowCredentials: options.publicKey.allowCredentials?.map(cred => ({
                    ...cred,
                    id: this.base64ToArrayBuffer(cred.id)
                })) || []
            };
            
            // Get the credential
            const assertion = await navigator.credentials.get({
                publicKey: publicKeyCredentialRequestOptions
            });
            
            if (!assertion) {
                throw new Error('Failed to authenticate with passkey');
            }
            
            // Prepare assertion data for server
            const assertionData = {
                id: assertion.id,
                rawId: this.arrayBufferToBase64(assertion.rawId),
                response: {
                    authenticatorData: this.arrayBufferToBase64(assertion.response.authenticatorData),
                    clientDataJSON: this.arrayBufferToBase64(assertion.response.clientDataJSON),
                    signature: this.arrayBufferToBase64(assertion.response.signature),
                    userHandle: assertion.response.userHandle ? 
                        this.arrayBufferToBase64(assertion.response.userHandle) : null
                },
                type: assertion.type,
                clientExtensionResults: assertion.getClientExtensionResults()
            };
            
            // Verify authentication with server
            const verifyResponse = await fetch(`${this.apiBaseUrl}/passkey/authentication/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: userEmail,
                    assertion: assertionData
                })
            });
            
            const result = await verifyResponse.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Passkey authentication failed');
            }
            
            return {
                success: true,
                message: 'Successfully authenticated!',
                user: result.user,
                sessionToken: result.sessionToken
            };
            
        } catch (error) {
            console.error('Passkey authentication error:', error);
            return {
                success: false,
                message: error.message || 'Failed to authenticate with passkey'
            };
        }
    }
    
    // Helper methods for ArrayBuffer/Base64 conversion
    base64ToArrayBuffer(base64) {
        const binaryString = atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    }
    
    arrayBufferToBase64(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }
    
    // Check if passkeys are supported
    static async isSupported() {
        return !!(
            window.navigator?.credentials?.create &&
            window.navigator?.credentials?.get &&
            window.PublicKeyCredential
        );
    }
    
    // Enhanced feature detection for 2025
    static async getCapabilities() {
        if (!await this.isSupported()) {
            return { supported: false };
        }
        
        try {
            // Use new Chrome 133+ feature detection
            if (window.PublicKeyCredential?.getClientCapabilities) {
                const capabilities = await window.PublicKeyCredential.getClientCapabilities();
                return {
                    supported: true,
                    conditionalGet: capabilities.conditionalGet === true,
                    passkeyPlatformAuthenticator: capabilities.passkeyPlatformAuthenticator === true,
                    hybridTransport: capabilities.hybridTransport === true
                };
            }
            
            // Fallback detection for older browsers
            const platformAuthenticatorAvailable = await window.PublicKeyCredential
                .isUserVerifyingPlatformAuthenticatorAvailable();
                
            return {
                supported: true,
                conditionalGet: false, // Unknown
                passkeyPlatformAuthenticator: platformAuthenticatorAvailable,
                hybridTransport: false // Unknown
            };
            
        } catch (error) {
            console.warn('Failed to detect passkey capabilities:', error);
            return { supported: true }; // Basic support
        }
    }
}

// Usage example
async function setupPasskeyAuth() {
    const passkeyManager = new PasskeyRegistrationManager();
    
    // Check capabilities
    const capabilities = await PasskeyRegistrationManager.getCapabilities();
    console.log('Passkey capabilities:', capabilities);
    
    if (!capabilities.supported) {
        console.log('Passkeys not supported on this device');
        return;
    }
    
    // Registration example
    document.getElementById('register-passkey').addEventListener('click', async () => {
        const result = await passkeyManager.startRegistration(
            'sean@august.style', 
            'Sean'
        );
        
        if (result.success) {
            alert('Passkey created successfully!');
        } else {
            alert(`Failed to create passkey: ${result.message}`);
        }
    });
    
    // Authentication example  
    document.getElementById('login-passkey').addEventListener('click', async () => {
        const result = await passkeyManager.startAuthentication();
        
        if (result.success) {
            alert(`Welcome back, ${result.user.first_name}!`);
            // Redirect to dashboard or update UI
        } else {
            alert(`Login failed: ${result.message}`);
        }
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', setupPasskeyAuth);
```

### Python Backend Passkey Implementation
```python
import base64
import json
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from webauthn import generate_registration_options, verify_registration_response
from webauthn import generate_authentication_options, verify_authentication_response
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria, UserVerificationRequirement,
    AttestationConveyancePreference, AuthenticatorAttachment,
    ResidentKeyRequirement, PublicKeyCredentialDescriptor
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier

class PasskeyManager:
    def __init__(self):
        self.rp_id = "mao.app"  # Your domain
        self.rp_name = "Modular Agent Orchestrator"
        self.origin = "https://mao.app"  # Your full origin
        
    def generate_registration_options(self, email: str, display_name: str) -> Dict[str, Any]:
        """Generate WebAuthn registration options for a new passkey"""
        try:
            # Generate user ID from email (deterministic)
            user_id = self._generate_user_id(email)
            
            options = generate_registration_options(
                rp_id=self.rp_id,
                rp_name=self.rp_name,
                user_id=user_id.encode('utf-8'),
                user_name=email,
                user_display_name=display_name or email.split('@')[0],
                attestation=AttestationConveyancePreference.NONE,
                authenticator_selection=AuthenticatorSelectionCriteria(
                    authenticator_attachment=None,  # Allow both platform and roaming
                    resident_key=ResidentKeyRequirement.PREFERRED,
                    user_verification=UserVerificationRequirement.PREFERRED
                ),
                supported_pub_key_algs=[
                    COSEAlgorithmIdentifier.ECDSA_SHA_256,
                    COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
                ],
                exclude_credentials=self._get_existing_credentials(email),
                challenge=secrets.token_bytes(32)
            )
            
            # Store challenge for verification
            self._store_challenge(email, options.challenge, 'registration')
            
            return {
                'success': True,
                'publicKey': {
                    'challenge': base64.urlsafe_b64encode(options.challenge).decode('utf-8'),
                    'rp': {
                        'name': options.rp.name,
                        'id': options.rp.id
                    },
                    'user': {
                        'id': base64.urlsafe_b64encode(options.user.id).decode('utf-8'),
                        'name': options.user.name,
                        'displayName': options.user.display_name
                    },
                    'pubKeyCredParams': [
                        {'alg': alg.alg, 'type': 'public-key'} 
                        for alg in options.pub_key_cred_params
                    ],
                    'timeout': 60000,
                    'attestation': options.attestation,
                    'authenticatorSelection': {
                        'authenticatorAttachment': options.authenticator_selection.authenticator_attachment,
                        'residentKey': options.authenticator_selection.resident_key,
                        'userVerification': options.authenticator_selection.user_verification
                    },
                    'excludeCredentials': [
                        {
                            'id': base64.urlsafe_b64encode(cred.id).decode('utf-8'),
                            'type': cred.type,
                            'transports': cred.transports
                        }
                        for cred in options.exclude_credentials or []
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate registration options: {e}")
            return {'success': False, 'message': 'Failed to generate registration options'}
    
    def verify_registration(self, email: str, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify WebAuthn registration response"""
        try:
            # Get stored challenge
            challenge = self._get_challenge(email, 'registration')
            if not challenge:
                return {'success': False, 'message': 'Invalid or expired challenge'}
            
            # Prepare credential for verification
            credential = {
                'id': credential_data['id'],
                'rawId': base64.urlsafe_b64decode(credential_data['rawId']),
                'response': {
                    'attestationObject': base64.urlsafe_b64decode(
                        credential_data['response']['attestationObject']
                    ),
                    'clientDataJSON': base64.urlsafe_b64decode(
                        credential_data['response']['clientDataJSON']
                    )
                },
                'type': credential_data['type']
            }
            
            # Verify the registration
            verification = verify_registration_response(
                credential=credential,
                expected_challenge=challenge,
                expected_origin=self.origin,
                expected_rp_id=self.rp_id
            )
            
            if not verification.verified:
                return {'success': False, 'message': 'Registration verification failed'}
            
            # Store the credential
            credential_record = {
                'credential_id': credential_data['id'],
                'public_key': base64.urlsafe_b64encode(verification.credential_public_key).decode('utf-8'),
                'sign_count': verification.sign_count,
                'email': email,
                'created_at': datetime.now().isoformat(),
                'credential_type': 'passkey',
                'backup_eligible': verification.credential_backed_up,
                'backup_state': verification.credential_backed_up,
                'device_type': verification.credential_device_type.value if verification.credential_device_type else 'unknown'
            }
            
            success = self._store_credential(email, credential_record)
            
            if success:
                # Clean up challenge
                self._remove_challenge(email, 'registration')
                
                return {
                    'success': True,
                    'message': 'Passkey registered successfully',
                    'credential_id': credential_data['id'],
                    'backup_eligible': verification.credential_backed_up
                }
            else:
                return {'success': False, 'message': 'Failed to store credential'}
                
        except Exception as e:
            logger.error(f"Registration verification failed: {e}")
            return {'success': False, 'message': 'Registration verification failed'}
    
    def generate_authentication_options(self, email: Optional[str] = None) -> Dict[str, Any]:
        """Generate WebAuthn authentication options"""
        try:
            # Get user's credentials if email provided
            allow_credentials = []
            if email:
                credentials = self._get_user_credentials(email)
                allow_credentials = [
                    PublicKeyCredentialDescriptor(
                        id=base64.urlsafe_b64decode(cred['credential_id']),
                        type='public-key'
                    )
                    for cred in credentials
                ]
            
            options = generate_authentication_options(
                rp_id=self.rp_id,
                challenge=secrets.token_bytes(32),
                allow_credentials=allow_credentials,
                user_verification=UserVerificationRequirement.PREFERRED
            )
            
            # Store challenge for verification
            challenge_key = email or 'usernameless'
            self._store_challenge(challenge_key, options.challenge, 'authentication')
            
            return {
                'success': True,
                'publicKey': {
                    'challenge': base64.urlsafe_b64encode(options.challenge).decode('utf-8'),
                    'timeout': 60000,
                    'rpId': options.rp_id,
                    'allowCredentials': [
                        {
                            'id': base64.urlsafe_b64encode(cred.id).decode('utf-8'),
                            'type': cred.type
                        }
                        for cred in options.allow_credentials or []
                    ],
                    'userVerification': options.user_verification
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate authentication options: {e}")
            return {'success': False, 'message': 'Failed to generate authentication options'}
    
    def verify_authentication(self, email: Optional[str], assertion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify WebAuthn authentication response"""
        try:
            # Get stored challenge
            challenge_key = email or 'usernameless'
            challenge = self._get_challenge(challenge_key, 'authentication')
            if not challenge:
                return {'success': False, 'message': 'Invalid or expired challenge'}
            
            # Find credential record
            credential_record = self._get_credential_by_id(assertion_data['id'])
            if not credential_record:
                return {'success': False, 'message': 'Credential not found'}
            
            # Prepare assertion for verification
            assertion = {
                'id': assertion_data['id'],
                'rawId': base64.urlsafe_b64decode(assertion_data['rawId']),
                'response': {
                    'authenticatorData': base64.urlsafe_b64decode(
                        assertion_data['response']['authenticatorData']
                    ),
                    'clientDataJSON': base64.urlsafe_b64decode(
                        assertion_data['response']['clientDataJSON']
                    ),
                    'signature': base64.urlsafe_b64decode(
                        assertion_data['response']['signature']
                    )
                },
                'type': assertion_data['type']
            }
            
            # Add userHandle if present
            if assertion_data['response'].get('userHandle'):
                assertion['response']['userHandle'] = base64.urlsafe_b64decode(
                    assertion_data['response']['userHandle']
                )
            
            # Verify the authentication
            verification = verify_authentication_response(
                credential=assertion,
                expected_challenge=challenge,
                expected_origin=self.origin,
                expected_rp_id=self.rp_id,
                credential_public_key=base64.urlsafe_b64decode(credential_record['public_key']),
                credential_current_sign_count=credential_record['sign_count']
            )
            
            if not verification.verified:
                return {'success': False, 'message': 'Authentication verification failed'}
            
            # Update sign count
            self._update_credential_sign_count(
                assertion_data['id'], 
                verification.new_sign_count
            )
            
            # Clean up challenge
            self._remove_challenge(challenge_key, 'authentication')
            
            # Get user data
            user_data = self._get_user_by_email(credential_record['email'])
            
            # Generate session token
            session_token = self._create_session(user_data)
            
            return {
                'success': True,
                'message': 'Authentication successful',
                'user': {
                    'email': user_data['email'],
                    'first_name': user_data.get('first_name', ''),
                    'user_id': user_data['user_id']
                },
                'sessionToken': session_token
            }
            
        except Exception as e:
            logger.error(f"Authentication verification failed: {e}")
            return {'success': False, 'message': 'Authentication verification failed'}
    
    def _generate_user_id(self, email: str) -> str:
        """Generate deterministic user ID from email"""
        # Use the same logic as the existing user ID generator
        from scripts.user_id_generator.user_id_generator import generate_user_id
        return generate_user_id(email)
```

## Implementation Commands and Scripts

### Email Migration Command
```bash
# Migrate existing user to email-based login
mao migrate --username seanivore --email sean@august.style

# Batch migrate multiple users
mao migrate --batch --input users_migration.json

# Check migration status
mao migrate --status
```

### Passkey Management Commands
```bash
# Setup passkey for current user
mao passkey --setup

# List passkey status
mao passkey --status

# Remove passkey (with backup authentication required)
mao passkey --remove

# Test passkey functionality
mao passkey --test
```

### API Key Management Commands
```bash
# Add API key through secure prompt
mao apikey --add anthropic

# List configured API keys (shows only metadata)
mao apikey --list

# Test API key connectivity
mao apikey --test anthropic

# Remove API key
mao apikey --remove openai
```

---

*This comprehensive implementation document provides the foundation for building a modern, secure, and emotionally intelligent authentication system that transforms the MAO user experience while maintaining the powerful functionality that makes it unique*