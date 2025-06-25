# 🎯 Mao v4 Quality Control Validator

Automated validation system to ensure MAO v4 maintains professional quality standards and prevents regressions.

## 🚀 Quick Start

### Installation

1. **Copy the validator code:**
   ```bash
   # Create the validator directory
   mkdir -p scripts/quality_validator
   
   # Copy the Mao Quality Validator Python code to:
   # scripts/quality_validator/mao_validator.py
   ```

2. **Run the installation script:**
   ```bash
   chmod +x scripts/quality_validator/install_validator.sh
   ./scripts/quality_validator/install_validator.sh
   ```

3. **Test the installation:**
   ```bash
   chmod +x scripts/quality_validator/test_validator.sh
   ./scripts/quality_validator/test_validator.sh
   ```

### Usage

```bash
# Run all validations
./mao-validate

# Verbose output
./mao-validate --verbose

# Specify project root
./mao-validate --project-root /path/to/mao/project
```

## 🔍 Validation Checks

The validator performs 6 comprehensive checks:

### 1. 🏗️ Tool Structure Validator
- ✅ Verifies 4-file pattern for each tool:
  - `{tool_name}.py` (logic)
  - `button_{tool_name}.py` (button generation)
  - `ui_{tool_name}.py` (display)  
  - `tool_{tool_name}.json` (configuration)
- ✅ Checks required function signatures
- ✅ Validates tool architecture compliance

### 2. 💰 Cost Function Validator
- ✅ Ensures all tools have `estimate_cost()` function
- ✅ Verifies consistent function signatures
- ✅ Detects non-standard naming patterns
- ✅ Flags missing cost estimation

### 3. ⚡ Cache Pattern Validator
- ✅ Verifies CacheManager import and usage
- ✅ Checks for duplicate cache instances
- ✅ Validates caching patterns:
  - `get_cached_analysis()` → process → `cache_content_analysis()`
- ✅ Ensures optimal performance patterns

### 4. 🔗 Import Path Validator
- ✅ Checks all import statements resolve correctly
- ✅ Detects broken references after architectural moves
- ✅ Validates file paths in JSON configurations
- ✅ Flags problematic import patterns:
  - `from orchestrator.files_api import` ❌
  - `from tools.files_api.files_api import` ✅

### 5. 📄 JSON Schema Validator
- ✅ Validates tool configuration schemas
- ✅ Checks required fields: `name`, `version`, `description`, `capabilities`
- ✅ Detects deprecated field patterns (`id` → `name`)
- ✅ Ensures consistent JSON structure

### 6. 🛡️ Error Handling Validator
- ✅ Checks error handling imports
- ✅ Validates decorator usage (`@handle_errors`)
- ✅ Ensures robust error patterns
- ✅ Promotes defensive programming

## 📊 Output Examples

### ✅ Successful Validation
```
🎯 MAO v4 Quality Control Validator

Validating project at: /Users/sean/Development/modular-agent-orchestrator

🔍 Running Tool Structure Validator...
✅ Tool Structure: PASSED (11 items)

🔍 Running Cost Functions Validator...
✅ Cost Functions: PASSED (56 items)

🔍 Running Cache Patterns Validator...
✅ Cache Patterns: PASSED (44 items)

🔍 Running Import Paths Validator...
✅ Import Paths: PASSED (56 items)

🔍 Running JSON Schemas Validator...
✅ JSON Schemas: PASSED (11 items)

🔍 Running Error Handling Validator...
✅ Error Handling: PASSED (44 items)

📊 DETAILED VALIDATION RESULTS
============================================================

Summary:
  Validators: 6/6 passed
  Issues: 0
  Warnings: 0

🎉 ALL VALIDATIONS PASSED!
MAO v4 meets all quality standards!

✅ Quality validation PASSED! MAO v4 is ready for production!
```

