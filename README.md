# Bank of Rasa - Banking Agent

A conversational AI agent built with Rasa 3.x that helps customers with banking inquiries. The agent uses FlowPolicy to handle structured conversations and can provide information about the bank, answer questions, and assist with basic banking tasks.

## Project Structure

```
RasaFinanceAgent/
├── actions/                    # Custom action implementations
│   ├── __init__.py             # Python package initialization
│   └── actions.py              # Custom actions (e.g., session_start)
├── data/                        # Training data and flow definitions
│   ├── flows.yml               # User flows (conversation flows)
│   └── patterns.yml            # Pattern flows (system flows)
├── config.yml                  # Rasa configuration (pipeline, policies)
├── credentials.yml              # Channel credentials
├── domain.yml                  # Domain definition (slots, responses, actions)
├── endpoints.yml               # Action server and external service endpoints
└── README.md                   # This file
```

### Key Files Explained

- **`config.yml`**: Defines the pipeline and dialogue policies. Uses `FlowPolicy` for flow-based conversations.
- **`domain.yml`**: Contains all responses, actions, and slot definitions. This is where you define what the bot can say.
- **`data/flows.yml`**: Defines user-facing conversation flows. Each flow represents a conversation path the bot can take.
- **`data/patterns.yml`**: Defines system-level pattern flows (e.g., chitchat, clarification).
- **`actions/actions.py`**: Custom Python actions that can perform logic, API calls, or complex operations.
- **`endpoints.yml`**: Configuration for the action server and other external services.

## Prerequisites

- **Python 3.8, 3.9, 3.10, or 3.11** (Python 3.11 recommended)
- **pip** (Python package installer)
- **Virtual environment tool** (venv is included with Python 3.3+)

## Installation

### Step 1: Clone or Navigate to the Project

```bash
cd /path/to/RasaFinanceAgent
```

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate project dependencies:

**On macOS/Linux:**
```bash
python3 -m venv venv
```

**On Windows:**
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

### Step 4: Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### Step 5: Install Rasa

Install Rasa and its dependencies:

```bash
pip install rasa
```

This will install Rasa along with all required dependencies. The installation may take a few minutes.

### Step 6: Verify Installation

Verify that Rasa is installed correctly:

```bash
rasa --version
```

You should see the Rasa version number displayed. 3.15 is the latest.

### Step 7: Train the Model

Train the Rasa model with your current configuration:

```bash
rasa train
```

This will process your flows, domain, and configuration files to create a trained model. The model will be saved in the `models/` directory.

## Running the Agent

The Rasa agent requires two servers to run: the action server and the Rasa server.

### Start the Action Server (Terminal 1)

The action server handles custom Python actions:

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the action server
rasa run actions
```

You should see output indicating the action server is running on `http://0.0.0.0:5055`.

**Keep this terminal window open.**

### Start the Rasa Server (Terminal 2)

Open a new terminal window and start the Rasa server with the interactive inspector:

```bash
# Navigate to the project directory
cd /path/to/RasaFinanceAgent

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the Rasa server
rasa inspect
```

You should see output indicating the server is running on `http://localhost:5005`.

### Access the Inspector

1. Open your web browser
2. Navigate to the URL shown in the terminal (typically `http://localhost:5005`)
3. You'll see the Rasa Inspector interface where you can chat with your agent

## Deactivating the Virtual Environment

When you're done working, you can deactivate the virtual environment:

```bash
deactivate
```

The `(venv)` prefix will disappear from your terminal prompt.

## Adding a New Flow with One Message Step

This guide walks you through adding a simple banking Q&A flow. For example, let's create a flow that answers "What are your opening hours?"

### Step 1: Add the Response to `domain.yml`

Open `domain.yml` and add a new response under the `responses:` section:

