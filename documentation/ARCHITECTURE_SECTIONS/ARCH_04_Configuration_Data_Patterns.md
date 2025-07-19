# Configuration and Data Patterns - Delta-Only Storage and Privacy-First Design

## Introduction

MAO implements sophisticated configuration and data management patterns that prioritize user privacy, enable efficient storage through delta-only persistence, and provide comprehensive analytics while maintaining GDPR compliance. These patterns form the foundation for secure, efficient, and user-controlled data management in the LOCAL-only architecture.

## Delta-Only Storage Patterns

### Settings Manager Architecture

The settings manager implements delta-only storage, storing only changes from default configurations:

```python
# orchestrator/settings_manager.py
class SettingsManager:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.default_settings = {}
        self.user_settings = {}
        self.settings_schema = None
        
    @handle_errors
    async def load_settings_architecture(self):
        """Load complete settings architecture with schema and defaults"""
        # Load application settings schema
        schema_path = Path("configs/settings/application_settings_schema.json")
        with open(schema_path, 'r') as f:
            self.settings_schema = json.load(f)
            
        # Extract default values from schema
        self.default_settings = self.extract_defaults_from_schema(self.settings_schema)
        
        # Load user-specific delta settings
        await self.load_user_delta_settings()
        
        return {
            "schema": self.settings_schema,
            "defaults": self.default_settings,
            "user_deltas": self.user_settings
        }
        
    async def get_effective_setting(self, setting_name: str, username: str = None):
        """Get effective setting value using delta-only resolution"""
        # Start with default value
        default_value = self.default_settings.get(setting_name)
        
        # Apply system-wide overrides
        system_override = await self.get_system_override(setting_name)
        effective_value = system_override if system_override is not None else default_value
        
        # Apply user-specific delta
        if username:
            user_delta = await self.get_user_delta_setting(username, setting_name)
            if user_delta is not None:
                effective_value = user_delta
                
        return {
            "setting_name": setting_name,
            "effective_value": effective_value,
            "default_value": default_value,
            "user_delta": user_delta if username else None,
            "source": self.determine_setting_source(setting_name, username)
        }
        
    async def update_user_setting(self, username: str, setting_name: str, new_value):
        """Update user setting using delta-only storage"""
        default_value = self.default_settings.get(setting_name)
        
        # Only store delta if different from default
        if new_value == default_value:
            # Remove delta entry if reverting to default
            await self.remove_user_delta(username, setting_name)
        else:
            # Store delta value
            await self.store_user_delta(username, setting_name, new_value)
            
        # Update in-memory cache
        if username not in self.user_settings:
            self.user_settings[username] = {}
            
        if new_value == default_value:
            self.user_settings[username].pop(setting_name, None)
        else:
            self.user_settings[username][setting_name] = new_value
            
        # Cache invalidation for affected settings
        await self.invalidate_settings_cache(username, setting_name)
        
        return {
            "setting_name": setting_name,
            "new_value": new_value,
            "is_delta": new_value != default_value,
            "previous_effective": await self.get_effective_setting(setting_name, username)
        }
        
    async def store_user_delta(self, username: str, setting_name: str, delta_value):
        """Store individual user setting delta"""
        user_settings_dir = Path(f"configs/user/{username}")
        user_settings_dir.mkdir(parents=True, exist_ok=True)
        
        # Create individual setting file
        setting_file = user_settings_dir / f"{setting_name}_app_settings.json"
        
        delta_config = {
            "setting_name": setting_name,
            "user_value": delta_value,
            "timestamp": datetime.utcnow().isoformat(),
            "delta_from_default": True,
            "metadata": {
                "schema_version": self.settings_schema.get("version", "1.0"),
                "username": username,
                "setting_type": self.get_setting_type(setting_name)
            }
        }
        
        with open(setting_file, 'w') as f:
            json.dump(delta_config, f, indent=2)
            
        # Update cache
        cache_key = f"user_setting:{username}:{setting_name}"
        await self.cache_manager.set(cache_key, delta_value, "settings", ttl=3600)
```

### Dynamic Configuration Discovery

The system dynamically discovers configuration files without hardcoded mappings:

