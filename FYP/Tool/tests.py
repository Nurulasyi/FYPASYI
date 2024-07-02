# Tool/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Tool.models import Asset, UserResult, ToolResult
from django.conf import settings
import tempfile

class ToolViewsTestCase(TestCase):
    def setUp(self):
        # Setup a client to make requests
        self.client = Client()
        
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/home.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/signup.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/login.html')

    def test_add_asset_view(self):
        response = self.client.get(reverse('add_asset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/add_asset.html')

        # Test POST request
        post_data = {
            'goal_pentest': 1,
            'type_software': 1,
            'platform': 1,
            'type_password_attack': 1,
            'hash_type': 0
        }
        response = self.client.post(reverse('add_asset'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(Asset.objects.filter(user=self.user).exists())

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/dashboard.html')

    def test_user_results_view(self):
        response = self.client.get(reverse('user_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/user_results.html')

    def test_historyresults_view(self):
        response = self.client.get(reverse('historyresults'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/historyresults.html')

    def test_delete_tool_result(self):
        # Create a tool result
        tool_result = ToolResult.objects.create(user=self.user, tool_name="Nmap", result="Test result")
        
        # Delete the tool result
        response = self.client.post(reverse('delete_tool_result', args=[tool_result.id]))
        self.assertRedirects(response, reverse('historyresults'))
        self.assertFalse(ToolResult.objects.filter(id=tool_result.id).exists())
        
    def test_hydra_view(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"password1\npassword2\n")
        temp_file.close()
        with open(temp_file.name) as password_file:
            response = self.client.post(reverse('hydra'), {
                'target_service': 'http-get',
                'target_ip': '127.0.0.1',
                'username': 'testuser',
                'password_list': password_file.read()
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('password_strengths', response.context)

    def test_medusa_view(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"password1\npassword2\n")
        temp_file.close()
        with open(temp_file.name) as password_file:
            response = self.client.post(reverse('medusa'), {
                'target_ip': '127.0.0.1',
                'username': 'testuser',
                'password_list': password_file.read(),
                'protocol': 'ssh'
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)

    def test_nmap_view(self):
        response = self.client.post(reverse('Nmap'), {
            'target_ip': '127.0.0.1',
            'scan_type': 'sS'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)

    def test_wfuzz_view(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"FUZZ\nadmin\n")
        temp_file.close()
        with open(temp_file.name) as wordlist_file:
            response = self.client.post(reverse('wfuzz'), {
                'target_url': 'http://localhost/FUZZ',
                'wordlist': wordlist_file.read()
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)