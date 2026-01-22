from django.shortcuts import redirect
from datetime import datetime
import uuid
import os
os.makedirs('logs', exist_ok=True)

class SecureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        path = request.path
        user = request.session.get('username', 'guest')
        auth = request.session.get('is_authenticated', False)

        PROTECTED_PATHS = [
            '/profilesecure',
            '/createcar',
            '/readcar',
            '/updatecar',
            '/deletecar',
            '/searchcar',
            '/api/',
        ]

        # 🔐 proteksi halaman secure
        if any(path.startswith(p) for p in PROTECTED_PATHS) and not auth:
            self.write_log(request_id, path, user, 'INTRUDER')
            return redirect('/signin/')

        if auth:
            self.write_log(request_id, path, user, 'HTTPAccess')
        else:
            self.write_log(request_id, path, user, 'GUEST')
        response = self.get_response(request)
        return response

    def write_log(self, uuid, path, user, key):
        with open('logs/secure.log', 'a') as f:
            f.write(f'{datetime.now()} | {uuid} | {key} | {path} | {user}\n')
