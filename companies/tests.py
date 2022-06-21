from django.test      import TestCase, Client

from companies.models import Category, Subcategory, Company, Position


class JobPositionListTest(TestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
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
            description      = 'test_company#2에서 프론트엔드를 적극 채용하고 있습니다!!.',
            position         = '프론트엔드 개발자',
            technology       = 'Javascript, React, Vue.js',
            status           = 'under_recruitment',
            compensation     = 700000,
            due_date         = '2022-12-31'
        )
        
        Position.objects.create(
            id               = 4,
            companies_id     = 2,
            subcategories_id = 2,
            title            = '<백엔드 개발자 모집중>',
            description      = 'test_company#2에서 백엔드를 적극 채용하고 있습니다!!.',
            position         = '백엔드 개발자',
            technology       = 'Javascript, Node.js',
            status           = 'under_recruitment',
            compensation     = 2000000,
            due_date         = '2022-12-31'
        )
        
    def test_success_display_position_list(self):
        client   = Client()
        response = client.get('/companies/positions')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "results": [
                    {
                        "id": 4,
                        "company_name": "test_company#2",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "백엔드 개발자",
                        "job_compensation": 2000000,
                        "technology": "Javascript, Node.js"
                    },
                    {
                        "id": 3,
                        "company_name": "test_company#2",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "프론트엔드 개발자",
                        "job_compensation": 700000,
                        "technology": "Javascript, React, Vue.js"
                    },
                    {
                        "id": 2,
                        "company_name": "test_company#1",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "백엔드 개발자",
                        "job_compensation": 1500000,
                        "technology": "Python/Django"
                    },
                    {
                        "id": 1,
                        "company_name": "test_company#1",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "프론트엔드 개발자",
                        "job_compensation": 1000000,
                        "technology": "Javascript, React"
                    }
                ]
            }
        )
    
    def test_success_display_search_filter_position_list(self):
        client   = Client()
        response = client.get('/companies/positions?search=Python')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "results": [
                    {
                        "id": 2,
                        "company_name": "test_company#1",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "백엔드 개발자",
                        "job_compensation": 1500000,
                        "technology": "Python/Django"
                    }
                ]
            }
        )
        
    def test_success_display_search_sort_filter_position_list(self):
        client   = Client()
        response = client.get('/companies/positions?search=Javascript&sort=job_compensation')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "results": [
                    {
                        "id": 4,
                        "company_name": "test_company#2",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "백엔드 개발자",
                        "job_compensation": 2000000,
                        "technology": "Javascript, Node.js"
                    },
                    {
                        "id": 1,
                        "company_name": "test_company#1",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "프론트엔드 개발자",
                        "job_compensation": 1000000,
                        "technology": "Javascript, React"
                    },
                    {
                        "id": 3,
                        "company_name": "test_company#2",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "프론트엔드 개발자",
                        "job_compensation": 700000,
                        "technology": "Javascript, React, Vue.js"
                    }
                ]
            }
        )
        
    def test_fail_display_position_list_due_to_key_error(self):
        client   = Client()
        response = client.get('/companies/positions?sort=liked')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "key error"})
        

class JobPositionDetailTest(TestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
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
        
    def test_success_display_position_detail(self):
        client   = Client()
        response = client.get('/companies/position/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result": [
                    {
                        "id": 1,
                        "company_name": "test_company#1",
                        "country": "korea",
                        "location": "seoul",
                        "job_position": "프론트엔드 개발자",
                        "job_compensation": 1000000,
                        "technology": "Javascript, React",
                        "description": "test_company#1에서 프론트엔드를 적극 채용하고 있습니다.",
                        "other_job_positions": [
                            2
                        ]
                    }
                ]
            }
        )
        
    def test_fail_display_position_detail_due_to_position_id(self):
        client   = Client()
        response = client.get('/companies/position/100')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "position not existed"})
        

