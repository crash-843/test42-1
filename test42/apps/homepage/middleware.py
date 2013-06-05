from .models import LogEntry


class Requests:
    def process_response(self, request, response):
        entry = LogEntry(method=request.method,
                         url=request.path,
                         status=response.status_code)
        entry.save()
        return response
