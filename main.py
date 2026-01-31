import asyncio
import sys

from rich.console import Console
from rich.live import Live
from app.agents.incident_analysis import AgentDisplay, create_incident_analysis_agent

console = Console()


async def main():
    """Run the incident analysis agent with streaming output."""
    console.print()
    console.print("[bold blue]Incident Analysis Agent[/]")

    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task_input = console.input(
            "[bold yellow]Enter incident description[/] (press Enter for default): "
        ).strip()
        if task_input:
            task = task_input
        else:
            task = "Analyze a potential incident where a user received a suspicious email with a link to a 'salary_update.exe' file, which they downloaded and ran."

    console.print(f"[dim]Task: {task}[/]")
    console.print()

    agent = create_incident_analysis_agent()
    display = AgentDisplay()

    console.print()

    # Use Live display for spinner during waiting periods
    with Live(
        display.spinner, console=console, refresh_per_second=10, transient=True
    ) as live:
        async for chunk in agent.astream(
            {"messages": [("user", task)]},
            config={"configurable": {"thread_id": "content-writer-demo"}},
            stream_mode="values",
        ):
            if "messages" in chunk:
                messages = chunk["messages"]
                if len(messages) > display.printed_count:
                    # Temporarily stop spinner to print
                    live.stop()
                    for msg in messages[display.printed_count :]:
                        display.print_message(msg)
                    display.printed_count = len(messages)
                    # Resume spinner
                    live.start()
                    live.update(display.spinner)

    console.print()
    console.print("[bold green]✓ Done![/]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/]")
