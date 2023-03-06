from django.test import TestCase

# Create your tests here.

class SimpleTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_notifications_page_status_code(self):
        response = self.client.get('/notificaciones/')
        self.assertEqual(response.status_code, 200)
        
    def test_analysis_page_status_code(self):
        response = self.client.get('/analisis/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page_status_code(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_status_code(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
    def test_logout_page_status_code(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
    
    
