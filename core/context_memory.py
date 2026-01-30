"""
Context Memory - Maintains conversation history for multi-turn interactions.
"""


class ContextMemory:
    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns

    def add_exchange(self, user_input, assistant_response):
        """Add a user/assistant exchange to history."""
        self.history.append({
            "user": user_input,
            "assistant": assistant_response
        })
        # Keep only the last N turns
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def get_context_string(self):
        """Get conversation history formatted for the AI prompt."""
        if not self.history:
            return ""

        lines = []
        for exchange in self.history:
            lines.append(f"User: {exchange['user']}")
            lines.append(f"JARVIS: {exchange['assistant']}")
        return "\n".join(lines)

    def clear(self):
        """Clear conversation history."""
        self.history = []

    def get_last_exchange(self):
        """Get the most recent exchange."""
        if self.history:
            return self.history[-1]
        return None
