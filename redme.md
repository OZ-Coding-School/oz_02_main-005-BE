

python manage.py runserver

python manage.py makemigrations members
python manage.py migrate

회원관련(로그인, 소셜로그인등) : 김창규

새로운 Django 앱 생성
모델 정의
마이그레이션 생성 및 적용
Django의 내장 인증 시스템 사용
로그인 뷰 생성
소셜 로그인 구현

docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate

docker-compose exec app python manage.py createsuperuser

run exec

Account: ck
Member email: ck@gmail.com
Display name: kim
Password: 
Password (again): 