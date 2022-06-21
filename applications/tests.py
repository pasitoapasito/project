from django.test         import TestCase, Client

from users.models        import User, Resume
from companies.models    import Category, Subcategory, Company, Position
from applications.models import Application, ResumeApplication


class ApplicationTest(TestCase):
    
    maxDiff = None
    
    def setUp(self):
        User.objects.create(
            id   = 1,
            name = 'user#1'
        )
        
        User.objects.create(
            id   = 2,
            name = 'user#2'
        )
        
        Resume.objects.create(
            id       = 1,
            name     = 'resume#1',
            file_url = 'https://resume#1_url.com',
            users_id = 1 
        )
        
        Resume.objects.create(
            id       = 2,
            name     = 'resume#2',
            file_url = 'https://resume#2_url.com',
            users_id = 1 
        )
        
        Resume.objects.create(
            id       = 3,
            name     = 'resume#3',
            file_url = 'https://resume#3_url.com',
            users_id = 1 
        )
        
        Resume.objects.create(
            id       = 4,
            name     = 'resume#4',
            file_url = 'https://resume#4_url.com',
            users_id = 2
        )
        
        Resume.objects.create(
            id       = 5,
            name     = 'resume#5',
            file_url = 'https://resume#5_url.com',
            users_id = 2 
        )
        
        Resume.objects.create(
            id       = 6,
            name     = 'resume#6',
            file_url = 'https://resume#6_url.com',
            users_id = 2 
        )
        
        Category.objects.create(
            id   = 1,
            name = 'test_category#1'
        )
        
        Subcategory.objects.create(
            id            = 1,
            name          = 'front-end',
            categories_id = 1
        )
        
        Subcategory.objects.create(
            id            = 2,
            name          = 'back-end',
            categories_id = 1
        )
        
        Company.objects.create(
            id       = 1,
            name     = 'test_company#1',
            country  = 'korea',
            location = 'seoul',
        )
        
        Company.objects.create(
            id       = 2,
            name     = 'test_company#2',
            country  = 'korea',
            location = 'seoul',
        )
        
        Position.objects.create(
            id               = 1,
            companies_id     = 1,
            subcategories_id = 1,
            title            = '프론트엔드 개발자 모집중!!',
            description      = 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            position         = '프론트엔드 개발자',
            technology       = 'Javascript, React',
            status           = 'under_recruitment',
            compensation     = 1000000,
            due_date         = '2022-12-31'
        )
        
        Position.objects.create(
            id               = 2,
            companies_id     = 1,
            subcategories_id = 2,
            title            = '백엔드 개발자 모집중!!',
            description      = 'test_company#1에서 백엔드를 적극 채용하고 있습니다.',
            position         = '백엔드 개발자',
            technology       = 'Python/Django',
            status           = 'under_recruitment',
            compensation     = 1500000,
            due_date         = '2022-12-31'
        )
        
        Position.objects.create(
            id               = 3,
            companies_id     = 2,
            subcategories_id = 1,
            title            = '<프론트엔드 개발자 모집중>',
            description      = 'test_company#2에서 프론트엔드를 적극 채용하고 있습니다.',
            position         = '프론트엔드 개발자',
            technology       = 'Javascript, Vue.js',
            status           = 'deleted',
            compensation     = 1000000,
            due_date         = '2022-12-31'
        )
        
        Application.objects.create(
            id                 = 1,
            users_id           = 1,
            job_positions_id   = 2,
            application_status = 'application_complete'
        )
        
        ResumeApplication.objects.create(
            applications_id = 1,
            resumes_id      = 1
        )
        
        ResumeApplication.objects.create(
            applications_id = 1,
            resumes_id      = 2
        )
        
        ResumeApplication.objects.create(
            applications_id = 1,
            resumes_id      = 3
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        Company.objects.all().delete()
        Position.objects.all().delete()
        Application.objects.all().delete()
        ResumeApplication.objects.all().delete()
        
    def test_success_apply_position(self):
        client = Client()
        data   = {
            'user_id'   : 1,
            'resume_id' : [1, 2, 3]
        }
        response = client.post('/applications/1', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'application success'})
        
    def test_fail_apply_position_due_to_application_already_existed(self):
        client = Client()
        data   = {
            'user_id'   : 1,
            'resume_id' : [1, 2, 3]
        }
        response = client.post('/applications/2', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'application already existed'})
    
    def test_fail_apply_position_due_to_application_status(self):
        client = Client()
        data   = {
            'user_id'   : 2,
            'resume_id' : [4, 5, 6]
        }
        response = client.post('/applications/3', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'you cannot apply this position'})
        
    def test_fail_apply_position_due_to_key_error(self):
        client = Client()
        data   = {
            'users_id'  : 1,
            'resume_id' : [1, 2, 3]
        }
        response = client.post('/applications/1', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'key error user_id'})
    
    
    def test_fail_apply_position_due_to_position_not_existed(self):
        client = Client()
        data   = {
            'user_id' : 1,
            'resume_id' : [1, 2, 3]
        }
        response = client.post('/applications/100', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position not existed'})