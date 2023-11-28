from flask import request


# 需要修改
def check_csrf_token(request):
    csrf_token = request.headers.get("X-CSRF-Token")

    # 在这里进行比较
    return csrf_token == "your_expected_csrf_token"  # 这里只是示例
