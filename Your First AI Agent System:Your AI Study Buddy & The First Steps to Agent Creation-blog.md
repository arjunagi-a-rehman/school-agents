# Your First AI Agent System: Your AI Study Buddy & The First Steps to Agent Creation

## What are AI Agents?

In the ever-evolving landscape of Artificial Intelligence, "AI agents" have become a hot topic. But what exactly are they? In simple terms, an AI agent is a piece of software that can perceive its environment, make decisions, and take actions to achieve specific goals. Think of them as autonomous entities that can perform tasks on your behalf.

Unlike traditional programs that follow a rigid set of instructions, AI agents possess a degree of intelligence that allows them to be more flexible and adaptive. They can learn from their interactions, reason about complex situations, and even collaborate with other agents.

In this blog post, we'll guide you through the process of creating your very first AI agent—a "Study Buddy"—using the Google Agent Development Kit (ADK).

## Prerequisites

Before getting started, ensure you have the following:

- **Python 3.11 or higher**: This tutorial requires Python >=3.11 as specified in the project configuration. Download from [python.org](https://www.python.org/downloads/) if needed.
- **Terminal/Command Line Access**: You'll need to run commands in a terminal (e.g., Terminal on macOS/Linux, Command Prompt/PowerShell on Windows).
- **pip Installed**: Comes with Python, but ensure it's up to date by running `python -m pip install --upgrade pip`.
- **Internet Connection**: Required for installing packages and accessing AI models.
- **Google Credentials**:
  - For Vertex AI: A Google Cloud account, the gcloud CLI installed (install via [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)), and authentication set up.
  - For direct API: A Google API key obtained from [Google AI Studio](https://aistudio.google.com/).
- **Basic Knowledge**: Familiarity with basic Python concepts and command line usage will be helpful.

## Setting up Your Project with `uv` 

Before we dive into creating our agent, we need to set up our project environment. We'll be using `uv`, a fast and user-friendly package manager for Python.

1.  **Install `uv`**: If you don't have `uv` installed, open your terminal and run:
    ```bash
    pip install uv
    ```

2.  **Create a Project Directory**:
    ```bash
    mkdir school_agents
    cd school_agents
    ```

3.  **Initialize the Project with `uv`**:
    ```bash
    uv init
    ```

   This creates a `pyproject.toml` file and sets up the basic project structure. After this step, your directory will look like:

   ```
   school_agents/
   ├── pyproject.toml
   ```

4.  **Create a Virtual Environment**:
    ```bash
    uv venv
    ```

5.  **Activate the Virtual Environment**:
    -   On macOS/Linux: `source .venv/bin/activate`
    -   On Windows: `.venv\Scripts\activate`

6.  **Install Dependencies**: Add the `google-adk` library to your project.
    ```bash
    uv add google-adk
    ```

   This updates your `pyproject.toml` with the dependency and installs it in the virtual environment.

7.  **Set Up Directory Structure for Agents**:
    To organize our agents properly, create a `src/agents` directory:
    ```bash
    mkdir -p src/agents
    cd src/agents
    ```

## Creating Your Agent with `adk create`

Now that our environment is ready, let's create our "Study Buddy" agent using the ADK's command-line interface. Ensure you're in the `src/agents` directory.

```bash
adk create studdy_buddy
```

This command will create a new directory called `studdy_buddy` with the basic scaffolding for our agent.

## Project Structure

After running the `adk create` command, your project structure will look like this:

```
school_agents/
├── .venv/
├── src/
│   └── agents/
│       └── study_buddy/
│           ├── __init__.py
│           ├── agent.py
│           ├── agent_config.yml
│           └── prompts/
│               └── study_buddy_prompt.md
├── pyproject.toml
└── uv.lock
```

This structure keeps your agent's code, configuration, and prompts neatly organized.

## Configuring Your Agent

Before diving into the agent's files, it's important to set up your API keys. Create a `.env` file in the main project directory (`school_agents/`).

```bash
touch .env
```

Keeping the `.env` file at the project level is preferable because:

- **Centralized Configuration**: If your project grows to include multiple agents, a single `.env` file manages credentials for all of them, reducing duplication and potential errors.

- **Security**: Environment variables are not committed to version control (add `.env` to `.gitignore`), and keeping it at the root makes it easier to manage access.

- **Consistency**: It follows standard practices in Python projects, where tools like `python-dotenv` (often used by libraries like ADK) load from the project root.

The `google-adk` automatically loads environment variables from this file. For using a model on Vertex AI, you will need to add the following to your `.env` file:

```
GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"
```
Replace `"your-google-cloud-project-id"` with your actual Google Cloud project ID. You also need to be authenticated. You can do this by running:
```bash
gcloud auth application-default login
```

### Using GOOGLE_API_KEY Instead of Vertex AI

If you prefer to use the direct Google AI API instead of Vertex AI (for example, if you don't have a Google Cloud project set up), you can configure your `.env` file with your Google API key:

```
GOOGLE_API_KEY="your-google-api-key"
```

You can obtain a Google API key from [Google AI Studio](https://aistudio.google.com/). 

In this case, omit the Vertex AI-specific variables (GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION). The ADK will use the direct API endpoint, which is simpler to set up but may have different rate limits and features compared to Vertex AI.

Inside the `study_buddy` directory, you'll find a few files. Let's focus on `agent_config.yml` and `prompts/study_buddy_prompt.md`.

### `agent_config.yml`

This file contains the basic configuration for our agent, such as its name, description, and the AI model it should use.

```yaml
agent:
  name: "study_buddy"
  description: "A friendly, encouraging, and knowledgeable assistant for students"
  model: "gemini-2.5-flash"
  prompt_file: "prompts/study_buddy_prompt.md"
```

### `prompts/study_buddy_prompt.md`

This is where the magic happens. The prompt file defines the agent's personality, capabilities, and constraints. It's a detailed set of instructions that the AI model will follow.

To create an effective prompt for your AI agent, you can utilize Google Gemini to generate and refine ideas. Engage in prompt engineering by iteratively testing and improving your instructions. A good prompt must clearly define:

- **Role**: What the agent is (e.g., a study buddy).
- **Responsibilities**: Core tasks the agent should perform.
- **Specifications**: Capabilities and how to handle specific scenarios.
- **Limitations**: What the agent should not do.
- **Tonality**: The style and tone of responses (e.g., friendly and encouraging).
- **Response Instructions**: How to structure replies, including any formats or guidelines.

Here's the full prompt used in our Study Buddy agent:

```markdown
You are an AI-powered Study Buddy, a friendly, encouraging, and knowledgeable assistant for students. Your primary purpose is to make learning easier, more effective, and less stressful by providing academic support and motivation.

## Identity & Purpose

- You are a patient, encouraging, and supportive Study Buddy
- Help students understand concepts, clarify doubts, assist with homework, and prepare for exams
- Main goal: Empower students to learn independently and build confidence

## Capabilities

### Subject Expertise
- Explain complex topics from various subjects (Math, Science, History, Literature, etc.)
- Use analogies and real-world examples to make concepts clear
- Answer specific, fact-based academic questions

### Homework Guidance
- Guide students through homework problems
- Provide hints and explanations (NOT direct answers)
- Walk through similar example problems

### Exam Preparation
- Create practice quizzes and flashcards
- Summarize key points from chapters or articles
- Help develop personalized study plans
- Explain key terms and definitions

### Motivation & Support
- Provide words of encouragement
- Celebrate small wins
- Help students overcome study blocks

## Behavior Guidelines

### Tone & Communication
- Always maintain a friendly, patient, positive, and encouraging tone
- Use supportive phrases such as:
  - "That's a great question!"
  - "You're on the right track!"
  - "Let's figure this out together!"
  - "You can do this!"

### Interaction Style
- Communicate clearly and concisely
- Ask clarifying questions to understand struggles
- When students are wrong, gently correct and frame as learning opportunities
- If unsure about something, be honest: "I'm not quite sure about that, but we can try to find some good resources to help you."

## Critical Constraints

### Academic Integrity (NON-NEGOTIABLE)
- NEVER provide direct answers to homework, test, or assignment questions
- NEVER write essays, reports, or code for students
- NEVER enable cheating in any form

### Response to Direct Answer Requests
When asked for direct answers, respond with: "I can't give you the answer directly, because the goal is for you to learn how to solve it. But I can definitely help you understand the steps to get there! Where are you getting stuck?"

### Technical Requirements
- Use clear mathematical notation in plain text format
- For equations, use standard notation like: a^2 + b^2 = c^2

### Boundaries
- Do not engage in personal conversations outside academic context
- Do not provide life advice, medical advice, or mental health counseling
- If student expresses severe distress or mentions self-harm:
  - Immediately disengage from academic topic
  - Direct them to seek help from trusted adults or professional services

## Core Mission

Your purpose is to facilitate learning and maintain academic integrity at all times.

Remember: You are not just answering questions—you are a supportive partner in the student's learning journey.
```

For our Study Buddy, the prompt outlines its identity as a "friendly, encouraging, and knowledgeable assistant for students." It specifies its capabilities, such as explaining complex topics, guiding students through homework, and helping with exam preparation.

Crucially, it also sets "Critical Constraints," particularly around academic integrity. The agent is explicitly told **not** to provide direct answers but to guide students to find the answers themselves.

### Why External Configuration and Prompts?

We choose to keep the agent's configuration in an external `agent_config.yml` file and the system prompt in a separate `prompts` folder for several reasons:

- **Modularity and Maintainability**: Separating configuration from code allows you to update the agent's name, description, model, or prompt file without modifying the Python code. This makes the system more flexible and easier to maintain.

- **Readability and Collaboration**: Prompts are often lengthy and descriptive. Storing them in Markdown files makes them easier to read, edit, and version control. Multiple team members can collaborate on refining the prompt without touching the codebase.

- **Separation of Concerns**: By externalizing these elements, we follow best practices in software design, keeping the code focused on logic (like loading and creating the agent) while configuration and content are handled separately.

- **Reusability**: This structure allows you to reuse prompts across different agents or projects, and easily experiment with different configurations.

This approach aligns with principles like the Twelve-Factor App methodology, which emphasizes treating configuration as something separate from code.

## Bringing Your Agent to Life: The Code

The logic for our agent resides in `agent.py`. Let's take a look at a simplified version of the code:

```python
import os
from pathlib import Path
import yaml
from google.adk import Agent

def load_agent_config(config_path: str) -> dict:
    """Load agent configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_prompt(prompt_path: str) -> str:
    """Load prompt content from markdown file."""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def create_study_buddy_agent() -> Agent:
    """Create and configure the Study Buddy agent."""
    current_dir = Path(__file__).parent
    config_path = current_dir / 'agent_config.yml'
    config = load_agent_config(config_path)
    
    prompt_path = current_dir / config['agent']['prompt_file']
    instruction = load_prompt(prompt_path)
    
    agent = Agent(
        name=config['agent']['name'],
        description=config['agent']['description'],
        model=config['agent']['model'],
        instruction=instruction
    )
    
    return agent

root_agent = create_study_buddy_agent()
```

This script loads the configuration and prompt we defined earlier and uses them to create an `Agent` instance from the `google-adk` library.

## Running Your Agent with `adk web`

Now for the exciting part! Let's run our agent and interact with it. The ADK provides a handy web interface for testing and debugging agents.

First, navigate to the agent's directory:

```bash
cd src/agents/studdy_buddy
```

Then, run:

```bash
adk web
```

We run this command from the agent's directory because the ADK web interface will display a dropdown menu of available agents found in the current working directory and its subdirectories, ensuring your Study Buddy agent is easily selectable.

This will start a local web server and open a chat interface in your browser. You can now chat with your Study Buddy! Ask it a question about a school subject and see how it responds based on the prompt we provided.

## Conclusion

Congratulations! You've successfully created your first AI agent. You've learned how to:

-   Set up a project environment with `uv`.
-   Create an agent using `adk create`.
-   Configure your agent's personality and capabilities through a prompt.
-   Run and interact with your agent using the ADK web interface.

This is just the beginning of your journey into the world of AI agents. From here, you can explore adding tools to your agent, connecting it to external APIs, and building more complex and powerful autonomous systems. Happy coding!

## Experiment and Iterate

One of the best ways to deepen your understanding of AI agents is through hands-on experimentation. Don't be afraid to tweak and test different aspects of your Study Buddy:

- **Change Models**: In the `agent_config.yml`, try switching to different Gemini models (e.g., from "gemini-2.5-flash" to "gemini-1.5-pro"). Observe how this affects response quality, speed, creativity, and any associated costs.

- **Modify Prompts**: Edit the `study_buddy_prompt.md` file to adjust the agent's tone, add new responsibilities, or introduce additional constraints. Use prompt engineering best practices: be specific, provide examples, and iterate based on test interactions.

- **Customize Code**: Experiment with the `agent.py` file by adding custom logic, such as integrating simple tools or handling specific user scenarios.

- **Test Variations**: Run the agent with different configurations and compare results. Try adding more agents to your project and see how they interact.

Remember, true learning comes from experimentation. Without trying new things, making mistakes, and iterating, you won't fully grasp the nuances of building effective AI agents. Start small, document your changes, and build your intuition through practice!

## What's Next: Advancing Your AI Agent Skills

This tutorial has given you the foundation for creating a simple AI agent. In future posts or explorations, we'll dive deeper into advanced topics to take your agents to the next level:



- **Integrating with tools mcp and APIs**: Learn how to equip your agent with tools to interact with external APIs, such as fetching real-time data, sending emails, or querying databases. We'll also cover creating MCP servers and integrating them with your agents to enable more advanced functionalities and custom workflows. This allows your agent to perform practical tasks beyond basic conversations.

- **Deployment**: Discover how to deploy your agent to production environments, including cloud platforms like Google Cloud, Vercel, or Heroku. We'll cover containerization with Docker, setting up web servers, and ensuring scalability and security.

- **Building Multi-Agent Systems**: Explore creating complex systems where multiple agents collaborate. For example, a team of specialized agents (e.g., a researcher, a writer, and an editor) working together on a task, coordinating through a central orchestrator.

Stay tuned for more guides, and experiment with these concepts to build even more sophisticated AI solutions!
