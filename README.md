# zoompan-api
이 프로젝트는 이미지를 입력받아 왼쪽에서 오른쪽으로 패닝되는 9:16 비율의 동영상을 생성하는 API 서비스입니다. FFmpeg을 사용하여 이미지를 처리하고, FastAPI를 통해 HTTP 인터페이스를 제공합니다.

## 기능
- 임의의 해상도 이미지를 9:16 비율로 자동 크롭
- 왼쪽에서 오른쪽으로 부드러운 패닝 효과 적용
- 사용자 지정 동영상 길이 설정 가능
- 로컬 실행 및 Docker 컨테이너 지원

## 프로젝트 구조

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

## API서버 실행
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker로 실행
### Docker 이미지 빌드
```bash
docker build -t zoompan-api .
```

### Docker 컨테이너 실행
```bash
docker run -d --name zoompan-container -p 8000:80 zoompan-api
```
이제 API는 `http://localhost:8000`에서 접근할 수 있습니다.
