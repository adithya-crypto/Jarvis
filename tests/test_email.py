"""Tests for email agent."""
import unittest


class TestEmailAgent(unittest.TestCase):

    def test_check_email_returns_config_message(self):
        from automation.email_agent import check_email
        result = check_email()
        self.assertIn("not yet configured", result)

    def test_send_email_returns_config_message(self):
        from automation.email_agent import send_email
        result = send_email("to@test.com", "Subject", "Body")
        self.assertIn("not yet configured", result)

    def test_summarize_inbox_returns_config_message(self):
        from automation.email_agent import summarize_inbox
        result = summarize_inbox()
        self.assertIn("not yet configured", result)


if __name__ == "__main__":
    unittest.main()
