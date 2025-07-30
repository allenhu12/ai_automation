# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Bug and Test Case Analysis System** that combines AI-powered analysis with web-based interfaces to analyze test reports, identify coverage gaps, and generate new test cases automatically.

## System Architecture

The system follows a 3-tier architecture:

1. **Frontend**: React/Vue web application for file uploads and results display
2. **Backend**: Django-based API server that processes test/bug reports 
3. **Analysis Engine**: MCP (Model Context Protocol) integration for AI-powered analysis

Key components:
- **File Processing Service**: Handles test report and bug report uploads
- **MCP Client Integration**: Connects to AI services for intelligent analysis
- **Test Case Generator**: Creates Robot Framework test files
- **Results Presentation**: Web UI for analysis results and test downloads

## Development Stack

- **Backend**: Django with PostgreSQL database
- **Frontend**: React application with file upload capabilities
- **Testing Framework**: Robot Framework for generated test cases
- **AI Integration**: Model Context Protocol (MCP) for analysis capabilities
- **File Processing**: XML parsing for test reports, text processing for bug reports

## Key Design Decisions

### MCP Integration Strategy
The system uses MCP (Model Context Protocol) to connect Django backend with AI capabilities. The Django backend acts as an MCP client, sending analysis requests to an MCP server that provides:
- Test coverage analysis
- Bug classification
- Gap identification between bugs and test coverage
- Automated test case generation

### File Processing Flow
1. Users upload test reports (XML) and bug reports (text files)
2. Django processes and parses files to extract structured data
3. Processed data sent to MCP server for AI analysis
4. Results formatted and presented via web interface
5. Generated Robot Framework test files available for download

## Current State

This project is in the **design and planning phase**. The repository currently contains:
- Comprehensive system design document (`Claude-Test Case Analysis System Design.md`)
- Project structure planning and architecture decisions
- No implementation code yet - ready for development phase

## Next Development Steps

Based on the design document, the implementation should follow this order:
1. Set up Django backend with basic API endpoints
2. Implement file upload and processing services
3. Create MCP client integration
4. Build React frontend for file uploads and results display
5. Implement Robot Framework test generation
6. Add database models for storing analysis results

## File Structure (Planned)

The design document suggests this structure:
```
bug_test_analyzer/
├── backend/ (Django)
│   ├── api/
│   ├── services/
│   ├── models/
│   └── mcp_client/
├── frontend/ (React)
│   ├── components/
│   ├── services/
│   └── utils/
└── mcp_server/
    ├── analyzers/
    └── generators/
```

## Special Considerations

- **MCP Server Architecture**: The system requires careful consideration of whether to build a custom MCP server or integrate with existing AI services
- **File Processing**: System must handle various test report formats (XML, text) and extract meaningful data for analysis
- **Robot Framework Integration**: Generated test cases must be valid Robot Framework syntax
- **Scalability**: Design supports both local development and cloud deployment scenarios

## Working Locations

- The "/Users/hubo/workspace/git-depot/AI_automation/.claude/" is the working location for the current AI_automation project