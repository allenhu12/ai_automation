# Implementation Plan - AI_automation

## Project: Bug and Test Case Analysis System MVP (Updated for JIRA XML Input)

### Current Todo Status (2025-07-29 4:10 PM)

#### ✅ Completed Tasks
1. **Create HLD, PRD, and STATUS documents in current working directory** ✅
   - HLD_ruckathon2025.md created and updated for JIRA XML input
   - PRD_ruckathon2025.md created  
   - STATUS_ruckathon2025.md created

#### 🔄 Pending Tasks  
2. **Set up MVP project structure with simplified FastAPI backend** (High Priority)
   - Create main.py with folder-based FastAPI endpoints
   - Set up JIRA XML file upload handling
   - Implement source_folder → target_folder workflow

3. **Implement JIRA XML parsing and validation** (High Priority)
   - Create analysis_engine.py for JIRA XML structure
   - Parse issue keys, titles, comments, and custom fields
   - Validate XML format and extract structured data

4. **Create Cursor IDE prompt templates and manual workflow** (High Priority)
   - Create cursor_prompts.md with predefined analysis prompts
   - Define manual workflow for test coverage analysis
   - Standardize target_folder output format

### Updated Implementation Timeline (8-hour MVP)

#### Hour 1-2: Simplified FastAPI Backend
- [ ] Create main.py with folder-based FastAPI structure
- [ ] Implement JIRA XML upload endpoint (/upload)
- [ ] Add results polling endpoint (/results) for target_folder monitoring
- [ ] Create source_folder/ and target_folder/ directory structure
- [ ] Basic JIRA XML file validation on upload

#### Hour 3-4: JIRA XML Processing & Cursor Templates
- [ ] Build JIRA XML parser (analysis_engine.py) for structured data extraction
- [ ] Parse issue keys, titles, comments, custom fields from JIRA XML
- [ ] Create cursor_prompts.md with predefined analysis templates
- [ ] Define standardized output format for target_folder results
- [ ] Test JIRA XML parsing with real UN-12686 format data

#### Hour 5-6: Updated Web Interface
- [ ] Create static/index.html with JIRA XML upload interface
- [ ] Add XML file validation and drag-and-drop functionality
- [ ] Implement target_folder polling for results display
- [ ] Show structured JIRA data (issue key, title, priority) in results
- [ ] Add download functionality for generated Robot Framework tests

#### Hour 7-8: Manual Workflow & Demo
- [ ] Test end-to-end JIRA XML workflow (upload → source_folder → manual analysis → target_folder)
- [ ] Demonstrate manual Cursor IDE analysis process with predefined prompts
- [ ] Generate sample Robot Framework test cases for uncovered JIRA bugs
- [ ] Complete 10-minute demo with real JIRA data (UN-12686 format)

### Updated Success Criteria
- [ ] Parse JIRA XML files successfully (UN-12686 format with structured data)
- [ ] Implement folder-based workflow (source_folder → target_folder)
- [ ] Manual Cursor IDE analysis process with predefined prompt templates
- [ ] Generate valid Robot Framework test cases for uncovered JIRA bugs
- [ ] Complete 10-minute end-to-end demo showing JIRA XML processing
- [ ] Show test coverage analysis workflow with real zfrwbot_218 integration
- [ ] Demonstrate immediate value through structured JIRA bug analysis

### Updated File Structure
```
mvp_bug_analysis/
├── main.py                 # Simplified FastAPI backend (~100 lines)
├── analysis_engine.py      # JIRA XML parsing (~80 lines)
├── cursor_prompts.md       # Manual prompt templates (~50 lines)
├── static/
│   └── index.html          # JIRA XML upload interface (~120 lines)
├── source_folder/          # Input: JIRA XML files
├── target_folder/          # Output: Analysis results
└── README.md              # Manual workflow instructions
```

### Key Benefits of Updated Approach
- **Simplified Architecture**: No job queue complexity, direct folder-based workflow
- **Richer Input Data**: JIRA XML provides structured bug information vs simple text
- **User Control**: Manual Cursor IDE interaction allows for better analysis quality  
- **Faster Development**: Fewer components and endpoints to implement (350 lines total vs 500)
- **Better Integration**: Direct compatibility with existing JIRA bug tracking system