```python
async def discover_configuration_files(self, config_type: str = None):
    """Dynamically discover all configuration files"""
    config_discoveries = {
        "models": self.discover_model_configs(),
        "providers": self.discover_provider_configs(),
        "tools": self.discover_tool_configs(),
        "users": self.discover_user_configs(),
        "system": self.discover_system_configs()
    }
    
    if config_type:
        return await config_discoveries.get(config_type, lambda: {})()
    
    # Discover all configuration types
    all_configs = {}
    for discovery_type, discovery_func in config_discoveries.items():
        try:
            all_configs[discovery_type] = await discovery_func()
        except Exception as e:
            logger.warning(f"Failed to discover {discovery_type} configs: {e}")
            all_configs[discovery_type] = {}
            
    return all_configs
    
async def discover_model_configs(self):
    """Discover all model configuration files"""
    models_dir = Path("configs/models")
    discovered_models = {}
    
    for model_file in models_dir.glob("*.json"):
        try:
            with open(model_file, 'r') as f:
                model_config = json.load(f)
                
            # Validate model configuration structure
            if self.validate_model_config(model_config):
                model_name = model_file.stem
                discovered_models[model_name] = {
                    "config": model_config,
                    "file_path": str(model_file),
                    "capabilities": model_config.get("capabilities", []),
                    "provider": model_config.get("provider", "unknown"),
                    "cost_model": model_config.get("cost_model", {})
                }
                
        except Exception as e:
            logger.warning(f"Failed to load model config {model_file}: {e}")
            
    return discovered_models
    
async def discover_provider_configs(self):
    """Discover all provider configuration files"""
    providers_dir = Path("configs/providers")
    discovered_providers = {}
    
    for provider_file in providers_dir.glob("*.json"):
        try:
            with open(provider_file, 'r') as f:
                provider_config = json.load(f)
                
            provider_name = provider_file.stem
            discovered_providers[provider_name] = {
                "config": provider_config,
                "file_path": str(provider_file),
                "supported_models": provider_config.get("supported_models", []),
                "api_endpoints": provider_config.get("api_endpoints", {}),
                "authentication": provider_config.get("authentication", {})
            }
            
        except Exception as e:
            logger.warning(f"Failed to load provider config {provider_file}: {e}")
            
    return discovered_providers
```

## Privacy-First Data Architecture

### User Data Isolation

The system implements strict user data isolation with complete user control:

```python
# orchestrator/username_manager.py
class UsernameManager:
    def __init__(self):
        self.user_data_root = Path.home() / ".mao" / "users"
        self.active_users = {}
        self.session_manager = UserSessionManager()
        
    async def create_user_environment(self, username: str):
        """Create isolated user environment with privacy controls"""
        user_directory = self.get_user_directory(username)
        
        # Create user-specific directory structure
        directories = [
            "settings",      # User-specific settings deltas
            "memory",        # Personal memory and context
            "workflows",     # User workflow states
            "analytics",     # User analytics (deletable)
            "cache",         # User-specific cache
            "exports"        # Data export staging
        ]
        
        for directory in directories:
            (user_directory / directory).mkdir(parents=True, exist_ok=True)
            
        # Create user privacy manifest
        privacy_manifest = {
            "username": username,
            "created_at": datetime.utcnow().isoformat(),
            "data_retention_policy": "user_controlled",
            "gdpr_compliance": True,
            "data_categories": {
                "settings": {"deletable": True, "exportable": True},
                "memory": {"deletable": True, "exportable": True},
                "workflows": {"deletable": True, "exportable": True},
                "analytics": {"deletable": True, "exportable": True, "anonymizable": True}
            },
            "privacy_controls": {
                "data_collection": "user_controlled",
                "analytics_sharing": "disabled",
                "external_integration": "user_authorized_only"
            }
        }
        
        manifest_file = user_directory / "privacy_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(privacy_manifest, f, indent=2)
            
        return {
            "user_directory": str(user_directory),
            "privacy_manifest": privacy_manifest,
            "status": "created"
        }
        
    async def delete_user_data(self, username: str, confirmation_code: str):
        """Complete user data deletion with GDPR compliance"""
        user_directory = self.get_user_directory(username)
        
        # Verify deletion authorization
        if not await self.verify_deletion_authorization(username, confirmation_code):
            raise ValueError("Invalid deletion authorization")
            
        # Create deletion audit log
        deletion_log = {
            "username": username,
            "deletion_timestamp": datetime.utcnow().isoformat(),
            "deleted_categories": [],
            "anonymized_categories": [],
            "audit_trail": []
        }
        
        try:
            # Delete user data categories
            for category in ["settings", "memory", "workflows", "cache", "exports"]:
                category_path = user_directory / category
                if category_path.exists():
                    shutil.rmtree(category_path)
                    deletion_log["deleted_categories"].append(category)
                    deletion_log["audit_trail"].append(f"Deleted {category} at {datetime.utcnow().isoformat()}")
                    
            # Anonymize analytics data instead of deletion (preserves system insights)
            analytics_path = user_directory / "analytics"
            if analytics_path.exists():
                await self.anonymize_user_analytics(analytics_path, username)
                deletion_log["anonymized_categories"].append("analytics")
                deletion_log["audit_trail"].append(f"Anonymized analytics at {datetime.utcnow().isoformat()}")
                
            # Remove user directory
            if user_directory.exists():
                shutil.rmtree(user_directory)
                deletion_log["audit_trail"].append(f"Removed user directory at {datetime.utcnow().isoformat()}")
                
            # Log deletion in system audit
            await self.log_gdpr_deletion(deletion_log)
            
            return {
                "status": "deleted",
                "username": username,
                "deletion_log": deletion_log
            }
            
        except Exception as e:
            logger.error(f"User data deletion failed for {username}: {e}")
            raise
```

