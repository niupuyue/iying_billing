import json
from django.http import HttpResponse


def make_iying_response(body: dict):
    response = HttpResponse(json.dumps(
        body,
        ensure_ascii=False, separators=(',', ':')),
        content_type='application/json',
        status=body.get('code', 200),
    )
    return response