### ❌ Failed Validation
```
🎯 MAO v4 Quality Control Validator

🔍 Running Tool Structure Validator...
❌ Tool Structure: FAILED (2 issues)

🔍 Running Import Paths Validator...
❌ Import Paths: FAILED (3 issues)

📊 DETAILED VALIDATION RESULTS
============================================================

Summary:
  Validators: 4/6 passed
  Issues: 5
  Warnings: 2

❌ VALIDATION FAILED
Please fix 5 issues before proceeding

Tool Structure:
  ❌ Tool 'web_search' missing files: ui
  ❌ Tool 'text_editor': Missing estimate_cost() function in logic file

Import Paths:
  ❌ Broken import in orchestrator/mcp_hub.py:8 - from orchestrator.files_api import FilesAPIManager
  ❌ Broken import in orchestrator/agent_callback.py:35 - from orchestrator.files_api import FilesAPIManager
  ❌ Broken import in tools/web_search/button_web_search.py:12 - from tools.web_search_modular import web_search

❌ Quality validation FAILED! Please fix issues before proceeding.
```

## 🔧 Integration

### CI/CD Pipeline Integration

Add to your GitHub Actions workflow:

```yaml
name: Quality Control
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run MAO Quality Validator
        run: |
          chmod +x ./mao-validate
          ./mao-validate
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "🎯 Running MAO Quality Validation..."
./mao-validate

if [ $? -ne 0 ]; then
    echo "❌ Quality validation failed. Commit blocked."
    exit 1
fi

echo "✅ Quality validation passed. Proceeding with commit."
```

## 🎯 Quality Standards Enforced

This validator ensures MAO v4 maintains:

### ✅ **Architectural Consistency**
- All tools follow identical 4-file patterns
- Consistent import structures
- Proper separation of concerns

### ✅ **Performance Standards**
- CacheManager integration in all components
- Optimized caching patterns
- Cost estimation for budget planning

### ✅ **Reliability Standards**
- Comprehensive error handling
- Graceful degradation patterns
- Robust exception management

### ✅ **Maintainability Standards**
- Consistent function signatures
- Standardized naming conventions
- Clear JSON schema compliance

## 🚨 Common Issues & Solutions

### Issue: Missing estimate_cost() function
```python
# ❌ Bad
class MyTool:
    def __init__(self):
        pass

# ✅ Good  
class MyTool:
    def __init__(self):
        self.cache = CacheManager()
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        return 0.001  # Appropriate cost estimate
```

### Issue: Broken import after architectural moves
```python
# ❌ Bad
from orchestrator.files_api import FilesAPIManager

# ✅ Good
from tools.files_api.files_api import FilesAPIManager
```

### Issue: Missing cache integration
```python
# ❌ Bad
class MyTool:
    def process_data(self, data):
        return expensive_operation(data)

# ✅ Good
class MyTool:
    def __init__(self):
        self.cache = CacheManager()
    
    def process_data(self, data):
        cache_key = f"data|{hash(str(data))}"
        cached = self.cache.get_cached_analysis(cache_key, "data_processing")
        if cached:
            return json.loads(cached)
        
        result = expensive_operation(data)
        self.cache.cache_content_analysis(cache_key, json.dumps(result), "data_processing")
        return result
```

## 🎉 Benefits

- **🚫 Zero Regressions**: Catch quality issues before they enter the codebase
- **⚡ Faster Development**: Automated checks reduce manual review time
- **📈 Consistent Quality**: Enforces professional standards across all components
- **🔒 Production Ready**: Ensures MAO v4 maintains enterprise-grade quality
- **👥 Team Scalability**: New contributors follow established patterns automatically

## 🤝 Contributing

To add new validation checks:

1. Add a new validator method to `MAOQualityValidator` class
2. Register it in the `run_all_validations()` method
3. Test with the test suite
4. Update this README with the new check

## 📝 License

This validation system is part of MAO v4 and follows the same license terms.

---

**Made with 💎 by the MAO v4 standardization team**

*Ensuring professional quality, one validation at a time!* 🚀