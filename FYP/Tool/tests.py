from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Asset, UserResult, ToolResult
from .views import load_model, preprocess_data, prepare_data, train_test_split
import pandas as pd
from django.utils import timezone

class AssetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.asset = Asset.objects.create(
            user=self.user,
            goal_pentest=1,
            type_software=1,
            platform=1,
            type_password_attack=1,
            hash_type=0
        )

    def test_asset_creation(self):
        self.assertEqual(self.asset.user.username, 'testuser')
        self.assertEqual(self.asset.goal_pentest, 1)
        self.assertEqual(self.asset.type_software, 1)
        self.assertEqual(self.asset.platform, 1)
        self.assertEqual(self.asset.type_password_attack, 1)
        self.assertEqual(self.asset.hash_type, 0)
        print("Test AssetModelTest: test_asset_creation - OK")

class UserResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_result = UserResult.objects.create(
            user=self.user,
            goal_pentest='Web Application',
            type_software='Web-based',
            platform='Windows',
            type_password_attack='Brute Force',
            hash_type='MD5',
            suggested_tool_1='Hydra',
            suggested_tool_2='Nmap'
        )

    def test_user_result_creation(self):
        self.assertEqual(self.user_result.user.username, 'testuser')
        self.assertEqual(self.user_result.goal_pentest, 'Web Application')
        self.assertEqual(self.user_result.type_software, 'Web-based')
        self.assertEqual(self.user_result.platform, 'Windows')
        self.assertEqual(self.user_result.type_password_attack, 'Brute Force')
        self.assertEqual(self.user_result.hash_type, 'MD5')
        self.assertEqual(self.user_result.suggested_tool_1, 'Hydra')
        self.assertEqual(self.user_result.suggested_tool_2, 'Nmap')
        print("Test UserResultModelTest: test_user_result_creation - OK")

class ToolResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.tool_result = ToolResult.objects.create(
            user=self.user,
            tool_name='Hydra',
            result='Test result'
        )

    def test_tool_result_creation(self):
        self.assertEqual(self.tool_result.user.username, 'testuser')
        self.assertEqual(self.tool_result.tool_name, 'Hydra')
        self.assertEqual(self.tool_result.result, 'Test result')
        print("Test ToolResultModelTest: test_tool_result_creation - OK")

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/signup.html')
        print("Test ViewsTestCase: test_signup_view - OK")

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/login.html')
        print("Test ViewsTestCase: test_login_view - OK")

    def test_add_asset_view(self):
        response = self.client.get(reverse('add_asset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/add_asset.html')
        print("Test ViewsTestCase: test_add_asset_view - OK")

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/dashboard.html')
        print("Test ViewsTestCase: test_dashboard_view - OK")

    def test_user_results_view(self):
        response = self.client.get(reverse('user_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/user_results.html')
        print("Test ViewsTestCase: test_user_results_view - OK")

    def test_hydra_view(self):
        response = self.client.get(reverse('hydra'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/hydra.html')
        print("Test ViewsTestCase: test_hydra_view - OK")

    def test_medusa_view(self):
        response = self.client.get(reverse('medusa'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/medusa.html')
        print("Test ViewsTestCase: test_medusa_view - OK")

    def test_nmap_view(self):
        response = self.client.get(reverse('Nmap'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/nmap.html')
        print("Test ViewsTestCase: test_nmap_view - OK")

    def test_wfuzz_view(self):
        response = self.client.get(reverse('wfuzz'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/wfuzz.html')
        print("Test ViewsTestCase: test_wfuzz_view - OK")

    def test_result_view(self):
        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/result.html')
        print("Test ViewsTestCase: test_result_view - OK")

    def test_history_results_view(self):
        response = self.client.get(reverse('historyresults'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/historyresults.html')
        print("Test ViewsTestCase: test_history_results_view - OK")

    def test_delete_tool_result_view(self):
        tool_result = ToolResult.objects.create(user=self.user, tool_name='Test Tool', result='Test result')
        response = self.client.post(reverse('delete_tool_result', args=[tool_result.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        print("Test ViewsTestCase: test_delete_tool_result_view - OK")

class ModelTrainingTestCase(TestCase):
    def setUp(self):
        # Create sample data
        data = {
            'goal_pentest': ['Web Application', 'Network', 'Cloud'],
            'type_software': ['Web-based', 'Mobile', 'Network'],
            'platform': ['Windows', 'Linux', 'MacOS'],
            'type_password_attack': ['Brute Force', 'Dictionary', 'Hybrid'],
            'hash_type': ['MD5', 'SHA-1', 'SHA-256'],
            'suggest': [0, 1, 2]
        }
        self.df = pd.DataFrame(data)
        self.df = preprocess_data(self.df)
        self.X, self.y = prepare_data(self.df)
        
    def test_model_training(self):
        model = train_test_split(self.X, self.y)
        self.assertIsNotNone(model)
        print("Test ModelTrainingTestCase: test_model_training - OK")

    def test_model_loading(self):
        model = load_model()
        self.assertIsNotNone(model)
        print("Test ModelTrainingTestCase: test_model_loading - OK")
        
# Integration tests
class IntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_add_and_view_asset(self):
        response = self.client.post(reverse('add_asset'), {
            'goal_pentest': 1,
            'type_software': 1,
            'platform': 1,
            'type_password_attack': 1,
            'hash_type': 0
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('user_results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Application')
        self.assertContains(response, 'Web-based')
        print("Test IntegrationTestCase: test_add_and_view_asset - OK")

    def test_full_workflow(self):
        self.client.post(reverse('add_asset'), {
            'goal_pentest': 1,
            'type_software': 1,
            'platform': 1,
            'type_password_attack': 1,
            'hash_type': 0
        })

        data = {
            'goal_pentest': ['Web Application', 'Network', 'Cloud'],
            'type_software': ['Web-based', 'Mobile', 'Network'],
            'platform': ['Windows', 'Linux', 'MacOS'],
            'type_password_attack': ['Brute Force', 'Dictionary', 'Hybrid'],
            'hash_type': ['MD5', 'SHA-1', 'SHA-256'],
            'suggest': [0, 1, 2]
        }
        df = pd.DataFrame(data)
        df = preprocess_data(df)
        X, y = prepare_data(df)
        model = train_test_split(X, y)
        self.assertIsNotNone(model)
        print("Test IntegrationTestCase: test_full_workflow - model training OK")

        loaded_model = load_model()
        self.assertIsNotNone(loaded_model)
        print("Test IntegrationTestCase: test_full_workflow - model loading OK")

        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tool/result.html')
        print("Test IntegrationTestCase: test_full_workflow - OK")
