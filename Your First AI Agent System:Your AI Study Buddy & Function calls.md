Before, we saw how to create a simple AI agent using ADK.

In this blog, we'll see how to provide tools to agents so they can perform their jobs right.

Think of it from the real world: let's say you're opening a bottle cap—maybe a beer bottle. You could use your teeth to do it, but that doesn't ensure a clean job. A tool like a bottle opener makes it easy and effective. Another example: cutting a vegetable. You can break a vegetable by hand, but you can't cut it precisely; for cutting, you need a knife.

Just like in real life, tools are important for AI agents.

Let's take the example of Study Buddy. It's providing answers to students, but it can't provide the latest information—it will totally fail at current affairs, and there's a high probability of it failing at math calculations.

How do we solve this? Simple: provide it with tools like google_search and calculator. Now your agent is much more capable of doing its job.


How do agents actually use these tools?

It's pretty simple. Here's how it works:

1. The agent thinks about what you asked and what it needs to do (reasoning).
2. It decides if it needs a tool, and if so, which one (selection).
3. It figures out what info to give the tool and runs it (invocation).
4. It looks at what the tool gives back (observation).
5. It uses that result to keep going, answer you, or decide what to do next (finalization).

You can think of tools as a special toolkit that the agent's smart brain (the LLM) can grab whenever it needs to get something done—just like you’d grab a bottle opener or a knife for the right job.


Tool Types in ADK
-----------------
There are basically two main types of tools in ADK:

