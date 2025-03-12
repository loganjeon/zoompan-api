import os
import shutil
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from video_processor import VideoProcessor
import tempfile

app = FastAPI(title="Zoompan Video Generator API")

# 임시 디렉토리 생성
TEMP_DIR = os.path.join(tempfile.gettempdir(), "zoompan_api")
os.makedirs(TEMP_DIR, exist_ok=True)

# VideoProcessor 인스턴스 생성
video_processor = VideoProcessor(temp_dir=TEMP_DIR)

@app.post("/generate-video/", summary="Generate a panning video from an image")
async def generate_video(
    file: UploadFile = File(...),
    duration: Optional[int] = 3
):
    """
    이미지 파일을 업로드하여 왼쪽에서 오른쪽으로 패닝되는 동영상을 생성합니다.
    이미지 해상도를 자동으로 파싱하고 9:16 비율로 크롭합니다.
    
    - **file**: 입력 이미지 파일
    - **duration**: 동영상 길이(초), 기본값 3초
    
    Returns:
        생성된 동영상 파일
    """
    # 지원되는 이미지 형식 확인
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(status_code=400, detail="지원되는 이미지 형식은 PNG, JPG, JPEG, WEBP입니다.")
    
    try:
        # 임시 파일로 저장
        temp_image_path = os.path.join(TEMP_DIR, f"temp_{file.filename}")
        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 동영상 생성
        output_path, output_resolution = video_processor.create_panning_video(
            temp_image_path, 
            duration=duration
        )
        
        # 임시 이미지 파일 삭제
        os.remove(temp_image_path)
        
        # 파일 응답 반환
        return FileResponse(
            path=output_path, 
            media_type="video/mp4", 
            filename=f"panning_video.mp4"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"동영상 생성 중 오류가 발생했습니다: {str(e)}")

@app.on_event("shutdown")
def cleanup():
    """서버 종료 시 임시 파일 정리"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

