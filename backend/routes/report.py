from fastapi import APIRouter, HTTPException, Response
from backend.database.mongodb_sync import fs
import gridfs
from bson import ObjectId

router = APIRouter()

@router.get("/report/{file_id}")
async def get_file(file_id: str):
    try:
        object_id = ObjectId(file_id)
        
        file = fs.get(object_id)
        
        return Response(
            content=file.read(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file.filename}"}
        )
    
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))