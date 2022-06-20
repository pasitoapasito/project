import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from companies.models import Company, Position, Subcategory


class JobPositionListView(View):
    def get(self, request):
        try:
            search     = request.GET.get('search', None)
            technology = request.GET.get('tech', None)
            sort       = request.GET.get('sort', 'new')
            
            sort_set = {
                'new' : '-created_at',
                'old' : 'created_at',
                'job_compensation' : '-compensation',
                # 'liked' : '-likes'
            }
            
            q = Q()
            
            if search:
                q |= Q(title__icontains = search)
                q |= Q(description__icontains = search)
                q |= Q(technology__icontains = search)
                q |= Q(companies__name__icontains = search)
                q |= Q(companies__description__icontains = search)
                
            if technology:
                q &= Q(technology__icontains = technology)
            
            positions = Position.objects\
                                .select_related('companies')\
                                .filter(q)\
                                .order_by(sort_set[sort])\
                                .exclude(status__in=['recruitment_ended', 'deleted'])                    
                                
            results = [
                {
                    'id'               : position.id,
                    'company_name'     : position.companies.name,
                    'country'          : position.companies.country,
                    'location'         : position.companies.location,
                    'job_position'     : position.position,
                    'job_compensation' : position.compensation,
                    'technology'       : position.technology,                
                }
            for position in positions]
            
            return JsonResponse({'results' : results}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
            

class JobPositionDetailView(View):
    def get(self, request, position_id):
        try:
            position = Position.objects\
                               .select_related('companies')\
                               .exclude(status='deleted')\
                               .get(id=position_id)

            company  = position.companies
            
            result = [
                {
                    'id'                  : position.id,
                    'company_name'        : company.name,
                    'country'             : company.country,
                    'location'            : company.location,
                    'job_position'        : position.position,
                    'job_compensation'    : position.compensation,
                    'technology'          : position.technology,
                    'description'         : position.description,
                    'other_job_positions' : [other_position.id for other_position in company.position_set.all()],
                }
            ]

            return JsonResponse({'result' : result}, status=200)
        
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_POSITON'}, status=400)


class JobPositionView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            company_id     = data['company_id']
            subcategory_id = data['subcategory_id']
            title          = data['title']
            position       = data['job_position']
            compensation   = data['job_compensation']
            description    = data['description']
            technology     = data['technology']
            due_date       = data['due_date']
            status         = data['status']
            
            company     = Company.objects.get(id=company_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            
            result, is_created = Position.objects.get_or_create(
                companies      = company,
                subcategories  = subcategory,
                title          = title,
                position       = position,
                status         = status,
                defaults       = {
                    'compensation' : compensation,
                    'description'  : description,
                    'technology'   : technology,
                    'due_date'     : due_date,
                },
            )
            
            if not is_created:
                return JsonResponse({'message' : 'ALREADY_EXISTED_EQUAL_POSITION'}, status=400)
            
            return JsonResponse({'message' : 'NEW_POSITON_CREATED' }, status=201)
    
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Company.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_COMPANY'}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_SUBCATEGORY'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
    
    def patch(self, request):
        try:
            data = json.loads(request.body)
            
            company_id = data.get('company_id', None)
            
            if company_id:
                return JsonResponse({'message' : 'CANNOT_CHANGE_COMPANY_ID'}, status=400)
            
            position_id    = data.get('position_id', None)
            subcategory_id = data.get('subcategory_id', None)
            
            if not position_id or not subcategory_id:
                return JsonResponse({'message' : 'POSITION_ID OR SUBCATEGORY_ID IS REQUIRED'}, status=400)
            
            position_instance = Position.objects.get(id=position_id)
            
            position_instance.subcategories = Subcategory.objects.get(id=subcategory_id)
            position_instance.title         = data.get('title', position_instance.title)
            position_instance.position      = data.get('job_position', position_instance.position)
            position_instance.compensation  = data.get('job_compensation', position_instance.compensation)
            position_instance.description   = data.get('description', position_instance.description)
            position_instance.technology    = data.get('technology', position_instance.technology)
            position_instance.due_date      = data.get('due_date', position_instance.due_date)
            position_instance.status        = data.get('status', position_instance.status)
            
            position_instance.save()

            return JsonResponse({'message' : 'POSITION_UPDATED'}, status=200)
            
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_POSITION'}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_SUBCATEGORY'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
    def delete(self, request):
        try:
            data = json.loads(request.body)
            
            position_id = data.get('position_id', None)
            
            if not position_id:
                return JsonResponse({'message' : 'POSITION_ID IS REQUIRED'}, status=400)
            
            position_instance = Position.objects.get(id=position_id)
            
            if position_instance.status == 'deleted':
                return JsonResponse({'message' : 'ALREADY_DELETED_POSITION'}, status=400)
            
            position_instance.status = 'deleted'
            position_instance.save()
            
            return JsonResponse({'message' : 'POSITION_DELETED'}, status=200)
    
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST_POSITION'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'messsage' : 'JSON_DECODE_ERROR'}, status=400)