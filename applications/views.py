import json

from django.db           import transaction
from django.http         import JsonResponse
from django.views        import View

from applications.models import Application, ResumeApplication


class ApplicationView(View):
    def post(self, request, job_position_id):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                
                users_id   = data['user_id']
                resumes_id = data['resume_id']
                
                application, is_applied = Application.objects.get_or_create(
                    users_id            = users_id,
                    job_positions_id    = job_position_id,
                    application_status  = 'application_complete',
                )
                
                if not is_applied:
                    return JsonResponse({'message' : 'application already existed'}, status=400)
                
                resumes_application = []
                for resume_id in resumes_id:
                    result = ResumeApplication(applications_id=application.id, resumes_id=resume_id)
                    resumes_application.append(result)
                    
                ResumeApplication.objects.bulk_create(resumes_application)
                
                return JsonResponse({'message' : 'application success'}, status=201) 

        except KeyError as e:
            return JsonResponse({'message' : 'key error ' + str(e).replace("'", '')}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'json decode error'}, status=400)