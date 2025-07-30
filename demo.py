#!/usr/bin/env python3
"""
Demo script for Bug and Test Case Analysis System
Tests the JIRA XML processing workflow
"""

import os
import json
from pathlib import Path
from analysis_engine import process_jira_file

def run_demo():
    """Run end-to-end demo of the system"""
    print("🚀 Bug and Test Case Analysis System Demo")
    print("=" * 50)
    
    # Setup
    demo_file = "demo_jira_sample.xml"
    source_folder = "source_folder"
    target_folder = "target_folder"
    
    # Ensure folders exist
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(target_folder, exist_ok=True)
    
    print(f"\n📁 Processing demo file: {demo_file}")
    
    if not os.path.exists(demo_file):
        print(f"❌ Demo file not found: {demo_file}")
        print("Please ensure demo_jira_sample.xml exists in the current directory")
        return
    
    try:
        # Process the JIRA XML file
        print("🔄 Processing JIRA XML...")
        result = process_jira_file(demo_file, target_folder)
        
        print(f"✅ Processing complete!")
        print(f"📊 Status: {result['status']}")
        
        if result['status'] == 'processed':
            print(f"📈 Issues found: {result['issues_found']}")
            print(f"📄 Output files created:")
            for file_type, file_path in result['output_files'].items():
                print(f"   - {file_type}: {file_path}")
            
            print(f"\n💡 Next step: {result['next_step']}")
            
            # Show content of generated files
            print("\n" + "=" * 50)
            print("📋 Generated Analysis Prompt Preview:")
            print("=" * 50)
            
            prompt_file = result['output_files']['analysis_prompt']
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r') as f:
                    content = f.read()
                    # Show first 500 characters
                    print(content[:500] + "..." if len(content) > 500 else content)
            
            print("\n" + "=" * 50)
            print("📊 Parsed JIRA Data Preview:")
            print("=" * 50)
            
            parsed_file = result['output_files']['parsed_data']
            if os.path.exists(parsed_file):
                with open(parsed_file, 'r') as f:
                    data = json.load(f)
                    print(f"Issues found: {len(data.get('issues', []))}")
                    for i, issue in enumerate(data.get('issues', [])[:2], 1):
                        print(f"\nIssue {i}:")
                        print(f"  Key: {issue.get('key', 'No key')}")
                        print(f"  Title: {issue.get('title', 'No title')}")
                        print(f"  Status: {issue.get('status', 'Unknown')}")
                        print(f"  Priority: {issue.get('priority', 'Unknown')}")
                        print(f"  Components: {', '.join(issue.get('components', []))}")
        
        else:
            print(f"❌ Processing failed: {result.get('error_message', 'Unknown error')}")
        
        print("\n" + "=" * 50)
        print("🎯 Manual Analysis Instructions:")
        print("=" * 50)
        print("1. Open cursor_prompts.md for analysis templates")
        print("2. Copy the generated prompt from target_folder/prompt_*.md")
        print("3. Use Cursor AI to perform the analysis")
        print("4. Save results as analysis_results_TIMESTAMP.json in target_folder/")
        print("5. Optionally create corresponding .robot test files")
        
        print("\n📂 Check these folders:")
        print(f"   - source_folder/ (input files)")
        print(f"   - target_folder/ (analysis results)")
        print(f"   - static/ (web interface)")
        
        print("\n🌐 To run the web interface:")
        print("   python main.py")
        print("   Then navigate to http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

def show_system_info():
    """Show current system status"""
    print("\n📊 System Status:")
    print("-" * 30)
    
    folders = ['source_folder', 'target_folder', 'static']
    for folder in folders:
        if os.path.exists(folder):
            file_count = len(os.listdir(folder))
            print(f"📁 {folder}/: {file_count} files")
        else:
            print(f"📁 {folder}/: Not found")
    
    files = ['main.py', 'analysis_engine.py', 'cursor_prompts.md', 'static/index.html']
    print("\n📄 Core Files:")
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file}: {size} bytes")
        else:
            print(f"❌ {file}: Missing")

if __name__ == "__main__":
    show_system_info()
    run_demo()
    
    print("\n🎉 Demo complete! The system is ready for use.")