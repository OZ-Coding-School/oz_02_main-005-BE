from asgiref.sync import async_to_sync

# 비동기 함수
async def async_func():
    # ...

# 동기적인 Django 뷰
def sync_view(request):
    # 비동기 함수를 동기적으로 호출
    result = async_to_sync(async_func)()