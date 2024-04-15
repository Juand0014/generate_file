import os
import zipfile
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List

app = FastAPI()

@app.post("/generateFile")
async def generate_file(data: List[dict]): 
    output_dir = './outputFile'
    zip_path = './outputFile.zip'

    if os.path.exists(zip_path):
        os.remove(zip_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open('template.txt', 'r') as file:
        template_content = file.read()

    for item in data:
        output_content = template_content.format(
            subscriber_no=item['subscriber_no'],
            unit_esn=item['unit_esn'],
            imsi=item['imsi']
        )
        
        output_file_path = os.path.join(output_dir, item['name'])
        with open(output_file_path, 'w') as output_file:
            output_file.write(output_content)

    # Create a zip file
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))
                
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    shutil.rmtree(output_dir)
    return FileResponse(path=zip_path, filename=os.path.basename(zip_path), media_type='application/octet-stream')