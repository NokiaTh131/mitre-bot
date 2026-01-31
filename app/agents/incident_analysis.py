from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from app.tools.retrieval import AttackPatternsTool
from app.tools.mitre_attack import MitreIncidentTool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
from app.agents.prompt import system_prompt

load_dotenv()

console = Console()

llm = init_chat_model(
    model=os.getenv("MODEL"),
    temperature=0.1,
    max_tokens=4096,
    timeout=None,
    max_retries=2,
)


attack_pattern_tool = AttackPatternsTool()
mitre_incident_tool = MitreIncidentTool()


def create_incident_analysis_agent():
    """
    Creates and compiles the agent graph with an optional checkpointer.
    """
    return create_agent(
        llm,
        tools=[attack_pattern_tool.get_tool(), mitre_incident_tool.get_tool()],
        system_prompt=system_prompt,
    )


class AgentDisplay:
    """Manages the display of agent progress."""

    def __init__(self):
        self.printed_count = 0
        self.current_status = ""
        self.spinner = Spinner("dots", text="Thinking...")

    def update_status(self, status: str):
        self.current_status = status
        self.spinner = Spinner("dots", text=status)

    def print_message(self, msg):
        """Print a message with nice formatting."""
        if isinstance(msg, HumanMessage):
            console.print(Panel(str(msg.content), title="You", border_style="blue"))

        elif isinstance(msg, AIMessage):
            content = msg.content
            if isinstance(content, list):
                text_parts = [
                    p.get("text", "")
                    for p in content
                    if isinstance(p, dict) and p.get("type") == "text"
                ]
                content = "\n".join(text_parts)

            if content and content.strip():
                console.print(
                    Panel(Markdown(content), title="Agent", border_style="green")
                )

            if msg.tool_calls:
                for tc in msg.tool_calls:
                    name = tc.get("name", "unknown")
                    args = tc.get("args", {})

                    if name == "task":
                        desc = args.get("description", "researching...")
                        console.print(
                            f"  [bold magenta]>> Researching:[/] {desc[:60]}..."
                        )
                        self.update_status(f"Researching: {desc[:40]}...")
                    elif name in ("generate_cover", "generate_social_image"):
                        console.print("  [bold cyan]>> Generating image...[/]")
                        self.update_status("Generating image...")
                    elif name == "write_file":
                        path = args.get("file_path", "file")
                        console.print(f"  [bold yellow]>> Writing:[/] {path}")
                    elif name == "web_search":
                        query = args.get("query", "")
                        console.print(f"  [bold blue]>> Searching:[/] {query[:50]}...")
                        self.update_status(f"Searching: {query[:30]}...")
                    elif name == "retrieve_attack":
                        query = args.get("query", "")
                        console.print(
                            f"  [bold cyan]>> Pattern Analyst:[/] Searching for '{query}'..."
                        )
                    elif name == "get_mitre_incident_context":
                        stix_id = args.get("technique_stix_id", "")
                        console.print(
                            f"  [bold orange1]>> MITRE Specialist:[/] Retrieving context for {stix_id}..."
                        )
                    else:
                        console.print(
                            f"  [bold purple]>> Calling Tool:[/] {name} args={args}"
                        )

        elif isinstance(msg, ToolMessage):
            name = getattr(msg, "name", "")
            content = msg.content
            if isinstance(content, list):
                content = str(content)

            if name in ("generate_cover", "generate_social_image"):
                if "saved" in content.lower():
                    console.print("  [green]✓ Image saved[/]")
                else:
                    console.print(f"  [red]✗ Image failed: {content}[/]")
            elif name == "write_file":
                console.print("  [green]✓ File written[/]")
            elif name == "task":
                console.print("  [green]✓ Research complete[/]")
            elif name == "retrieve_attack":
                console.print("  [green]✓ Patterns retrieved[/]")
            elif name == "get_mitre_incident_context":
                console.print("  [green]✓ MITRE context retrieved[/]")
            elif name == "web_search":
                if "error" not in content.lower():
                    console.print("  [green]✓ Found results[/]")
            else:
                console.print(f"  [green]✓ Tool {name} complete[/]")
