"""
Bug and Test Case Analysis System MVP
FastAPI backend with folder-based workflow for JIRA XML processing
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import shutil
from typing import List, Dict, Any

app = FastAPI(title="Bug Analysis System", version="1.0.0")

# Configuration
SOURCE_FOLDER = "source_folder"
TARGET_FOLDER = "target_folder"
STATIC_FOLDER = "static"

# Ensure directories exist
for folder in [SOURCE_FOLDER, TARGET_FOLDER, STATIC_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse(f"{STATIC_FOLDER}/index.html")

@app.post("/upload")
async def upload_jira_xml(file: UploadFile = File(...)):
    """
    Upload JIRA XML file for analysis
    Saves to source_folder with timestamp
    """
    try:
        # Validate file type
        if not file.filename.endswith('.xml'):
            raise HTTPException(status_code=400, detail="Only XML files are allowed")
        
        # Validate XML content
        content = await file.read()
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            raise HTTPException(status_code=400, detail="Invalid XML format")
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jira_{timestamp}_{file.filename}"
        filepath = os.path.join(SOURCE_FOLDER, filename)
        
        # Save file
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Create metadata file
        metadata = {
            "original_filename": file.filename,
            "upload_time": datetime.now().isoformat(),
            "file_size": len(content),
            "status": "uploaded",
            "analysis_status": "pending"
        }
        
        metadata_file = filepath.replace('.xml', '_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return JSONResponse({
            "status": "success",
            "message": "JIRA XML file uploaded successfully",
            "filename": filename,
            "next_step": "Manual analysis required - check cursor_prompts.md for templates"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/results")
async def get_results():
    """
    Poll target_folder for analysis results
    Returns list of completed analyses with download links
    """
    try:
        results = []
        
        if not os.path.exists(TARGET_FOLDER):
            return JSONResponse({"results": []})
        
        # Scan target folder for result files
        for filename in os.listdir(TARGET_FOLDER):
            if filename.endswith('.json'):
                filepath = os.path.join(TARGET_FOLDER, filename)
                try:
                    with open(filepath, 'r') as f:
                        result_data = json.load(f)
                    
                    # Check for associated Robot Framework file
                    robot_file = filepath.replace('.json', '.robot')
                    has_robot_file = os.path.exists(robot_file)
                    
                    results.append({
                        "filename": filename,
                        "result_data": result_data,
                        "has_robot_file": has_robot_file,
                        "download_links": {
                            "json": f"/download/{filename}",
                            "robot": f"/download/{filename.replace('.json', '.robot')}" if has_robot_file else None
                        }
                    })
                    
                except Exception as e:
                    print(f"Error reading result file {filename}: {e}")
                    continue
        
        return JSONResponse({
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get results: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files from target_folder"""
    try:
        filepath = os.path.join(TARGET_FOLDER, filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            filepath,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.get("/status")
async def get_status():
    """Get system status and folder contents"""
    try:
        source_files = []
        target_files = []
        
        # Count source files
        if os.path.exists(SOURCE_FOLDER):
            source_files = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith('.xml')]
        
        # Count target files
        if os.path.exists(TARGET_FOLDER):
            target_files = os.listdir(TARGET_FOLDER)
        
        return JSONResponse({
            "status": "running",
            "source_folder": {
                "path": SOURCE_FOLDER,
                "file_count": len(source_files),
                "files": source_files[:10]  # Show first 10 files
            },
            "target_folder": {
                "path": TARGET_FOLDER,
                "file_count": len(target_files),
                "files": target_files[:10]  # Show first 10 files
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Bug Analysis System...")
    print(f"Source folder: {SOURCE_FOLDER}")
    print(f"Target folder: {TARGET_FOLDER}")
    print("Navigate to http://localhost:8000 to access the web interface")
    uvicorn.run(app, host="0.0.0.0", port=8000)