### Analytics with Privacy Protection

The system implements dual analytics with user control and anonymization:

```python
# orchestrator/user_analytics_manager.py
class UserAnalyticsManager:
    def __init__(self):
        self.user_analytics = {}
        self.system_analytics = SystemAnalyticsManager()
        
    @handle_errors
    async def record_user_activity(self, username: str, activity: dict):
        """Record user activity with privacy controls"""
        # Check user privacy preferences
        privacy_settings = await self.get_user_privacy_settings(username)
        
        if privacy_settings.get("data_collection", "enabled") == "disabled":
            # Only record anonymized system analytics
            await self.system_analytics.record_anonymous_activity(activity)
            return {"status": "anonymized_only"}
            
        # Create user activity record
        activity_record = {
            "username": username,
            "timestamp": datetime.utcnow().isoformat(),
            "activity_type": activity.get("type", "unknown"),
            "activity_data": activity,
            "session_id": await self.get_user_session_id(username),
            "privacy_level": privacy_settings.get("privacy_level", "standard")
        }
        
        # Store user analytics
        user_analytics_file = self.get_user_analytics_file(username)
        await self.append_user_analytics(user_analytics_file, activity_record)
        
        # Create anonymized version for system analytics
        anonymized_activity = await self.anonymize_activity(activity_record)
        await self.system_analytics.record_anonymous_activity(anonymized_activity)
        
        return {"status": "recorded", "privacy_level": privacy_settings.get("privacy_level")}
        
    async def anonymize_activity(self, activity_record: dict):
        """Anonymize user activity for system analytics"""
        # Remove all personally identifiable information
        anonymized = {
            "timestamp": activity_record["timestamp"],
            "activity_type": activity_record["activity_type"],
            "session_hash": hashlib.sha256(activity_record["session_id"].encode()).hexdigest()[:8],
            "user_hash": hashlib.sha256(activity_record["username"].encode()).hexdigest()[:8],
            "activity_metadata": self.extract_non_personal_metadata(activity_record["activity_data"])
        }
        
        # Ensure no personal data remains
        anonymized = self.scrub_personal_data(anonymized)
        
        return anonymized
        
    async def export_user_analytics(self, username: str, export_format: str = "json"):
        """Export user analytics for GDPR compliance"""
        user_analytics_file = self.get_user_analytics_file(username)
        
        if not user_analytics_file.exists():
            return {"status": "no_data", "message": "No analytics data found for user"}
            
        # Load all user analytics
        with open(user_analytics_file, 'r') as f:
            user_data = [json.loads(line) for line in f]
            
        # Create export package
        export_data = {
            "username": username,
            "export_timestamp": datetime.utcnow().isoformat(),
            "export_format": export_format,
            "data_summary": {
                "total_activities": len(user_data),
                "date_range": {
                    "first_activity": user_data[0]["timestamp"] if user_data else None,
                    "last_activity": user_data[-1]["timestamp"] if user_data else None
                },
                "activity_types": list(set(record["activity_type"] for record in user_data))
            },
            "analytics_data": user_data
        }
        
        # Create export file
        export_file = self.get_user_directory(username) / f"analytics_export_{int(time.time())}.{export_format}"
        
        if export_format == "json":
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2)
        elif export_format == "csv":
            # Convert to CSV format
            await self.export_to_csv(export_data, export_file)
            
        return {
            "status": "exported",
            "export_file": str(export_file),
            "export_summary": export_data["data_summary"]
        }
```

