# Beeline Changelog

All notable changes to the Beeline project are documented in this file.

## [2.0.0] - 2025-10-18

### Added - Multi-Model Support

#### Major Features
- **Gemini Integration**: Added support for Google's Gemini 2.5 Flash model
  - FREE tier available (60 requests/minute)
  - Fast response times
  - Good JSON output quality
  - Model name: `gemini-2.5-flash`

- **Multi-Model API Server**: New `api_server_multimodel.py`
  - Supports both Claude and Gemini
  - Auto-select mode (prefers Gemini for cost savings)
  - Manual model selection via API parameter
  - Graceful fallback handling

- **Model Selection**: Three modes of operation
  - `"model": "auto"` - Auto-selects best available (Gemini preferred)
  - `"model": "gemini"` - Explicitly use Gemini 2.5 Flash
  - `"model": "claude"` - Explicitly use Claude 3.5 Sonnet

#### API Enhancements
- Added `model_used` field to response metadata
- Both models use same prompt template
- Consistent JSON response format across models
- Automatic markdown stripping for Gemini responses

#### Documentation
- Created `PROJECT_STATUS.md` - Current project state
- Updated `MULTI_MODEL_GUIDE.md` - Corrected model name to `gemini-2.5-flash`
- Updated `DEMO_SETUP.md` - Multi-model setup instructions
- Updated `TESTING_GUIDE.md` - Testing both models
- Created `CHANGELOG.md` - This file

### Changed

#### Model Updates
- **Claude**: Updated to `claude-3-5-sonnet-20250219` (from deprecated version)
- **Gemini**: Finalized on `gemini-2.5-flash` after testing:
  - Initially tried `gemini-pro` (not found)
  - Tried `gemini-1.5-flash` (not found)
  - Tried `gemini-2.0-flash-latest` (not supported for generateContent)
  - **Success**: `gemini-2.5-flash` works perfectly

#### Architecture
- Multi-model planner supports both LLM providers
- Unified `RoutePlanner` class works with any model
- Model-agnostic prompt engineering

### Fixed

#### Model Issues
- Fixed Gemini model name compatibility
- Fixed markdown stripping in Gemini responses
- Fixed model initialization for both providers

#### API Fixes
- Added proper error handling for missing models
- Improved fallback route generation
- Better logging for model selection

### Testing

#### Verified Working
- ✅ Gemini query parsing
- ✅ Gemini route generation
- ✅ Claude query parsing
- ✅ Claude route generation
- ✅ Auto-select mode (prefers Gemini)
- ✅ Manual model selection
- ✅ Fallback handling
- ✅ Google Maps integration
- ✅ Multi-leg route generation

#### Test Results
**Query**: "Palo Alto to Oracle Park by 7pm"
- **Model**: Gemini 2.5 Flash
- **Generated**: 3 optimized routes
  1. Direct drive (37 min, $25)
  2. Park-and-ride with Caltrain (59 min, $13)
  3. Full transit option (59 min, $9.75)
- **Status**: ✅ All routes valid and realistic

## [1.0.0] - 2025-10-17

### Added - Initial Implementation

#### Core Features
- FastAPI backend server
- Claude LLM integration for query parsing
- Google Maps API integration via MCP
- Multi-modal route planning
- Natural language query processing

#### Components
- `api_server.py` - Claude-only API server
- `mcp_server.py` - MCP WebSocket server
- `test_planner.py` - Interactive testing script
- SvelteKit frontend (basic implementation)

#### Google Maps Integration
- Geocoding API
- Directions API (driving)
- Directions API (transit)
- Real-time traffic data

#### Route Planning
- Drive + transit combinations
- Cost calculations
- Time optimization
- Carbon savings estimates
- Parking cost estimates

### Initial Documentation
- `README.md` - Project overview
- `MULTI_MODEL_GUIDE.md` - Multi-model setup
- `TESTING_GUIDE.md` - Testing instructions
- `DEMO_SETUP.md` - Demo setup guide

## Release Notes

### Version 2.0.0 Summary

This release adds multi-model support, allowing users to choose between:
- **Gemini 2.5 Flash** (FREE, fast, good quality)
- **Claude 3.5 Sonnet** (paid, excellent quality)

The auto-select feature defaults to Gemini to minimize costs while maintaining high-quality route generation. All existing functionality remains intact, with improved error handling and better documentation.

### Breaking Changes

None. The original `api_server.py` (Claude-only) still works. New multi-model server is opt-in via `api_server_multimodel.py`.

### Migration Guide

To use multi-model support:

1. Get a Gemini API key (FREE): https://makersuite.google.com/app/apikey
2. Set environment variable: `export GEMINI_API_KEY=your_key`
3. Use `api_server_multimodel.py` instead of `api_server.py`
4. Optionally specify model in requests: `{"query": "...", "model": "gemini"}`

### Known Issues

#### Gemini
- Occasionally returns markdown-wrapped JSON (auto-stripped by server)
- Free tier limited to 60 requests/minute

#### Claude
- Requires paid API credits
- May have low balance warnings (fallback routes used)

### Future Roadmap

- [ ] Additional model support (OpenAI GPT-4, etc.)
- [ ] Model performance comparison metrics
- [ ] Cost tracking per model
- [ ] Model A/B testing framework
- [ ] Frontend model selector UI
- [ ] Real-time parking API integration
- [ ] Calendar integration
- [ ] Historical route analytics

## Version History

- **2.0.0** (2025-10-18): Multi-model support (Gemini + Claude)
- **1.0.0** (2025-10-17): Initial implementation (Claude only)

---

For detailed information about each version, see the sections above.
For the current project status, see `PROJECT_STATUS.md`.
For setup instructions, see `DEMO_SETUP.md`.
