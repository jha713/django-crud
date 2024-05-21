from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post
from unittest.mock import patch

class PostViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = reverse('post-list')
        self.post_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'author': 'Test Author'
        }
        self.post_instance = Post.objects.create(**self.post_data)
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post_instance.pk})

    @patch('blog.views.is_feature_enabled', return_value=True)
    def test_list_posts_with_crud_enabled(self, mock_flag):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post_data['title'])

    @patch('blog.views.is_feature_enabled', return_value=False)
    def test_list_posts_with_crud_disabled(self, mock_flag):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post_data['title'])

    @patch('blog.views.is_feature_enabled', return_value=True)
    def test_create_post_with_crud_enabled(self, mock_flag):
        response = self.client.post(self.post_url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    @patch('blog.views.is_feature_enabled', return_value=False)
    def test_create_post_with_crud_disabled(self, mock_flag):
        response = self.client.post(self.post_url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    @patch('blog.views.is_feature_enabled', return_value=True)
    def test_update_post_with_crud_enabled(self, mock_flag):
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': 'Updated Author'
        }
        response = self.client.put(self.post_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post_instance.refresh_from_db()
        self.assertEqual(self.post_instance.title, updated_data['title'])

    @patch('blog.views.is_feature_enabled', return_value=False)
    def test_update_post_with_crud_disabled(self, mock_flag):
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': 'Updated Author'
        }
        response = self.client.put(self.post_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post_instance.refresh_from_db()
        self.assertEqual(self.post_instance.title, self.post_data['title'])

    @patch('blog.views.is_feature_enabled', return_value=True)
    def test_delete_post_with_crud_enabled(self, mock_flag):
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    @patch('blog.views.is_feature_enabled', return_value=False)
    def test_delete_post_with_crud_disabled(self, mock_flag):
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
