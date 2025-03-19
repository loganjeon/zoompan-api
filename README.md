# zoompan-api
## 로컬에서 테스트하는 방법.
### 1. Excute 'video_processor.py'
```bash
python video_processor.py path/to/your/image.jpg --duration 5 --output output.mp4
```

### 2. Excute test script
```bash
python test_processor.py path/to/your/image.jpg --duration 5 --output output.mp4

``` 

## 추가 설명
### 1.	명령줄 인자:
- `image_path`: 필수 인자로, 입력 이미지 파일 경로를 지정합니다.
- `--duration`: 선택적 인자로, 동영상 길이(초)를 지정합니다. 기본값은 3초입니다.
- `--output`: 선택적 인자로, 출력 동영상 파일 경로를 지정합니다. 지정하지 않으면 입력 파일명에 “_panning.mp4”를 추가한 이름으로 저장됩니다.
### 2.	디버깅 정보:
- 이미지 크기, 크롭 크기, 출력 해상도, 패닝 범위, 패닝 속도 등의 정보를 콘솔에 출력하여 디버깅을 용이하게 했습니다.
### 3.	오류 처리:
- 파일이 존재하지 않는 경우, FFmpeg 오류 등 다양한 예외 상황을 처리합니다.
