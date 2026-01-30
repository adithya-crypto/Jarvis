"""Tests for command_router.py - verifies routing logic."""
import unittest
from unittest.mock import patch


class TestCommandRouter(unittest.TestCase):

    @patch('core.command_router.open_app')
    def test_open_chrome(self, mock_open):
        from core.command_router import route_command
        result = route_command("open chrome")
        mock_open.assert_called_with("Google Chrome")
        self.assertIn("Chrome", result)

    @patch('core.command_router.open_app')
    def test_open_vscode(self, mock_open):
        from core.command_router import route_command
        result = route_command("open vs code")
        mock_open.assert_called_with("Visual Studio Code")
        self.assertIn("Visual Studio Code", result)

    @patch('core.command_router.mute_system')
    def test_mute(self, mock_mute):
        from core.command_router import route_command
        result = route_command("mute")
        mock_mute.assert_called_once()
        self.assertIn("muted", result)

    @patch('core.command_router.unmute_system')
    def test_unmute(self, mock_unmute):
        from core.command_router import route_command
        result = route_command("unmute")
        mock_unmute.assert_called_once()
        self.assertIn("restored", result.lower())  # "Audio restored, sir."

    @patch('core.command_router.set_volume')
    def test_set_volume(self, mock_vol):
        from core.command_router import route_command
        result = route_command("set volume to 75")
        mock_vol.assert_called_with(75)
        self.assertIn("75", result)

    @patch('core.command_router.get_weather')
    def test_weather(self, mock_weather):
        mock_weather.return_value = "Sunny, temperature 72F"
        from core.command_router import route_command
        result = route_command("what's the weather like")
        mock_weather.assert_called_once()
        self.assertIn("72", result)

    def test_remember(self):
        from core.command_router import route_command
        result = route_command("remember that my favorite color is blue")
        self.assertTrue("remember" in result.lower() or "noted" in result.lower())

    def test_recall(self):
        from core.command_router import route_command
        # First remember something
        route_command("remember that my favorite color is blue")
        result = route_command("what did i tell you about my favorite color")
        self.assertIn("blue", result)

    def test_no_matching_action(self):
        from core.command_router import route_command
        result = route_command("tell me a joke about cats")
        self.assertIn("no matching action", result)

    @patch('core.command_router.search_web')
    def test_search(self, mock_search):
        mock_search.return_value = "Here is what I found: Python is great"
        from core.command_router import route_command
        result = route_command("search for python tutorials")
        mock_search.assert_called_once()
        self.assertIn("found", result.lower())

    def test_check_email_stub(self):
        from core.command_router import route_command
        result = route_command("check email")
        self.assertIn("not yet configured", result)

    def test_check_calendar_stub(self):
        from core.command_router import route_command
        result = route_command("check calendar")
        self.assertIn("not yet configured", result)

    @patch('core.command_router.start_timer')
    def test_set_timer(self, mock_timer):
        mock_timer.return_value = "Reminder set: 'Timer complete' in 5 minutes."
        from core.command_router import route_command
        result = route_command("set timer for 5 minutes")
        mock_timer.assert_called_with(5)

    @patch('core.command_router.notify')
    def test_notify(self, mock_notify):
        mock_notify.return_value = "Notification sent: JARVIS."
        from core.command_router import route_command
        result = route_command("notify take a break")
        mock_notify.assert_called_once()

    @patch('core.command_router.open_youtube')
    def test_open_youtube(self, mock_yt):
        mock_yt.return_value = "Opening YouTube."
        from core.command_router import route_command
        result = route_command("open youtube")
        mock_yt.assert_called_once()

    @patch('core.command_router.open_github')
    def test_open_github(self, mock_gh):
        mock_gh.return_value = "Opening GitHub."
        from core.command_router import route_command
        result = route_command("open github")
        mock_gh.assert_called_once()


if __name__ == "__main__":
    unittest.main()
