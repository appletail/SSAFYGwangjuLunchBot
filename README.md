# 개요

- 싸피 광주 캠퍼스 점심에 뭐가 나오는지 알기 위해서 만든 런치봇입니다.
- 디스코드에 봇을 추가한 후 <!점심> 명령어로 점심 메뉴를 알 수 있습니다.
- 명령어
  - !점심 : 오늘 점심
  - !월 : 이번주 월요일 점심
  - !월월 : 다음주 월요일 점심
  - !야옹 : 랜덤 고양이 사진
  - !멍멍 : 랜덤 강아지 사진

- 런치봇은 사진이 있는 경우 6번 메시지를 보내며 이는 사진을 포함시키기 위함입니다.

# 사용법

1. .env 파일 생성
2. .env파일 안에 아래 내용 추가  
   TOKEN = '디스코드 봇 토큰'  
   TODAY = '프레시밀 점심 url (마지막 날짜 제외)'  
   WEEK_URL = '프레시밀 이번주 url'  
   NEXT_WEEK_URL = '프레시밀 다음주 url'

3. lunch.py 실행
4. 디스코드에 봇 추가 후 사용

# 참고 사이트

https://yunwoong.tistory.com/212  
https://yunwoong.tistory.com/214
