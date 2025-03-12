import os
import uuid
import ffmpeg
import tempfile
import shutil
from pathlib import Path
import argparse

class VideoProcessor:
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def create_panning_video(self, image_path, duration=3):
        """
        이미지를 받아 왼쪽에서 오른쪽으로 패닝하는 동영상을 생성합니다.
        이미지 해상도를 자동으로 파싱하고 9:16 비율로 크롭합니다.
        
        Args:
            image_path: 입력 이미지 경로
            duration: 동영상 길이(초)
        
        Returns:
            생성된 동영상 파일 경로, 출력 해상도 (width, height)
        """
        # 고유한 출력 파일 이름 생성
        output_filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(self.temp_dir, output_filename)
        
        try:
            # 이미지 정보 가져오기
            probe = ffmpeg.probe(image_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            img_width = int(video_info['width'])
            img_height = int(video_info['height'])
            
            # 9:16 비율에 맞는 출력 해상도 결정
            # 원본 이미지 비율에 따라 적절한 출력 해상도 계산
            if img_width / img_height > 9/16:  # 이미지가 더 넓은 경우
                # 높이를 기준으로 너비 계산
                output_height = min(1280, img_height)  # 최대 높이 제한
                output_width = int(output_height * 9/16)
            else:  # 이미지가 더 좁거나 같은 경우
                # 너비를 기준으로 높이 계산
                output_width = min(720, img_width)  # 최대 너비 제한
                output_height = int(output_width * 16/9)
            
            # 9:16 비율의 크롭 너비 계산
            if img_width / img_height > 9/16:  # 이미지가 더 넓은 경우
                crop_height = img_height
                crop_width = int(crop_height * 9/16)
            else:  # 이미지가 더 좁거나 같은 경우
                crop_width = img_width
                crop_height = int(crop_width * 16/9)
                # 크롭 높이가 이미지 높이보다 크면 조정
                if crop_height > img_height:
                    crop_height = img_height
                    crop_width = int(crop_height * 9/16)
            
            # 왼쪽에서 오른쪽으로 패닝하는 효과 생성
            # 패닝 범위 계산 (이미지 너비 - 크롭 너비)
            panning_range = max(0, img_width - crop_width)
            
            # 패닝 속도 계산 (전체 범위를 duration 시간 동안 이동)
            panning_speed = panning_range / duration if duration > 0 and panning_range > 0 else 0
            
            print(f"이미지 크기: {img_width}x{img_height}")
            print(f"크롭 크기: {crop_width}x{crop_height}")
            print(f"출력 해상도: {output_width}x{output_height}")
            print(f"패닝 범위: {panning_range}px")
            print(f"패닝 속도: {panning_speed}px/초")
            
            # 세로 중앙 위치 계산
            y_position = (img_height - crop_height) // 2
            
            # 패닝 표현식 - 작은따옴표 없이 직접 표현식 사용
            x_expr = f"min({panning_speed}*t,{panning_range})"
            
            # FFmpeg 명령어 구성
            (
                ffmpeg
                .input(image_path, loop=1, t=duration)
                .filter('fps', fps=30)
                .filter('crop', 
                        w=crop_width, 
                        h=crop_height, 
                        x=x_expr,  # 작은따옴표 제거
                        y=y_position)  # 고정된 값으로 변경
                .filter('scale', output_width, output_height)  # 출력 해상도에 맞게 조정
                .output(output_path, pix_fmt='yuv420p', vcodec='libx264')
                .overwrite_output()
                .run(quiet=True)
            )
            
            return output_path, (output_width, output_height)
        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if hasattr(e, 'stderr') and e.stderr else str(e)
            print(f"FFmpeg error: {error_message}")
            raise

# 직접 실행 코드
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='이미지를 9:16 비율로 크롭하여 패닝 동영상 생성')
    parser.add_argument('image_path', help='입력 이미지 파일 경로')
    parser.add_argument('--duration', type=int, default=3, help='동영상 길이(초), 기본값: 3')
    parser.add_argument('--output', help='출력 동영상 파일 경로, 기본값: 입력 파일명_panning.mp4')
    
    args = parser.parse_args()
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        input_name = os.path.splitext(os.path.basename(args.image_path))[0]
        output_path = f"{input_name}_panning.mp4"
    
    # 비디오 프로세서 생성 및 동영상 생성
    processor = VideoProcessor(temp_dir=os.path.dirname(output_path) or '.')
    try:
        temp_output_path, resolution = processor.create_panning_video(args.image_path, args.duration)
        
        # 임시 파일을 최종 출력 경로로 이동
        shutil.copy(temp_output_path, output_path)
        os.remove(temp_output_path)
        
        print(f"동영상이 성공적으로 생성되었습니다: {output_path}")
        print(f"해상도: {resolution[0]}x{resolution[1]}, 길이: {args.duration}초")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

