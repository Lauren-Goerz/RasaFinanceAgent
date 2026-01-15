from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Check if bot has already sent any messages in this session
        # This prevents double greeting if action is called multiple times
        for event in reversed(tracker.events):
            # Events are dictionaries, check the 'event' field
            event_type = event.get('event') if isinstance(event, dict) else getattr(event, 'event', None)
            if event_type == 'bot':
                # Bot has already spoken, don't greet again
                return []
            # Stop checking once we hit session_started (start of this session)
            if event_type == "session_started":
                break
        
        # Send a greeting message
        dispatcher.utter_message(text="Welcome to the Bank of Rasa! How can I help you today?")

        # Return empty list - Rasa will handle session_started event automatically
        return []