```yaml
responses:
  utter_greet:
    - text: "Welcome to the Bank of Rasa! How can I help you today?"

  utter_bank_address:
    - text: "The Bank of Rasa is located at Schönhauser Allee 175, 10119 Berlin."

  utter_opening_hours:                    # Add this new response
    - text: "Our bank is open Monday to Friday from 9:00 AM to 5:00 PM, and Saturday from 10:00 AM to 2:00 PM. We are closed on Sundays."

  utter_free_chitchat_response:
    - text: "placeholder"
      # ... rest of the response
```

### Step 2: Add the Flow to `data/flows.yml`

Open `data/flows.yml` and add your new flow:

```yaml
flows:
  bank_address:
    description: Provide the bank's address to users who ask for it.
    steps:
      - action: utter_bank_address

  opening_hours:                           # Add this new flow
    description: Provide the bank's opening hours to users who ask for them.
    steps:
      - action: utter_opening_hours
```

**Flow Structure:**
- **`opening_hours`**: The flow name (use lowercase with underscores)
- **`description`**: A description of what the flow does. The LLM uses this to determine when to trigger the flow.
- **`steps`**: A list of steps the flow will execute
  - **`action: utter_opening_hours`**: The response action to execute

### Step 3: Retrain the Model

After making changes to flows or domain, you need to retrain:

```bash
rasa train
```

### Step 4: Restart Servers

1. **Restart the Action Server** (if you modified `actions.py`):
   - Stop the action server (Ctrl+C)
   - Run `rasa run actions` again

2. **Restart the Rasa Server** (if needed):
   - Stop the Rasa server (Ctrl+C)
   - Run `rasa inspect` again

### Step 5: Test Your Flow

In the Rasa Inspector, try asking:
- "What are your opening hours?"
- "When are you open?"
- "What time does the bank open?"

The FlowPolicy will automatically route these questions to your `opening_hours` flow based on the description and user intent.

## Example: Complete Banking Q&A Flow

Here's a complete example of adding a flow for "What services do you offer?"

**1. Add to `domain.yml`:**
```yaml
  utter_bank_services:
    - text: "We offer a wide range of banking services including checking and savings accounts, loans, mortgages, investment services, and online banking. How can I help you with any of these?"
```

**2. Add to `data/flows.yml`:**
```yaml
  bank_services:
    description: Provide information about the banking services offered.
    steps:
      - action: utter_bank_services
```

**3. Retrain and test:**
```bash
rasa train
```

## Flow Types

### Simple Response Flow (One Message)
Use this pattern for simple Q&A where you just need to provide information:

```yaml
flow_name:
  description: What the flow does (used by LLM to route users here)
  steps:
    - action: utter_response_name
```

### Multi-Step Flow
For flows that need to collect information or perform multiple actions:

```yaml
flow_name:
  description: Collect user information and provide response
  steps:
    - collect: slot_name          # Collect a slot value
    - action: custom_action       # Run a custom action
    - action: utter_response      # Send a response
```

## Custom Actions

If you need to perform logic, API calls, or complex operations, create a custom action in `actions/actions.py`:

```python
class ActionCustomAction(Action):
    def name(self) -> Text:
        return "action_custom_action"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your logic here
        dispatcher.utter_message(text="Your response")
        return []
```

Don't forget to:
1. Add the action name to `domain.yml` under `actions:`
2. Register it in `endpoints.yml` (already configured if using `actions_module: "actions"`)

## Troubleshooting

- **Flow not triggering?** Make sure the description in `flows.yml` clearly describes when the flow should be used. The LLM uses this to route users.
- **Action not found?** Ensure the action is listed in `domain.yml` under `actions:` and the action server is running.
- **Changes not taking effect?** Remember to retrain (`rasa train`) and restart the action server if you modified `actions.py`.

## Next Steps

- Add more banking Q&A flows using the same pattern
- Create flows that collect user information (e.g., account number, amount)
- Implement custom actions for complex operations (e.g., checking account balance, processing transactions)
- Customize the chitchat responses in `patterns.yml`

## Resources

- [Rasa Documentation](https://rasa.com/docs/)
- [Rasa FlowPolicy Guide](https://rasa.com/docs/rasa/flows/)
- [Rasa Custom Actions](https://rasa.com/docs/rasa/custom-actions/)
