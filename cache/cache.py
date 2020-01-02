import json
import re
import os.path
import os

# ----------------- python cache json -----------------

def _hash(request):
    return re.sub(r'\W|[0-9]+', '', request.get_full_path().replace('page', ''))

def _path(request):
    return 'cache/storage/{}.json'.format(_hash(request))

def _size(file_path):
    return os.stat(file_path).st_size or 0

def store(request, data):
    try:
        with open(_path(request), 'w') as f:
            json.dump(data, f)
    except:
        return {}

def get(request):
    try:
        file_path = _path(request)
        if (not os.path.exists(file_path) or _size(file_path) == 0):
            return {}
        with open(file_path, 'r') as f:
            return json.load(f)
        return {}
    except:
        return {}

def delete(request):
    pass
