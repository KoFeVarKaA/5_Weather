import pytest
from unittest.mock import Mock, patch
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

from . import views
from .models import Locations
from .views import MainView

# Create your tests here.
class TestApiResponceProcessing(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.location = Locations.objects.create(
            name="Moscow",
            longitude=37.6173,
            latitude=55.7558
        )
        self.location.user_id.add(self.user)
        self.view = MainView()

    @patch("requests.get")
    @patch("weather.views.cache.set")
    def test_successful_api_request(self, mock_cache_set: Mock, mock_get: Mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Moscow"}
        mock_get.return_value = mock_response

        request = self.factory.get("/weather/")
        request.user = self.user

        location, _ = views._process_response(mock_response)
        self.assertEqual("Moscow", location["name"])

        response = self.view.get(request)
        self.assertEqual(response.status_code, 200)
    
    
    @pytest.fixture(params=[400, 401, 403, 404, 429, 500, 502, 503])
    def status_code(request):
        return request.param

    def test_api_exeptions(self):
        mock_response = Mock()
        mock_response.status_code = self.status_code

        _, message = views._process_response(mock_response)
        self.assertIsNotNone(message)