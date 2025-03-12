import os
import argparse
from video_processor import VideoProcessor

def main():
    parser = argparse.ArgumentParser(description='이미지를 9:16 비율로 크롭하여 패닝 동영상 생성')
    parser.add_argument('image_path', help='입력 이미지 파일 경로')
    parser.add_argument('--duration', type=int, default=3, help='동영상 길이(초), 기본값: 3')
    parser.add_argument('--output', help='출력 동영상 파일 경로, 기본값: 입력 파일명_panning.mp4')
    
    args = parser.parse_args()
    
    # 이미지 파일 존재 확인
    if not os.path.exists(args.image_path):
        print(f"오류: 파일 '{args.image_path}'을(를) 찾을 수 없습니다.")
        return
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        input_name = os.path.splitext(os.path.basename(args.image_path))[0]
        output_path = f"{input_name}_panning.mp4"
    
    # 출력 디렉토리 확인 및 생성
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 비디오 프로세서 생성 및 동영상 생성
    processor = VideoProcessor(temp_dir=output_dir or '.')
    try:
        temp_output_path, resolution = processor.create_panning_video(args.image_path, args.duration)
        
        # 임시 파일을 최종 출력 경로로 이동
        import shutil
        shutil.copy(temp_output_path, output_path)
        os.remove(temp_output_path)
        
        print(f"동영상이 성공적으로 생성되었습니다: {output_path}")
        print(f"해상도: {resolution[0]}x{resolution[1]}, 길이: {args.duration}초")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main()
