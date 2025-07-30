#!/usr/bin/env python3
"""
Test script to demonstrate coverage detection for both covered and uncovered issues
"""

import json
from datetime import datetime
from pathlib import Path
from analysis_engine import JiraXMLParser, TestCoverageAnalyzer

def create_demo_jira_xml():
    """Create a demo JIRA XML file with multiple issues"""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="0.92">
    <channel>
        <title>JIRA Issues</title>
        <item>
            <key>UN-12634</key>
            <title>AP role 'member(Fix)' lost after reboot in dedicated mode</title>
            <summary>AP role persistence issue after reboot</summary>
            <description>When AP is configured as member with fixed role in dedicated mode, 
            the role is lost after reboot. The AP should maintain its member(Fix) status 
            but reverts to different state.</description>
            <status>Open</status>
            <priority>High</priority>
            <components>Election</components>
            <labels>reboot,role_persistence,dedicated_mode</labels>
        </item>
        <item>
            <key>TLID-89974</key>
            <title>AP update AP cache database every 30 sec</title>
            <summary>AP cache update timing test</summary>
            <description>Test to verify that AP updates its cache database every 30 seconds
            to ensure election information is current.</description>
            <status>Open</status>
            <priority>Medium</priority>
            <components>Election</components>
            <labels>election,cache,timing</labels>
        </item>
        <item>
            <key>UN-99999</key>
            <title>New OAuth2 integration with external identity providers</title>
            <summary>Implement OAuth2 authentication</summary>
            <description>Add capability for users to authenticate using external OAuth2 
            providers like Google, Microsoft, and Okta.</description>
            <status>Open</status>
            <priority>High</priority>
            <components>Authentication</components>
            <labels>oauth,authentication,security</labels>
        </item>
    </channel>
</rss>"""
    
    # Save demo XML
    demo_file = "demo_jira_issues.xml"
    with open(demo_file, 'w') as f:
        f.write(xml_content)
    
    return demo_file

def test_coverage_analysis():
    """Test the enhanced coverage analysis system"""
    
    # Create demo JIRA file
    print("1. Creating demo JIRA XML file...")
    demo_file = create_demo_jira_xml()
    
    # Parse JIRA XML
    print("2. Parsing JIRA XML...")
    parser = JiraXMLParser()
    jira_data = parser.parse_jira_xml(demo_file)
    print(f"   Found {len(jira_data['issues'])} issues")
    
    # Perform coverage analysis
    print("3. Performing coverage analysis...")
    analyzer = TestCoverageAnalyzer()
    analysis_result = analyzer.perform_coverage_analysis(jira_data)
    
    # Display results
    print("\n📊 Coverage Analysis Results:")
    print("=" * 50)
    summary = analysis_result['analysis_summary']
    print(f"Total Issues: {summary['total_issues']}")
    print(f"✅ Covered Issues: {summary['covered_issues']}")
    print(f"❌ Uncovered Issues: {summary['uncovered_issues']}")
    print(f"🔥 High Priority Gaps: {summary['high_priority_gaps']}")
    
    # Show covered issues
    if analysis_result['covered_issues']:
        print("\n✅ COVERED ISSUES:")
        print("-" * 30)
        for issue in analysis_result['covered_issues']:
            print(f"\n{issue['issue_key']}: {issue['issue_title']}")
            print(f"Status: {issue['coverage_status']}")
            if issue['existing_test_cases']:
                print("Existing Tests:")
                for test in issue['existing_test_cases']:
                    print(f"  - {test['test_case_id']}: {test['test_name']}")
                    print(f"    File: {test['test_file']}")
                    print(f"    Confidence: {test['confidence'] * 100:.0f}%")
    
    # Show uncovered issues
    if analysis_result['coverage_gaps']:
        print("\n❌ UNCOVERED ISSUES (Need Test Cases):")
        print("-" * 30)
        for gap in analysis_result['coverage_gaps']:
            print(f"\n{gap['issue_key']}: {gap['gap_description']}")
            print(f"Risk Level: {gap['risk_level']}")
            print(f"Suggested: {gap['suggested_test']}")
    
    # Save results
    output_file = f"target_folder/coverage_analysis_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path("target_folder").mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(analysis_result, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Cleanup
    Path(demo_file).unlink()
    
    return analysis_result

if __name__ == "__main__":
    print("🚀 Testing Enhanced Coverage Analysis System")
    print("=" * 50)
    test_coverage_analysis()