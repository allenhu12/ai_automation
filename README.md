# Bug and Test Case Analysis System MVP

AI-powered JIRA XML analysis system for Robot Framework test coverage gap identification.

## Quick Start

1. **Install dependencies:**
   
   **Option A - Full installation (recommended):**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Option B - If you have dependency conflicts:**
   ```bash
   pip install -r requirements-minimal.txt
   ```
   
   **Option C - Manual installation:**
   ```bash
   pip install fastapi uvicorn[standard] python-multipart
   ```

2. **Run the demo:**
   ```bash
   python demo.py
   ```

3. **Start the web server:**
   ```bash
   python main.py
   ```

4. **Access the web interface:**
   Open http://localhost:8000 in your browser

## System Architecture

```
📁 Project Structure:
├── main.py                 # FastAPI backend server
├── analysis_engine.py      # JIRA XML parser and analysis prompt generator
├── cursor_prompts.md       # Manual analysis templates for Cursor AI
├── demo.py                 # Demo script with sample data
├── static/
│   └── index.html          # Web interface for file uploads
├── source_folder/          # Input: JIRA XML files
├── target_folder/          # Output: Analysis results
└── demo_jira_sample.xml    # Sample JIRA XML for testing
```

## Workflow

### 1. Upload JIRA XML
- Use web interface at http://localhost:8000
- Drag & drop or browse for JIRA XML export files
- System validates XML format and saves to `source_folder/`

### 2. Automatic Processing
- JIRA XML is parsed and structured data extracted
- Analysis prompt is generated based on issue content
- Files saved to `target_folder/`:
  - `parsed_*.json` - Structured JIRA data
  - `prompt_*.md` - Analysis prompt for Cursor AI

### 3. Manual Analysis with Cursor AI
- Open `cursor_prompts.md` for analysis templates
- Copy generated prompt from `target_folder/prompt_*.md`
- Use Cursor AI to perform detailed analysis
- Generate Robot Framework test cases

### 4. Save Results
- Save analysis as `analysis_results_TIMESTAMP.json` in `target_folder/`
- Optionally create corresponding `.robot` test files
- Results automatically appear in web interface

## API Endpoints

- `GET /` - Web interface
- `POST /upload` - Upload JIRA XML files
- `GET /results` - Poll for analysis results
- `GET /download/{filename}` - Download generated files
- `GET /status` - System status and folder contents

## Features

### JIRA XML Processing
- ✅ Supports standard JIRA XML exports
- ✅ Extracts issues, comments, custom fields
- ✅ Handles special characters and encoding
- ✅ Validates XML format and structure

### Analysis Engine
- ✅ Generates structured analysis prompts
- ✅ 6 specialized prompt templates (security, performance, API, UI, regression)
- ✅ Robot Framework test case templates
- ✅ Integration with zfrwbot_218 conventions

### Web Interface
- ✅ Drag & drop file upload
- ✅ Real-time results polling
- ✅ Download links for generated files
- ✅ System status monitoring
- ✅ Mobile-responsive design

### Manual Workflow
- ✅ Cursor AI integration templates
- ✅ Step-by-step analysis instructions
- ✅ Quality checklist and validation
- ✅ Robot Framework test generation

## Sample Output

The system generates structured analysis results:

```json
{
  "analysis_summary": {
    "total_issues": 2,
    "high_priority_gaps": 1,
    "test_cases_generated": 3,
    "analysis_date": "2025-07-30T14:45:11.000Z"
  },
  "coverage_gaps": [
    {
      "issue_key": "UN-12686",
      "gap_description": "Missing authentication tests for special characters",
      "risk_level": "High",
      "suggested_test": "Test login with various special characters in password"
    }
  ],
  "generated_tests": [
    {
      "test_name": "Test Login With Special Characters",
      "issue_keys": ["UN-12686"],
      "priority": "High",
      "robot_code": "*** Test Cases ***..."
    }
  ]
}
```

## Integration

### zfrwbot_218 Compatibility
- Follows existing naming conventions (TLID-XXXXX)
- Uses established keyword libraries
- Maintains consistency with existing test structure
- Considers existing test data and fixtures

### Cursor AI Workflow
- Predefined prompt templates for consistent analysis
- Structured output format for easy processing
- Quality checklist for validation
- Integration instructions and best practices

## Demo

Run the included demo to see the system in action:

```bash
python demo.py
```

This processes the sample JIRA XML file and shows:
- XML parsing and data extraction
- Analysis prompt generation
- File output structure
- Manual workflow instructions

## Development

### Adding New Prompt Templates
1. Edit `cursor_prompts.md`
2. Add new template following existing format
3. Update documentation and examples

### Extending JIRA XML Support
1. Modify `analysis_engine.py`
2. Update `_parse_single_issue()` method
3. Add new field extraction logic
4. Test with various JIRA export formats

### Customizing Web Interface
1. Edit `static/index.html`
2. Modify styles, layout, or functionality
3. Update API calls if needed
4. Test responsive design

## Troubleshooting

### Common Issues

**Dependency conflicts during installation:**
- Try: `pip install -r requirements-minimal.txt`
- Or manually: `pip install fastapi uvicorn[standard] python-multipart`
- For Claude Code users: The system works with existing MCP/Claude dependencies

**Upload fails with "Invalid XML format":**
- Ensure file is valid XML
- Check for encoding issues
- Verify JIRA export format

**No results showing:**
- Check `target_folder/` for generated files
- Verify analysis was completed manually
- Refresh results page

**Server won't start:**
- Install dependencies using one of the three methods above
- Check port 8000 is available
- Verify Python version compatibility (3.8+)

### File Locations

- **Input files:** `source_folder/`
- **Analysis results:** `target_folder/`
- **Web interface:** `static/index.html`
- **Logs:** Console output from `python main.py`

## System Requirements

- Python 3.8+
- FastAPI and dependencies (see requirements.txt)
- Modern web browser for interface
- Cursor AI for manual analysis (recommended)

## License

This is an MVP system developed for Ruckathon 2025. For production use, consider additional security, scalability, and monitoring features.