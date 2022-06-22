import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from companies.models import Company, Position, Subcategory
from core.utils       import query_debugger


class JobPositionListView(View):
    @query_debugger
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
                q |= Q(position__icontains = search)
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

        except KeyError:
            return JsonResponse({'message' : 'key error'}, status=400)
            

class JobPositionDetailView(View):
    @query_debugger
    def get(self, request, job_position_id):
        try:
            position = Position.objects\
                               .select_related('companies')\
                               .exclude(status='deleted')\
                               .get(id=job_position_id)

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
                    'other_job_positions' : [other_position.id for other_position in company.position_set.all() if other_position.id != position.id],
                }
            ]

            return JsonResponse({'result' : result}, status=200)
        
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'position not existed'}, status=400)


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
                technology     = technology,
                status         = status,
                defaults       = {
                    'position'     : position,
                    'compensation' : compensation,
                    'description'  : description,
                    'due_date'     : due_date
                },
            )
            
            if not is_created:
                return JsonResponse({'message' : 'equal position already existed'}, status=400)
            
            return JsonResponse({'message' : 'new position created'}, status=201)
    
        except KeyError:
            return JsonResponse({'message' : 'key error'}, status=400)
        except TypeError:
            return JsonResponse({'message' : 'type error'}, status=400)
        except Company.DoesNotExist:
            return JsonResponse({'message' : 'company not existed'}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'message' : 'subcategory not existed'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'json decode error'}, status=400)
    

    def patch(self, request):
        try:
            data = json.loads(request.body)
            
            position_id    = data.get('position_id', None)
            subcategory_id = data.get('subcategory_id', None)
            
            if not position_id or not subcategory_id:
                return JsonResponse({'message' : 'position id or subcategory id is required'}, status=400)
            
            position_instance = Position.objects.get(id=position_id)
            
            company_id = data.get('company_id', position_instance.companies_id)
            
            if position_instance.companies_id != company_id:
                return JsonResponse({'message' : 'you cannot change company id'}, status=400)
            
            
            position_instance.subcategories = Subcategory.objects.get(id=subcategory_id)
            position_instance.title         = data.get('title', position_instance.title)
            position_instance.position      = data.get('job_position', position_instance.position)
            position_instance.compensation  = data.get('job_compensation', position_instance.compensation)
            position_instance.description   = data.get('description', position_instance.description)
            position_instance.technology    = data.get('technology', position_instance.technology)
            position_instance.due_date      = data.get('due_date', position_instance.due_date)
            position_instance.status        = data.get('status', position_instance.status)
            
            position_instance.save()

            return JsonResponse({'message' : 'update success'}, status=200)
            
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'position not existed'}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'message' : 'subcategory not existed'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'json decode error'}, status=400)
    
    # soft_delete
    def delete(self, request):     
        try:
            data = json.loads(request.body)
            
            position_id = data.get('position_id', None)
            
            if not position_id:
                return JsonResponse({'message' : 'position id is required'}, status=400)
            
            position_instance = Position.objects.get(id=position_id)
            
            if position_instance.status == 'deleted':
                return JsonResponse({'message' : 'position already deleted'}, status=400)
            
            position_instance.status = 'deleted'
            position_instance.save()
            
            return JsonResponse({'message' : 'deletion success'}, status=200)
    
        except Position.DoesNotExist:
            return JsonResponse({'message' : 'position not existed'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'messsage' : 'json decode error'}, status=400)