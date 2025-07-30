"""
JIRA XML Analysis Engine
Parses JIRA XML files and extracts structured data for test coverage analysis
"""

import xml.etree.ElementTree as ET
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
import os

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


class TestCaseDiscovery:
    """Discovers and indexes existing Robot Framework test cases"""
    
    def __init__(self, test_framework_path: str = "zfrwbot_218"):
        self.framework_path = test_framework_path
        self.test_index = {}
        self.keyword_index = {}
        self.test_file_index = {}
        
    def scan_test_framework(self) -> Dict[str, Any]:
        """
        Scan the Robot Framework test directory and build an index
        
        Returns:
            Dictionary containing indexed test cases and metadata
        """
        test_files = []
        
        # Find all .robot files
        for root, dirs, files in os.walk(self.framework_path):
            for file in files:
                if file.endswith('.robot'):
                    full_path = os.path.join(root, file)
                    test_files.append(full_path)
        
        # Parse each test file
        for test_file in test_files:
            self._index_robot_file(test_file)
        
        return {
            "total_files": len(test_files),
            "total_test_cases": len(self.test_index),
            "total_keywords": len(self.keyword_index),
            "test_index": self.test_index,
            "keyword_index": self.keyword_index,
            "file_index": self.test_file_index
        }
    
    def _index_robot_file(self, file_path: str):
        """Index a single Robot Framework file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract relative path for easier reference
            rel_path = os.path.relpath(file_path, self.framework_path)
            
            # Parse test cases
            test_cases = self._extract_test_cases(content)
            for test_name, test_info in test_cases.items():
                test_id = test_info.get('test_id', f"{rel_path}::{test_name}")
                self.test_index[test_id] = {
                    "name": test_name,
                    "file": rel_path,
                    "tags": test_info.get('tags', []),
                    "documentation": test_info.get('documentation', ''),
                    "keywords": test_info.get('keywords', [])
                }
            
            # Parse keywords
            keywords = self._extract_keywords(content)
            for keyword_name, keyword_info in keywords.items():
                keyword_id = f"{rel_path}::{keyword_name}"
                self.keyword_index[keyword_id] = {
                    "name": keyword_name,
                    "file": rel_path,
                    "documentation": keyword_info.get('documentation', ''),
                    "arguments": keyword_info.get('arguments', [])
                }
            
            # Store file metadata
            self.test_file_index[rel_path] = {
                "test_count": len(test_cases),
                "keyword_count": len(keywords),
                "suite_documentation": self._extract_suite_documentation(content),
                "tags": self._extract_force_tags(content)
            }
            
        except Exception as e:
            print(f"Error indexing file {file_path}: {str(e)}")
    
    def _extract_test_cases(self, content: str) -> Dict[str, Any]:
        """Extract test cases from Robot Framework content"""
        test_cases = {}
        
        # Find Test Cases section
        test_section_match = re.search(r'\*\*\*\s*Test\s*Cases?\s*\*\*\*', content, re.IGNORECASE)
        if not test_section_match:
            return test_cases
        
        # Get content after Test Cases section
        test_section_start = test_section_match.end()
        next_section_match = re.search(r'\*\*\*\s*\w+\s*\*\*\*', content[test_section_start:])
        test_section_end = test_section_start + next_section_match.start() if next_section_match else len(content)
        
        test_content = content[test_section_start:test_section_end]
        
        # Parse individual test cases
        lines = test_content.split('\n')
        current_test = None
        current_test_data = {}
        
        for line in lines:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Test case name (not indented)
            if line and not line[0].isspace():
                if current_test and current_test_data:
                    test_cases[current_test] = current_test_data
                
                current_test = line.strip()
                current_test_data = {
                    'tags': [],
                    'documentation': '',
                    'keywords': [],
                    'test_id': None
                }
            
            # Test case metadata (indented)
            elif current_test and line.strip():
                if '[Tags]' in line:
                    tags = re.findall(r'\[Tags\]\s*(.*)', line)
                    if tags:
                        current_test_data['tags'] = [tag.strip() for tag in tags[0].split()]
                        # Look for TLID in tags
                        for tag in current_test_data['tags']:
                            if tag.startswith('TLID-'):
                                current_test_data['test_id'] = tag
                
                elif '[Documentation]' in line:
                    doc = re.findall(r'\[Documentation\]\s*(.*)', line)
                    if doc:
                        current_test_data['documentation'] = doc[0].strip()
                
                else:
                    # Extract keywords used in test
                    keyword_match = re.match(r'\s+([A-Za-z][A-Za-z0-9\s_]+)', line)
                    if keyword_match:
                        current_test_data['keywords'].append(keyword_match.group(1).strip())
        
        # Don't forget the last test case
        if current_test and current_test_data:
            test_cases[current_test] = current_test_data
        
        return test_cases
    
    def _extract_keywords(self, content: str) -> Dict[str, Any]:
        """Extract keywords from Robot Framework content"""
        keywords = {}
        
        # Find Keywords section
        keyword_section_match = re.search(r'\*\*\*\s*Keywords?\s*\*\*\*', content, re.IGNORECASE)
        if not keyword_section_match:
            return keywords
        
        # Get content after Keywords section
        keyword_section_start = keyword_section_match.end()
        keyword_content = content[keyword_section_start:]
        
        # Parse individual keywords
        lines = keyword_content.split('\n')
        current_keyword = None
        current_keyword_data = {}
        
        for line in lines:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Stop at next section
            if re.match(r'\*\*\*\s*\w+\s*\*\*\*', line):
                break
            
            # Keyword name (not indented)
            if line and not line[0].isspace():
                if current_keyword and current_keyword_data:
                    keywords[current_keyword] = current_keyword_data
                
                current_keyword = line.strip()
                current_keyword_data = {
                    'documentation': '',
                    'arguments': []
                }
            
            # Keyword metadata (indented)
            elif current_keyword and line.strip():
                if '[Documentation]' in line:
                    doc = re.findall(r'\[Documentation\]\s*(.*)', line)
                    if doc:
                        current_keyword_data['documentation'] = doc[0].strip()
                
                elif '[Arguments]' in line:
                    args = re.findall(r'\[Arguments\]\s*(.*)', line)
                    if args:
                        current_keyword_data['arguments'] = [arg.strip() for arg in args[0].split()]
        
        # Don't forget the last keyword
        if current_keyword and current_keyword_data:
            keywords[current_keyword] = current_keyword_data
        
        return keywords
    
    def _extract_suite_documentation(self, content: str) -> str:
        """Extract suite documentation from Robot Framework file"""
        doc_match = re.search(r'Documentation\s+(.*?)(?:\n|$)', content, re.MULTILINE)
        return doc_match.group(1).strip() if doc_match else ''
    
    def _extract_force_tags(self, content: str) -> List[str]:
        """Extract Force Tags from Robot Framework file"""
        tags_match = re.search(r'Force\s+Tags\s+(.*?)(?:\n|$)', content, re.MULTILINE)
        if tags_match:
            return [tag.strip() for tag in tags_match.group(1).split()]
        return []
    
    def find_coverage_for_issue(self, issue_data: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Find existing test coverage for a JIRA issue
        
        Args:
            issue_data: JIRA issue data dictionary
            
        Returns:
            Tuple of (is_covered, coverage_details)
        """
        covered_tests = []
        
        # Extract keywords from issue
        issue_keywords = self._extract_issue_keywords(issue_data)
        
        # Search test index
        for test_id, test_info in self.test_index.items():
            score = self._calculate_coverage_score(issue_data, test_info, issue_keywords)
            
            if score > 0.5:  # Threshold for considering it covered
                covered_tests.append({
                    "test_file": test_info['file'],
                    "test_case_id": test_info.get('test_id', test_id),
                    "test_name": test_info['name'],
                    "confidence": score,
                    "coverage_description": test_info['documentation'],
                    "tags": test_info['tags']
                })
        
        # Sort by confidence score
        covered_tests.sort(key=lambda x: x['confidence'], reverse=True)
        
        return len(covered_tests) > 0, covered_tests
    
    def _extract_issue_keywords(self, issue_data: Dict[str, Any]) -> List[str]:
        """Extract searchable keywords from JIRA issue"""
        keywords = []
        
        # Extract from title and description
        text_content = f"{issue_data.get('title', '')} {issue_data.get('description', '')}"
        
        # Technical keywords extraction
        tech_patterns = [
            r'AP\s+role',
            r'reboot',
            r'election',
            r'master',
            r'member',
            r'dedicated\s+mode',
            r'persistence',
            r'authentication',
            r'authorization',
            r'security',
            r'performance',
            r'error\s+handling',
            r'validation',
            r'configuration',
            r'upgrade',
            r'mesh',
            r'WLAN',
            r'client',
            r'connection'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            keywords.extend([match.lower() for match in matches])
        
        # Add components and labels
        keywords.extend([comp.lower() for comp in issue_data.get('components', [])])
        keywords.extend([label.lower() for label in issue_data.get('labels', [])])
        
        return list(set(keywords))  # Remove duplicates
    
    def _calculate_coverage_score(self, issue_data: Dict[str, Any], test_info: Dict[str, Any], issue_keywords: List[str]) -> float:
        """
        Calculate how well a test case covers a JIRA issue
        
        Returns:
            Score between 0.0 and 1.0
        """
        score = 0.0
        
        # Check direct issue reference in tags
        issue_key = issue_data.get('key', '')
        if issue_key in test_info.get('tags', []):
            return 1.0  # Direct reference means definitely covered
        
        # Check keyword matches in test name
        test_name_lower = test_info['name'].lower()
        for keyword in issue_keywords:
            if keyword in test_name_lower:
                score += 0.2
        
        # Check keyword matches in documentation
        doc_lower = test_info.get('documentation', '').lower()
        for keyword in issue_keywords:
            if keyword in doc_lower:
                score += 0.15
        
        # Check tag matches
        test_tags_lower = [tag.lower() for tag in test_info.get('tags', [])]
        for keyword in issue_keywords:
            if keyword in test_tags_lower:
                score += 0.1
        
        # Special boost for certain patterns
        if 'election' in issue_keywords and 'election' in test_tags_lower:
            score += 0.3
        
        if 'reboot' in issue_keywords and 'reboot' in test_name_lower:
            score += 0.3
        
        # Cap at 1.0
        return min(score, 1.0)


class TestCoverageAnalyzer:
    """Analyzes test coverage gaps based on JIRA issues"""
    
    def __init__(self):
        self.test_discovery = None
    
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
    
    def perform_coverage_analysis(self, jira_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive coverage analysis for JIRA issues
        
        Args:
            jira_data: Parsed JIRA XML data
            
        Returns:
            Analysis results with covered and uncovered issues
        """
        # Initialize test discovery if not already done
        if not self.test_discovery:
            self.test_discovery = TestCaseDiscovery()
            self.test_discovery.scan_test_framework()
        
        issues = jira_data.get("issues", [])
        covered_issues = []
        uncovered_issues = []
        coverage_gaps = []
        
        for issue in issues:
            is_covered, coverage_details = self.test_discovery.find_coverage_for_issue(issue)
            
            if is_covered:
                covered_issues.append({
                    "issue_key": issue.get('key', ''),
                    "issue_title": issue.get('title', ''),
                    "coverage_status": "Covered",
                    "existing_test_cases": coverage_details[:3]  # Top 3 matching tests
                })
            else:
                uncovered_issues.append({
                    "issue_key": issue.get('key', ''),
                    "issue_title": issue.get('title', ''),
                    "coverage_status": "Not Covered"
                })
                
                # Add to coverage gaps for test generation
                coverage_gaps.append({
                    "issue_key": issue.get('key', ''),
                    "gap_description": f"No test coverage found for: {issue.get('title', '')}",
                    "risk_level": self._assess_risk_level(issue),
                    "suggested_test": self._generate_test_suggestion(issue)
                })
        
        # Create enhanced analysis summary
        analysis_result = {
            "analysis_summary": {
                "total_issues": len(issues),
                "covered_issues": len(covered_issues),
                "uncovered_issues": len(uncovered_issues),
                "high_priority_gaps": len([g for g in coverage_gaps if g['risk_level'] == 'High']),
                "test_cases_generated": 0,  # Will be updated after generation
                "analysis_date": datetime.now().isoformat()
            },
            "covered_issues": covered_issues,
            "coverage_gaps": coverage_gaps,
            "generated_tests": []  # Will be populated by Cursor AI
        }
        
        return analysis_result
    
    def _assess_risk_level(self, issue: Dict[str, Any]) -> str:
        """Assess risk level based on issue priority and content"""
        priority = issue.get('priority', '').lower()
        
        if priority in ['critical', 'blocker', 'highest']:
            return 'High'
        elif priority in ['major', 'high']:
            return 'High'
        elif priority in ['minor', 'low']:
            return 'Low'
        else:
            return 'Medium'
    
    def _generate_test_suggestion(self, issue: Dict[str, Any]) -> str:
        """Generate test suggestion based on issue description"""
        title = issue.get('title', '')
        description = issue.get('description', '')[:200]
        
        return f"Create test case to verify: {title}. Focus on: {description}..."

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