1. **Function Tools:** These are tools you build yourself.
   - Sub-categories:
     - **Function/Method:** Your standard Python functions or methods.
     - **Agents-as-Tools:** Using another agent as a tool for your main agent (we'll dive deeper into this later in the series).
     - **Long Running Function Tools:** For tasks that take time or run asynchronously.
2. **Built-in Tools:** Pre-made tools from ADK, like Google Search or Code executor e.t.c.

We're focusing on these for now to keep things straightforward.

lets bigin with looking at **Built-in Tools:** 

we'll provide the agent capablity of google sarch for verfiying information and ansewring current aafairs

### Detailed Implementation: Adding Tools to Your Study Buddy Agent

Now that we've covered the basics, let's dive into the code. Here's how we set up the Study Buddy agent in `agent.py` to use tools like Google Search:

```pythonA
# From src/agents/studdy_buddy/agent.py

import os
from pathlib import Path
import yaml
from google.adk import Agent
from google.adk.tools import google_search

def create_study_buddy_agent() -> Agent:
    current_dir = Path(__file__).parent
    config_path = current_dir / 'agent_config.yml'
    config = yaml.safe_load(open(config_path, 'r', encoding='utf-8'))
    prompt_path = current_dir / config['agent']['prompt_file']
    instruction = open(prompt_path, 'r', encoding='utf-8').read().strip()
    
    agent = Agent(
        name=config['agent']['name'],
        description=config['agent']['description'],
        model=config['agent']['model'],
        instruction=instruction,
        tools=[google_search],
    )
    return agent

# This creates the agent instance
root_agent = create_study_buddy_agent()
```

This code loads the agent's config and prompt, then adds the `google_search` tool to handle real-time queries.

### How to Update Your Prompt for Effective Tool Usage

To make sure your agent uses tools properly, tweak the prompt in files like `prompts/study_buddy_google_search.md`. Here's what to include:

1. **Clear Tool Instructions:** Tell the agent when to use a tool, e.g., 'If the question needs up-to-date info, use the Google search tool first.'
2. **Reasoning Steps:** Guide it to think aloud, like 'Explain your reasoning before using any tool.'
3. **Error Handling:** Add phrases like 'If a tool fails, fall back to your knowledge base.'

For example, update your prompt to: 'You are a study buddy. For current affairs, use Google search to verify facts first—then summarize the results in a student-friendly way.'

### Creating Custom Tools for Your Study Buddy Agent

Sometimes, the built-in tools like Google Search aren't enough for your agent's specific needs. That's where custom tools come in! With the Agent Development Kit (ADK), you can create your own function tools to handle unique tasks—like connecting to a special database or performing custom calculations. Let's explore how to build and use these tools effectively, based on insights from the [Google ADK documentation on Function Tools](https://google.github.io/adk-docs/tools/function-tools/#1-function-tool).

#### What Are Custom Function Tools?

Custom function tools are essentially Python functions you write yourself and then integrate into your agent. ADK automatically wraps these functions into a format the agent can understand and use. For example, imagine you need a tool to calculate a student's grade based on their test scores. You can write a simple function for this and add it to your agent's toolkit.

Here's a basic example of a custom tool:

```python
# A custom tool for calculating grades
def calculate_grade(scores: list) -> str:
    """
    Calculate a student's grade based on their test scores.
    Args:
        scores (list): A list of numerical test scores.
    Returns:
        str: The calculated grade (e.g., 'A', 'B', 'C').
    """
    average = sum(scores) / len(scores) if scores else 0
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    else:
        return 'D or below'
```

When you add this function to your agent's `tools` list in `agent.py`, ADK inspects its signature—name, parameters, type hints, and docstring—to create a schema. This schema helps the agent's brain (the LLM) know when and how to use the tool.

#### Adding a Custom Tool to Your Agent

To use this custom tool with your Study Buddy agent, you would update the agent creation code in `agent.py` like this:

```python
# In src/agents/studdy_buddy/agent.py

def create_study_buddy_agent() -> Agent:
    current_dir = Path(__file__).parent
    config_path = current_dir / 'agent_config.yml'
    config = yaml.safe_load(open(config_path, 'r', encoding='utf-8'))
    prompt_path = current_dir / config['agent']['prompt_file']
    instruction = open(prompt_path, 'r', encoding='utf-8').read().strip()
    
    agent = Agent(
        name=config['agent']['name'],
        description=config['agent']['description'],
        model=config['agent']['model'],
        instruction=instruction,
        tools=[google_search, calculate_grade],  # Adding the custom tool
    )
    return agent
```

#### Best Practices for Custom Tools

s

### Leveling Up with Custom Tools: Adding Personalization to Study Buddy

Alright, we've got our Study Buddy agent using built-in tools like Google Search, and we've even dipped our toes into creating simple custom tools. But let's pause and think: is our agent truly "buddy-like" yet? Right now, it can answer questions and fetch info, but it treats every interaction like it's the first time. No memory of what the student learned last time, no tracking of progress, no personalized tips based on past struggles. That's not very buddy-ish, is it? It's like a friend who forgets everything you told them yesterday!

So, do we really need to add more? Well, let's think step by step about why personalization could be a game-changer, and if it's worth the effort. If we're building an agent to help students learn better, remembering their journey makes all the difference. Imagine if Study Buddy could say, "Hey, last time you nailed algebra basics—ready to tackle equations today?" That builds confidence and keeps things relevant. Without it, the agent feels generic. But with it, it becomes a true companion.

Now, is a custom tool the way to go? Built-in tools don't handle persistent data like student profiles. We could hack something with external databases, but that complicates things. A custom tool keeps it simple and integrated. Let's explore how we'd add this feature thoughtfully, using a tool called `student_manager.py` as our example.

#### Step 1: Identifying the Need – Why Personalization?

Start by asking: What problem are we solving? Students learn best when guidance is tailored. Track their name, grade, subjects, sessions, goals, and weak spots. This adds features like:
- Greeting them by name with progress updates.
- Suggesting reviews for weak topics.
- Celebrating completed goals.

Without this, the agent is helpful but forgetful. With it, it's engaging and effective. Makes sense for users? Absolutely—it's like upgrading from a generic tutor to a personal coach.

#### Step 2: Planning the Custom Tool – What Should It Do?

Don't jump straight to code. Think about must-have functions:
- Get and update basic info (name, grade).
- Track study sessions and progress.
- Manage goals and weak topics.

Keep it simple: Store data in a JSON file for easy persistence. Follow ADK best practices with docstrings and type hints so the agent understands when to use each part.

Here's a peek at a key function, but remember, the thinking is key: We need something to record sessions because tracking time spent on subjects helps spot patterns.

```python
# From src/agents/studdy_buddy/tools/student_manager.py
def record_study_session(subject: str, duration_minutes: int, topics_covered: List[str], session_notes: Optional[str] = None) -> Dict[str, str]:
    """
    Record a completed study session with progress tracking.
    
    Args:
        subject (str): Subject studied
        duration_minutes (int): Session length
        topics_covered (List[str]): Topics covered
        session_notes (str, optional): Extra notes
    
    Returns:
        Dict[str, str]: Status with details
    """
    # Logic to update JSON file...
```

The docstring here is crucial—it tells the agent's LLM exactly what this does and when to call it, like after a long explanation.

#### Step 3: Integrating It – Updating agent.py

Now, how do we add this to our agent? Import the functions and pop them into the tools list. But think: Which ones first? Start with core ones like getting profiles and recording sessions. Test incrementally.

```python
# In agent.py
from .tools.student_manager import record_study_session, get_student_profile  # Add more as needed

agent = Agent(
    # ...
    tools=[google_search, record_study_session, get_student_profile],
)
```

This adds the feature without overwhelming. Test: Does the agent now remember sessions? If yes, expand.

#### Step 4: Adjusting the Prompt – Guiding the Agent

Finally, tweak the prompt to use these tools smartly. Based on something like `study_buddy_notepad.md`, add instructions like: "Silently use get_student_profile() at the start to personalize. Record sessions with record_study_session() after helpful interactions, but only if it was substantial."

This ensures the agent thinks about when to use tools, keeping conversations natural.

By thinking through why, what, and how to add personalization via a custom tool, we've turned Study Buddy into something truly special. It's not about the syntax—it's about features that make learning fun and effective. If it doesn't fit your needs, skip it; but for a personalized agent, it's a winner!
 
#### A Quick Note on Tool Limitations

One thing to keep in mind as you build your agent: in the current setup with a single agent, you can typically integrate only one built-in tool (like Google Search) effectively, but you can add as many custom tools as you need. This keeps things focused but can feel limiting if you want multiple built-in capabilities. Don't worry—we'll solve this in future posts by exploring multi-agent systems, where different agents can handle different tools and collaborate. Stay tuned!

### The Power of Prompts: Your Agent's Guiding Star

We've talked a lot about tools and code, but let's zoom in on something even more crucial: the prompt. Think of the prompt as the agent's "personality blueprint"—it tells the LLM how to behave, what to say, and when to use tools. In our Study Buddy example, the prompt in `study_buddy_notepad.md` is a masterclass in prompt engineering. It's not just a wall of text; it's carefully structured for the best results. Let's break it down step by step, including a cool technique called XML tag prompting, and see why the prompt is hands-down the most critical part of your agent system.

#### Why Is the Prompt the Most Critical Component?

Before we dive into the tips, let's address the big question: Why does the prompt matter so much? The LLM is smart, but it's like a talented actor without a script—it needs direction to shine. A great prompt:
- **Defines Personality and Behavior**: It sets the tone (friendly, encouraging) and rules (never give direct answers to homework).
- **Guides Tool Usage**: It tells the agent exactly when and how to use tools, preventing misuse.
- **Ensures Consistency**: Without a strong prompt, responses can be erratic. With it, your agent acts reliably, like a true study buddy.
- **Handles Edge Cases**: It includes constraints to avoid issues, like not engaging in non-academic chats.

In short, code and tools build the body, but the prompt breathes life into your agent. Get it wrong, and even the best tools won't help. Get it right, and your agent feels magical. Now, let's look at how `study_buddy_notepad.md` nails this with specific techniques.

#### XML Tag Prompting: Structuring for Clarity

One standout technique in this prompt is "XML tag prompting." It's like organizing your closet with labeled sections—instead of a jumbled mess, everything is neatly categorized. By wrapping instructions in XML-like tags (e.g., <Persona>, <ToolUsageProtocol>), you make the prompt easier for the LLM to parse and follow. Why does this work so well?
- **Improves Comprehension**: LLMs are trained on structured data, so tags help them "chunk" information, reducing confusion.
- **Enhances Focus**: Each tag acts as a mini-section, letting the model zero in on specific aspects like personality or constraints.
- **Best Results Tip**: Use consistent, descriptive tags. In `study_buddy_notepad.md`, tags like <PedagogicalApproach> group teaching methods, making it clear how to explain concepts (e.g., using Socratic questions).

Example from the prompt:
```
<Persona>
Identity: You are a patient, encouraging, and supportive Study Buddy.
Tone: Always maintain a friendly, positive, and enthusiastic tone.
...
</Persona>
```
This tag ensures the agent embodies the right vibe every time.

#### Other Prompt Engineering Tips for Best Results

Beyond XML tags, the prompt uses several smart tricks to optimize performance:
- **Step-by-Step Instructions**: It breaks down complex behaviors into clear steps, like "Think Step-by-Step: Before responding to a complex query, plan your approach." This mirrors how LLMs reason best—methodically.
- **Examples and Good Phrases**: Provides ready-to-use phrases (e.g., "You're on the right track!") and examples (e.g., how to respond to wrong answers). This guides the agent to be encouraging without being vague.
- **Adaptive Elements**: Instructs the agent to adjust based on context, like simplifying language for younger students. Tip: Always include conditionals (if/then) for flexibility.
- **Constraints and Guardrails**: A whole section on what NOT to do, like never providing direct answers to homework. This prevents harmful or off-topic responses. Pro tip: List these explicitly to enforce boundaries.
- **Tool-Specific Guidance**: Details when to use tools silently (e.g., "Use get_student_profile() at the start"). This integrates tools naturally without disrupting the flow.

These tips make the prompt robust—test by iterating: Run sample queries and refine based on outputs.

By crafting prompts like this, you're not just instructing an LLM; you're engineering a reliable system. In our Study Buddy, this prompt ties everything together, ensuring tools like student_manager.py are used perfectly. Remember, a prompt is iterative—tweak it as you test, and watch your agent evolve!

### Wrapping It Up: Your Journey into AI Agents

Whew, we've covered a lot of ground! From understanding why tools are like a bottle opener for your agent, to adding built-in ones like Google Search, creating custom tools for personalization, and mastering prompt engineering with techniques like XML tags. You've seen how our Study Buddy evolves from a simple Q&A bot into a personalized learning companion that remembers progress and adapts to needs.

The key takeaway? Building AI agents is about thoughtful design—combining code, tools, and prompts to solve real problems. It's exciting to see how small additions like a custom student manager can make your agent feel alive and helpful. Experiment, test, and iterate; that's where the magic happens!

In the next section, we'll take this to the real world by deploying our Study Buddy agent using FastAPI. Get ready to turn your creation into a live service that anyone can access—stay tuned!