class JobPositionTest(TestCase):
    
    maxDiff = None
    
    def setUp(self):
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
            id               = 3,
            companies_id     = 2,
            subcategories_id = 1,
            title            = '<프론트엔드 개발자 모집중>',
            description      = 'test_company#2에서 프론트엔드를 적극 채용하고 있습니다.',
            position         = '프론트엔드 개발자',
            technology       = 'Javascript, Vue.js',
            status           = 'under_recruitment',
            compensation     = 1000000,
            due_date         = '2022-12-31'
        )
        
        Position.objects.create(
            id               = 4,
            companies_id     = 2,
            subcategories_id = 2,
            title            = '<백엔드 개발자 모집중>',
            description      = 'test_company#2에서 백엔드를 적극 채용하고 있습니다.',
            position         = '백엔드 개발자',
            technology       = 'Javascript, Node.js',
            status           = 'deleted',
            compensation     = 1000000,
            due_date         = '2022-12-31'
        )
        
    def tearDown(self):
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        Company.objects.all().delete()
        Position.objects.all().delete()
                
    def test_success_create_new_position(self):
        client = Client()
        data   = {
            'company_id'      : 1,
            'subcategory_id'  : 2,
            'title'           : '<백엔드 채용공고>',
            'job_position'    : '백엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 백엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Python/Django',
            'due_date'        : '2022-12-31',
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'new position created'})
        
    def test_fail_create_new_position_due_to_equal_position_already_existed(self):
        client = Client()
        data   = {
            'company_id'      : 1,
            'subcategory_id'  : 1,
            'title'           : '프론트엔드 개발자 모집중!!',
            'job_position'    : '프론트엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Javascript, React',
            'due_date'        : '2022-12-31',
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'equal position already existed'})
    
    def test_fail_create_new_position_due_to_company_id(self):
        client = Client()
        data   = {
            'company_id'      : 3,
            'subcategory_id'  : 1,
            'title'           : '프론트엔드 개발자 모집중!!',
            'job_position'    : '프론트엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Javascript, React',
            'due_date'        : '2022-12-31',
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'company not existed'})
        
    def test_fail_create_new_position_due_to_subcategory_id(self):
        client = Client()
        data   = {
            'company_id'      : 2,
            'subcategory_id'  : 3,
            'title'           : '프론트엔드 개발자 모집중!!',
            'job_position'    : '프론트엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Javascript, React',
            'due_date'        : '2022-12-31',
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'subcategory not existed'})
        
    def test_fail_create_new_position_due_to_key_error(self):
        client = Client()
        data   = {
            'company_id'      : 2,
            'subcategory_id'  : 1,
            'title'           : '프론트엔드 개발자 모집중!!',
            'job_position'    : '프론트엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Javascript, React',
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'key error'})
        
    def test_fail_create_new_position_due_to_type_error(self):
        client = Client()
        data   = {
            'company_id'      : 2,
            'subcategory_id'  : 1,
            'title'           : '프론트엔드 개발자 모집중!!',
            'job_position'    : '프론트엔드 개발자',
            'job_compensation': 1000000,
            'description'     : 'test_company#1에서 프론트엔드를 적극 채용하고 있습니다.',
            'technology'      : 'Javascript, React',
            'due_date'        : 20221231,
            'status'          : 'under_recruitment'
        }
        response = client.post('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'type error'})
    
    def test_success_update_position(self):
        client = Client()
        data   = {
            'company_id'       : 1,
            'position_id'      : 1,
            'subcategory_id'   : 1,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'update success'})
        
    def test_fail_update_position_due_to_no_position_id(self):
        client = Client()
        data   = {
            'company_id'       : 1,
            'subcategory_id'   : 1,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position id or subcategory id is required'})
       
    def test_fail_update_position_due_to_position_id_not_existed(self):
        client = Client()
        data   = {
            'company_id'       : 1,
            'position_id'      : 100,
            'subcategory_id'   : 1,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position not existed'})   
    
    def test_fail_update_position_due_to_subcategory_id_not_existed(self):
        client = Client()
        data   = {
            'company_id'       : 1,
            'position_id'      : 1,
            'subcategory_id'   : 100,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'subcategory not existed'})
    
    def test_fail_update_position_due_to_no_subcategory_id(self):
        client = Client()
        data   = {
            'company_id'       : 1,
            'position_id'      : 1,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position id or subcategory id is required'})
    
    def test_fail_update_position_due_to_changed_company_id(self):
        client = Client()
        data   = {
            'company_id'       : 2,
            'position_id'      : 1,
            'subcategory_id'   : 1,
            'job_compensation' : 1500000,
            'due_date'         : '2023-03-31'
        }
        response = client.patch('/companies/position', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'you cannot change company id'})
    
    def test_success_delete_position(self):
        client = Client()
        data   = {
            'position_id' : 3 
        }
        response = client.delete('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'deletion success'})
    
    def test_fail_delete_position_due_to_no_position_id(self):
        client = Client()
        data   = {}
        
        response = client.delete('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position id is required'})
        
    def test_fail_delete_position_due_to_already_deleted_position(self):
        client = Client()
        data   = {
            'position_id' : 4
        }
        response = client.delete('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'position already deleted'})
        
    def test_fail_delete_position_due_to_position_id_not_existed(self):
        client = Client()
        data   = {
            'position_id' : 100
        }
        response = client.delete('/companies/position', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'position not existed'})