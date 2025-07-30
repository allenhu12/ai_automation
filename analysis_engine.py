"""
JIRA XML Analysis Engine
Parses JIRA XML files and extracts structured data for test coverage analysis
"""

import xml.etree.ElementTree as ET
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class JiraXMLParser:
    """Parser for JIRA XML export files"""
    
    def __init__(self):
        self.supported_fields = [
            'key', 'title', 'summary', 'description', 'status', 'priority',
            'assignee', 'reporter', 'created', 'updated', 'resolution',
            'components', 'labels', 'fixVersion', 'customfields'
        ]
    
    def parse_jira_xml(self, xml_file_path: str) -> Dict[str, Any]:
        """
        Parse JIRA XML file and extract structured issue data
        
        Args:
            xml_file_path: Path to JIRA XML file
            
        Returns:
            Dictionary containing parsed JIRA data
        """
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            parsed_data = {
                "metadata": {
                    "source_file": Path(xml_file_path).name,
                    "parsed_at": datetime.now().isoformat(),
                    "parser_version": "1.0.0"
                },
                "issues": []
            }
            
            # Handle different XML structures
            issues = self._find_issues(root)
            
            for issue_element in issues:
                issue_data = self._parse_single_issue(issue_element)
                if issue_data:
                    parsed_data["issues"].append(issue_data)
            
            parsed_data["metadata"]["issue_count"] = len(parsed_data["issues"])
            return parsed_data
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse JIRA XML: {str(e)}")
    
    def _find_issues(self, root: ET.Element) -> List[ET.Element]:
        """Find issue elements in XML structure"""
        # Try common JIRA XML structures
        issues = []
        
        # Direct issues under root
        issues.extend(root.findall('.//item'))
        issues.extend(root.findall('.//issue'))
        
        # RSS-style structure
        if root.tag == 'rss':
            issues.extend(root.findall('.//item'))
        
        # Direct XML export
        if root.tag == 'issues':
            issues.extend(root.findall('issue'))
        
        return issues
    
    def _parse_single_issue(self, issue: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse a single JIRA issue element"""
        try:
            issue_data = {
                "key": "",
                "title": "",
                "summary": "",
                "description": "",
                "status": "",
                "priority": "",
                "assignee": "",
                "reporter": "",
                "created": "",
                "updated": "",
                "resolution": "",
                "components": [],
                "labels": [],
                "fixVersion": [],
                "customfields": {},
                "comments": []
            }
            
            # Extract basic fields
            issue_data["key"] = self._get_text(issue, ['key', 'title'])
            issue_data["title"] = self._get_text(issue, ['title', 'summary'])
            issue_data["summary"] = self._get_text(issue, ['summary', 'title'])
            issue_data["description"] = self._get_text(issue, ['description'])
            issue_data["status"] = self._get_text(issue, ['status'])
            issue_data["priority"] = self._get_text(issue, ['priority'])
            issue_data["assignee"] = self._get_text(issue, ['assignee'])
            issue_data["reporter"] = self._get_text(issue, ['reporter'])
            issue_data["created"] = self._get_text(issue, ['created'])
            issue_data["updated"] = self._get_text(issue, ['updated'])
            issue_data["resolution"] = self._get_text(issue, ['resolution'])
            
            # Extract arrays
            issue_data["components"] = self._get_array_values(issue, ['component', 'components'])
            issue_data["labels"] = self._get_array_values(issue, ['label', 'labels'])
            issue_data["fixVersion"] = self._get_array_values(issue, ['fixVersion', 'version'])
            
            # Extract custom fields
            issue_data["customfields"] = self._extract_custom_fields(issue)
            
            # Extract comments
            issue_data["comments"] = self._extract_comments(issue)
            
            # Only return if we have at least a key or title
            if issue_data["key"] or issue_data["title"]:
                return issue_data
            
            return None
            
        except Exception as e:
            print(f"Error parsing issue: {str(e)}")
            return None
    
    def _get_text(self, element: ET.Element, field_names: List[str]) -> str:
        """Get text content from element by trying multiple field names"""
        for field_name in field_names:
            # Try direct child
            child = element.find(field_name)
            if child is not None and child.text:
                return child.text.strip()
            
            # Try as attribute
            if element.get(field_name):
                return element.get(field_name).strip()
        
        return ""
    
    def _get_array_values(self, element: ET.Element, field_names: List[str]) -> List[str]:
        """Get array values from element"""
        values = []
        for field_name in field_names:
            # Multiple elements with same name
            elements = element.findall(field_name)
            for elem in elements:
                if elem.text:
                    values.append(elem.text.strip())
            
            # Single element with comma-separated values
            single_elem = element.find(field_name)
            if single_elem is not None and single_elem.text:
                values.extend([v.strip() for v in single_elem.text.split(',') if v.strip()])
        
        return list(set(values))  # Remove duplicates
    
    def _extract_custom_fields(self, element: ET.Element) -> Dict[str, str]:
        """Extract custom fields from JIRA issue"""
        custom_fields = {}
        
        # Look for customfields container
        customfields_elem = element.find('customfields')
        if customfields_elem is not None:
            for customfield in customfields_elem.findall('customfield'):
                field_id = customfield.get('id', '')
                field_key = customfield.get('key', '')
                
                # Get field value
                customfieldname = customfield.find('customfieldname')
                customfieldvalues = customfield.find('customfieldvalues')
                
                field_name = customfieldname.text if customfieldname is not None else field_key
                
                if customfieldvalues is not None:
                    values = []
                    for value in customfieldvalues.findall('customfieldvalue'):
                        if value.text:
                            values.append(value.text.strip())
                    
                    if field_name:
                        custom_fields[field_name] = ', '.join(values) if values else ''
        
        return custom_fields
    
    def _extract_comments(self, element: ET.Element) -> List[Dict[str, str]]:
        """Extract comments from JIRA issue"""
        comments = []
        
        comments_elem = element.find('comments')
        if comments_elem is not None:
            for comment in comments_elem.findall('comment'):
                comment_data = {
                    "author": comment.get('author', ''),
                    "created": comment.get('created', ''),
                    "text": comment.text.strip() if comment.text else ''
                }
                comments.append(comment_data)
        
        return comments

class TestCoverageAnalyzer:
    """Analyzes test coverage gaps based on JIRA issues"""
    
    def generate_analysis_prompt(self, jira_data: Dict[str, Any], robot_test_data: str = None) -> str:
        """
        Generate analysis prompt for Cursor AI based on JIRA data
        
        Args:
            jira_data: Parsed JIRA XML data
            robot_test_data: Optional Robot Framework test data
            
        Returns:
            Formatted prompt for manual analysis
        """
        issues = jira_data.get("issues", [])
        
        prompt = f"""# Test Coverage Analysis for JIRA Issues

## Overview
Analyze the following {len(issues)} JIRA issues for test coverage gaps and generate Robot Framework test cases.

## JIRA Issues to Analyze:

"""
        
        for i, issue in enumerate(issues, 1):
            prompt += f"""
### Issue {i}: {issue.get('key', 'No Key')}
**Title**: {issue.get('title', 'No Title')}
**Status**: {issue.get('status', 'Unknown')}
**Priority**: {issue.get('priority', 'Unknown')}
**Description**: {issue.get('description', 'No Description')[:500]}...

**Components**: {', '.join(issue.get('components', []))}
**Labels**: {', '.join(issue.get('labels', []))}

"""
            
            # Add comments if available
            comments = issue.get('comments', [])
            if comments:
                prompt += "**Recent Comments**:\n"
                for comment in comments[:3]:  # Show first 3 comments
                    prompt += f"- {comment.get('author', 'Unknown')}: {comment.get('text', '')[:200]}...\n"
                prompt += "\n"
        
        prompt += f"""
## Analysis Instructions:

1. **Identify Test Scenarios**: For each issue, identify what test scenarios should exist
2. **Find Coverage Gaps**: Determine which scenarios are missing from current test suite
3. **Generate Test Cases**: Create Robot Framework test cases for missing coverage
4. **Prioritize Tests**: Rank test cases by risk and business impact

## Expected Output Format:

Save results as JSON in target_folder/ with this structure:
```json
{{
  "analysis_summary": {{
    "total_issues": {len(issues)},
    "high_priority_gaps": 0,
    "test_cases_generated": 0,
    "analysis_date": "{datetime.now().isoformat()}"
  }},
  "coverage_gaps": [
    {{
      "issue_key": "ISSUE-123",
      "gap_description": "Missing error handling test",
      "risk_level": "High",
      "suggested_test": "Test Case Description"
    }}
  ],
  "generated_tests": [
    {{
      "test_name": "Test Invalid Input Handling",
      "issue_keys": ["ISSUE-123"],
      "priority": "High",
      "robot_code": "Robot Framework test code here"
    }}
  ]
}}
```

## Robot Framework Test Template:
Use this template for generating test cases:

```robot
*** Test Cases ***
Test Case Name
    [Tags]    {{issue_key}}    {{priority}}
    [Documentation]    Test description based on JIRA issue
    
    Given Initial State
    When Action Performed  
    Then Expected Result
    
*** Keywords ***
Given Initial State
    # Setup code
    
When Action Performed
    # Test action
    
Then Expected Result
    # Verification
```

Begin analysis now.
"""
        
        return prompt

def process_jira_file(source_file_path: str, target_folder: str) -> Dict[str, Any]:
    """
    Process a JIRA XML file and generate analysis prompt
    
    Args:
        source_file_path: Path to source JIRA XML file
        target_folder: Path to target folder for results
        
    Returns:
        Processing result summary
    """
    try:
        parser = JiraXMLParser()
        analyzer = TestCoverageAnalyzer()
        
        # Parse JIRA XML
        jira_data = parser.parse_jira_xml(source_file_path)
        
        # Generate analysis prompt
        analysis_prompt = analyzer.generate_analysis_prompt(jira_data)
        
        # Create output files
        source_filename = Path(source_file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save parsed data
        parsed_data_file = Path(target_folder) / f"parsed_{source_filename}_{timestamp}.json"
        with open(parsed_data_file, 'w') as f:
            json.dump(jira_data, f, indent=2)
        
        # Save analysis prompt
        prompt_file = Path(target_folder) / f"prompt_{source_filename}_{timestamp}.md"
        with open(prompt_file, 'w') as f:
            f.write(analysis_prompt)
        
        # Create result summary
        result = {
            "status": "processed",
            "source_file": source_filename,
            "issues_found": len(jira_data.get("issues", [])),
            "output_files": {
                "parsed_data": str(parsed_data_file),
                "analysis_prompt": str(prompt_file)
            },
            "next_step": "Use Cursor AI with the generated prompt to perform manual analysis",
            "processed_at": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "processed_at": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test with sample file
    import sys
    if len(sys.argv) > 1:
        result = process_jira_file(sys.argv[1], "target_folder")
        print(json.dumps(result, indent=2))