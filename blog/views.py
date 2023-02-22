from django.http import JsonResponse


def test_cors(request):
    # JsonResponse:返回一个字典类型的json字符串
    return JsonResponse({'msg':'CORS is fun'})