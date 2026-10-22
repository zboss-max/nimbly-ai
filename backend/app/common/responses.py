from flask import request

def ok(data=None, msg='ok', status=200):
    return {'code': 0, 'msg': msg, 'data': data}, status

def fail(msg, status=400, code=None):
    return {'code': code or status, 'msg': msg, 'data': None}, status

def parse_json(schema_cls):
    """校验请求体，返回 (schema, 错误响应)"""
    try:
        return schema_cls.from_json(request.get_json(silent=True)), None
    except ValueError as e:
        return None, fail(str(e), 400)
