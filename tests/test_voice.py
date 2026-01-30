"""Tests for voice-related modules (non-audio, logic-only tests)."""
import unittest
import re


class TestSpeechOutputCleaning(unittest.TestCase):
    """Test the text cleaning logic used in speech_output.py."""

    def _clean_text(self, text):
        """Replicate the cleaning logic from speech_output.speak()."""
        clean = text.replace("*", "").replace("#", "").replace("`", "")
        clean = re.sub(r'[^\w\s,?.!\'\"]', '', clean)
        return clean

    def test_removes_markdown_asterisks(self):
        result = self._clean_text("**bold text**")
        self.assertEqual(result, "bold text")

    def test_removes_hash_headers(self):
        result = self._clean_text("## Header")
        self.assertEqual(result, " Header")

    def test_removes_backticks(self):
        result = self._clean_text("`code`")
        self.assertEqual(result, "code")

    def test_keeps_normal_text(self):
        result = self._clean_text("Hello, how are you?")
        self.assertEqual(result, "Hello, how are you?")

    def test_removes_emojis(self):
        result = self._clean_text("Hello 🎉 World")
        self.assertNotIn("🎉", result)


class TestVoiceInputMicPriority(unittest.TestCase):
    """Test microphone selection logic."""

    def test_mic_list_accessible(self):
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        self.assertIsInstance(mics, list)
        self.assertGreater(len(mics), 0)


if __name__ == "__main__":
    unittest.main()