### System Analytics with Secondary Anonymization

System analytics ensure complete anonymization for privacy protection:

```python
# orchestrator/system_analytics_manager.py
class SystemAnalyticsManager:
    def __init__(self):
        self.analytics_cache = {}
        self.anonymization_keys = {}
        
    async def record_anonymous_activity(self, activity: dict):
        """Record system activity with secondary anonymization"""
        # Apply secondary anonymization to ensure no user identification
        double_anonymized = await self.apply_secondary_anonymization(activity)
        
        # Store in system analytics
        analytics_record = {
            "timestamp": double_anonymized["timestamp"],
            "activity_type": double_anonymized["activity_type"],
            "system_metrics": self.extract_system_metrics(double_anonymized),
            "performance_data": self.extract_performance_data(double_anonymized),
            "anonymization_level": "secondary",
            "record_id": str(uuid.uuid4())
        }
        
        # Append to system analytics log
        system_analytics_file = Path("system_data/analytics/system_activities.jsonl")
        system_analytics_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(system_analytics_file, 'a') as f:
            f.write(json.dumps(analytics_record) + '\n')
            
        # Update real-time metrics
        await self.update_system_metrics(analytics_record)
        
        return {"status": "recorded", "anonymization": "secondary"}
        
    async def apply_secondary_anonymization(self, primary_anonymized: dict):
        """Apply secondary anonymization to prevent any user identification"""
        # Remove or hash any remaining potentially identifying data
        secondary_anonymized = {
            "timestamp": self.round_timestamp(primary_anonymized["timestamp"]),
            "activity_type": primary_anonymized["activity_type"],
            "system_context": self.generalize_system_context(primary_anonymized),
            "performance_metrics": self.extract_performance_only(primary_anonymized)
        }
        
        # Ensure no hashes can be correlated back to users
        if "user_hash" in primary_anonymized:
            # Use rotating hash keys to prevent correlation
            session_key = self.get_session_anonymization_key()
            rehashed = hashlib.sha256(f"{primary_anonymized['user_hash']}{session_key}".encode()).hexdigest()[:6]
            secondary_anonymized["session_context"] = rehashed
            
        return secondary_anonymized
        
    def extract_system_metrics(self, activity: dict):
        """Extract only system-level metrics without user identification"""
        return {
            "resource_usage": activity.get("resource_usage", {}),
            "performance_timing": activity.get("performance_timing", {}),
            "error_counts": activity.get("error_counts", {}),
            "cache_effectiveness": activity.get("cache_stats", {})
        }
        
# Note: This represents planned system analytics functionality.
# Current implementation focuses on basic configuration management.
```

## Configuration Schema Patterns

### Application Settings Schema

The system uses comprehensive schema-driven configuration:

```python
# Application settings schema pattern
{
    "application_settings": {
        "version": "1.0",
        "last_updated": "2024-01-15T10:30:00Z",
        "settings": {
            "favorite_model": {
                "type": "string",
                "source": "dynamic_model_list",
                "fallback_options": ["claude-sonnet-4", "claude-opus-4"],
                "ui_metadata": {
                    "section": "Startup & Navigation",
                    "display_name": "Favorite Model",
                    "description": "Default model for new workflows",
                    "input_type": "select",
                    "preview_available": True
                }
            },
            "default_provider": {
                "type": "string",
                "source": "dynamic_provider_list",
                "fallback_options": ["anthropic direct", "openai direct"],
                "ui_metadata": {
                    "section": "Startup & Navigation",
                    "display_name": "Default Provider",
                    "description": "Primary AI service provider",
                    "input_type": "select"
                }
            },
            "theme": {
                "type": "string",
                "default": "dark",
                "options": ["dark", "light", "auto"],
                "ui_metadata": {
                    "section": "Interface & Experience",
                    "display_name": "Theme",
                    "description": "Visual theme for the interface",
                    "input_type": "radio"
                }
            },
            "data_collection": {
                "type": "string",
                "default": "full_insights",
                "options": ["full_insights", "basic_metrics", "no_tracking"],
                "ui_metadata": {
                    "section": "Notifications & Privacy",
                    "display_name": "Data Collection",
                    "description": "Analytics and usage data collection level",
                    "input_type": "select",
                    "privacy_impact": "high"
                }
            }
        },
        "ui_metadata": {
            "sections": [
                {
                    "name": "Startup & Navigation",
                    "description": "Application startup and default choices",
                    "icon": "startup"
                },
                {
                    "name": "Interface & Experience", 
                    "description": "User experience and interface preferences",
                    "icon": "interface"
                },
                {
                    "name": "Notifications & Privacy",
                    "description": "Communication and privacy controls",
                    "icon": "privacy"
                }
            ]
        }
    }
}
```

