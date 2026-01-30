"""Tests for code generation agent."""
import unittest
from unittest.mock import patch, MagicMock
import os


class TestCodegenAgent(unittest.TestCase):

    @patch('automation.codegen_agent.requests.post')
    @patch('automation.codegen_agent.load_api_key', return_value="test-key")
    def test_generate_code_success(self, mock_key, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{'content': {'parts': [{'text': 'print("hello")'}]}}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        from automation.codegen_agent import generate_code
        result = generate_code("hello world in python")
        self.assertIn("Code generated", result)

    @patch('automation.codegen_agent.requests.post')
    @patch('automation.codegen_agent.load_api_key', return_value="test-key")
    def test_generate_code_error(self, mock_key, mock_post):
        mock_post.side_effect = Exception("API error")

        from automation.codegen_agent import generate_code
        result = generate_code("failing request")
        self.assertIn("error", result.lower())


if __name__ == "__main__":
    unittest.main()
