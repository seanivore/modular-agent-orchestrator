  # Providers Command Notes

  - What functionality does this CLI command provide?
  - Scans /configs/providers/ directory to discover all available provider
  JSON files
  - Reads comprehensive provider metadata: display_name, description, API
  type, rate limits, capabilities
  - Shows provider-model compatibility from
  /configs/connections/providers_x_models.json
  - Displays organized provider listing with technical and UX details
  - Works as both mao --providers and /providers

  Which orchestrator files need integration?
  - Primary: manager_models.py - needs enhancement for provider discovery
  (currently expects single providers.json)
  - Architecture Fix Required: Resolve individual files vs. unified JSON
  discrepancy
  - Universal: cli_manager.py (routing), ui_terminal.py (slash commands)
  - Secondary: Provider-model connections file for compatibility display

  What manager methods will be called?
  - ModelManager.get_available_providers() - NEW method needed for
  directory scanning
  - Integration with existing provider loading logic
  - Possible helper for provider-model relationship mapping

  What UI patterns are needed for display?
  - Provider cards: display_name, description, API type
  - Technical details: rate limits, streaming support, base URL
  - Compatibility info: supported models, universal access indicators
  - Setup requirements: local setup, privacy level, cost optimization
  - Data structure: Essential info for UI designers, not detailed
  formatting

  Cost estimation approach (Claude Sonnet 4 costs):
  - Low cost: 0.001 (file system reading, JSON parsing, data organization)
  - No AI model calls required for basic provider listing
  - Similar to help/tools command cost profile

  Caching strategy and fingerprinting:
  - Cache duration: 15 minutes (providers change less frequently)
  - Fingerprint includes: Providers directory modification time, individual
   JSON file modification times, connections file state
  - Cache key: Combined hash of provider files + connections data for
  comprehensive invalidation