### Dynamic Configuration Loading

The system loads configurations dynamically with validation:

```python
async def load_configuration_with_validation(self, config_path: Path, schema_path: Path = None):
    """Load configuration with schema validation and error recovery"""
    try:
        # Load configuration file
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            
        # Load and apply schema validation if available
        if schema_path and schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                
            validation_result = await self.validate_config_against_schema(config_data, schema)
            
            if not validation_result["valid"]:
                logger.warning(f"Configuration validation failed for {config_path}")
                # Attempt to repair configuration
                repaired_config = await self.attempt_config_repair(config_data, schema, validation_result)
                config_data = repaired_config if repaired_config else config_data
                
        # Apply configuration defaults for missing values
        config_data = await self.apply_configuration_defaults(config_data)
        
        return {
            "config": config_data,
            "source": str(config_path),
            "validated": True,
            "schema_applied": schema_path is not None
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {config_path}: {e}")
        # Return default configuration
        return await self.get_default_configuration(config_path.stem)
        
    except Exception as e:
        logger.error(f"Configuration loading failed for {config_path}: {e}")
        raise
        
async def validate_config_against_schema(self, config: dict, schema: dict):
    """Validate configuration against schema with detailed reporting"""
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_required": [],
        "invalid_types": [],
        "unknown_fields": []
    }
    
    schema_settings = schema.get("application_settings", {}).get("settings", {})
    config_settings = config.get("settings", {})
    
    # Check required fields
    for setting_name, setting_schema in schema_settings.items():
        if setting_schema.get("required", False) and setting_name not in config_settings:
            validation_result["missing_required"].append(setting_name)
            validation_result["valid"] = False
            
    # Check field types and values
    for setting_name, setting_value in config_settings.items():
        if setting_name in schema_settings:
            setting_schema = schema_settings[setting_name]
            
            # Type validation
            expected_type = setting_schema.get("type", "string")
            if not self.validate_setting_type(setting_value, expected_type):
                validation_result["invalid_types"].append({
                    "field": setting_name,
                    "expected": expected_type,
                    "actual": type(setting_value).__name__
                })
                validation_result["valid"] = False
                
            # Options validation
            if "options" in setting_schema:
                if setting_value not in setting_schema["options"]:
                    validation_result["errors"].append(f"Invalid value for {setting_name}: {setting_value}")
                    validation_result["valid"] = False
        else:
            validation_result["unknown_fields"].append(setting_name)
            validation_result["warnings"].append(f"Unknown setting: {setting_name}")
            
    return validation_result
```

## Integration Guidelines

### Adding New Configuration Types

To add new configuration categories:

1. **Create Configuration Schema**
   ```json
   {
     "configuration_type": "new_category",
     "version": "1.0",
     "settings": {
       "setting_name": {
         "type": "string",
         "default": "default_value",
         "validation": "validation_rules"
       }
     }
   }
   ```

2. **Implement Discovery Pattern**
   - Add discovery function to configuration manager
   - Include validation and error handling
   - Cache configuration data appropriately

3. **Privacy Impact Assessment**
   - Determine if configuration affects user privacy
   - Implement appropriate anonymization if needed
   - Add to user data export if required

### Privacy Compliance Implementation

For GDPR compliance:

1. **User Data Categorization**
   - Identify all data types collected
   - Classify as deletable, exportable, or anonymizable
   - Implement appropriate handling for each category

2. **Anonymization Strategies**
   - Primary anonymization for user data
   - Secondary anonymization for system analytics
   - Regular rotation of anonymization keys

3. **User Control Implementation**
   - Granular privacy controls
   - Easy data export functionality
   - Complete data deletion capabilities

## Conclusion

MAO's configuration and data patterns provide a comprehensive framework for privacy-first data management with efficient delta-only storage. The system balances user privacy with system functionality through sophisticated anonymization and user control mechanisms.

The delta-only storage pattern reduces storage overhead while maintaining complete configuration flexibility. The privacy architecture ensures GDPR compliance while enabling valuable system analytics through secondary anonymization. These patterns work together to create a trustworthy, efficient configuration and data management system that respects user privacy while providing powerful functionality.