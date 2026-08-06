"""
ui.py — Presentation helpers for JobLens CLI.

This module contains ONLY display/rendering code. It must never import
business-logic modules or modify data structures. All helpers accept
pre-computed data and render it to the terminal via Rich.
"""

import os
import sys

# ── Force UTF-8 output for Windows terminals ─────────────────────────
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass  # non-reconfigurable stream (e.g. some CI runners)

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress_bar import ProgressBar
from rich import box

# ── Detect piped stdin ────────────────────────────────────────────────
_INTERACTIVE = sys.stdin.isatty() if hasattr(sys.stdin, "isatty") else True

# ── Shared console ────────────────────────────────────────────────────
console = Console(highlight=False)

# ── Theme constants ───────────────────────────────────────────────────
STATUS_STYLE = {
    "Applied": "blue",
    "Online Assessment": "cyan",
    "Interview": "yellow",
    "Offer": "green",
    "Rejected": "red",
}

STATUS_ICONS = {
    "Applied": "\U0001f4dd",        # 📝
    "Online Assessment": "\U0001f4bb",  # 💻
    "Interview": "\U0001f4bc",      # 💼
    "Offer": "\U0001f389",          # 🎉
    "Rejected": "\u274c",           # ❌
}

MENU_ICONS = {
    "1": "\u2795",   # ➕
    "2": "\U0001f4cb",  # 📋
    "3": "\U0001f504",  # 🔄
    "4": "\U0001f5d1",  # 🗑
    "5": "\U0001f50d",  # 🔍
    "6": "\U0001f4ca",  # 📊
    "7": "\U0001f4c4",  # 📄
    "8": "\U0001f6aa",  # 🚪
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Prompt helper (degrades to plain input() when stdin is piped)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def prompt(label: str) -> str:
    """Styled input prompt. Falls back to plain input() for piped stdin."""
    if _INTERACTIVE:
        console.print(f"  [bold cyan]{label}[/]")
        try:
            return console.input("  [dim]>[/] ")
        except EOFError:
            return ""
    else:
        # piped / non-interactive — use plain input so automated tests work
        try:
            return input(f"{label} ")
        except EOFError:
            return ""


def wait_for_enter():
    """Press-enter gate between screens."""
    if _INTERACTIVE:
        console.print()
        console.input("  [dim]Press Enter to return to the menu...[/] ")
    else:
        try:
            input()
        except EOFError:
            pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Message helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_success(msg: str):
    console.print(f"  [bold green]\u2713 {msg}[/]")

def print_error(msg: str):
    console.print(f"  [bold red]\u2717 {msg}[/]")

def print_warning(msg: str):
    console.print(f"  [bold yellow]\u26a0 {msg}[/]")

def print_info(msg: str):
    console.print(f"  [bold cyan]\u2139 {msg}[/]")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Welcome / Main Menu / Exit
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_welcome():
    """Render the branded welcome header."""
    title = Text()
    title.append("JobLens", style="bold white")
    subtitle = Text("Job Application Tracker", style="dim white")
    content = Text.assemble(title, "\n", subtitle, justify="center")
    console.print()
    console.print(
        Panel(
            content,
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 4),
        )
    )


def print_main_menu():
    """Render the numbered main menu with icons."""
    lines = [
        f"  [bold]{MENU_ICONS['1']}  1.[/] Add Application",
        f"  [bold]{MENU_ICONS['2']}  2.[/] View Applications",
        f"  [bold]{MENU_ICONS['3']}  3.[/] Update Status",
        f"  [bold]{MENU_ICONS['4']}  4.[/] Delete Application",
        f"  [bold]{MENU_ICONS['5']}  5.[/] Search Applications",
        f"  [bold]{MENU_ICONS['6']}  6.[/] Statistics",
        f"  [bold]{MENU_ICONS['7']}  7.[/] Resume Matcher",
        f"  [bold]{MENU_ICONS['8']}  8.[/] Exit [dim](Press Q or 8)[/]",
    ]
    menu_text = "\n".join(lines)
    console.print(
        Panel(
            menu_text,
            title="[bold white]Choose an option[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2),
        )
    )


def print_exit():
    """Render a brief goodbye message."""
    console.print()
    console.print(
        Panel(
            "[bold white]Goodbye![/]  [dim]Thanks for using JobLens.[/]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Application table (short list)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_app_table(applications):
    """Render the compact application list as a Rich table."""
    table = Table(
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold white",
        show_lines=False,
        padding=(0, 1),
    )
    table.add_column("ID", justify="right", style="dim", width=5)
    table.add_column("Company", min_width=16, max_width=22)
    table.add_column("Role", min_width=16, max_width=22)
    table.add_column("Status", min_width=18)

    for app in applications:
        style = STATUS_STYLE.get(app.status, "white")
        icon = STATUS_ICONS.get(app.status, "")
        table.add_row(
            str(app.id),
            app.company,
            app.role,
            f"[{style}]{icon}  {app.status}[/]",
        )
    console.print(table)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Application detail (single record)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_app_detail(app):
    """Render full details of a single JobApplication inside a panel."""
    style = STATUS_STYLE.get(app.status, "white")
    icon = STATUS_ICONS.get(app.status, "")

    lines = (
        f"  [bold]Company[/]       {app.company}\n"
        f"  [bold]Role[/]          {app.role}\n"
        f"  [bold]Location[/]      {app.location}\n"
        f"\n"
        f"  [bold]Date Applied[/]  {app.date_applied}\n"
        f"  [bold]Status[/]        [{style}]{icon}  {app.status}[/]\n"
        f"\n"
        f"  [bold]Job Link[/]      [underline]{app.job_link}[/]\n"
        f"\n"
        f"  [bold]Notes[/]\n"
        f"  [dim]{app.notes}[/]"
    )

    console.print(
        Panel(
            lines,
            title=f"[bold white]\U0001f4c4 Application #{app.id}[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style=style,
            padding=(1, 2),
        )
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Section header
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_section_header(title: str, style: str = "cyan"):
    """Render a bordered section title."""
    console.print()
    console.rule(f"[bold {style}]{title}[/]", style=style)
    console.print()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Status selector
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_status_select(statuses):
    """Render the numbered status list for update_status()."""
    lines = []
    for idx, status in enumerate(statuses, start=1):
        style = STATUS_STYLE.get(status, "white")
        icon = STATUS_ICONS.get(status, "")
        lines.append(f"  [bold]{idx}.[/] [{style}]{icon}  {status}[/]")
    content = "\n".join(lines)
    console.print(
        Panel(
            content,
            title="[bold white]Select new Status[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2),
        )
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Search sub-menu
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_search_menu():
    """Render the search-by sub-menu."""
    lines = [
        "  [bold]1.[/] By Company",
        "  [bold]2.[/] By Role",
        "  [bold]3.[/] By Location",
        "  [bold]4.[/] By Status",
        "  [bold]5.[/] Back",
    ]
    content = "\n".join(lines)
    console.print(
        Panel(
            content,
            title="[bold white]\U0001f50d Search By[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2),
        )
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Statistics sub-menu
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_statistics_menu():
    """Render the statistics sub-menu."""
    lines = [
        "  [bold]1.[/] View Terminal Statistics",
        "  [bold]2.[/] Generate Applications by Status Chart",
        "  [bold]3.[/] Back",
    ]
    content = "\n".join(lines)
    console.print(
        Panel(
            content,
            title="[bold white]\U0001f4ca Statistics[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2),
        )
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Statistics dashboard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_statistics_dashboard(track: dict, total: int):
    """Render the terminal statistics as a Rich dashboard with panels."""
    # ── Total applications header ─────────────────────────────────────
    console.print()
    console.print(
        Panel(
            f"  [bold white]\U0001f4c4 Total Applications:[/]  [bold cyan]{total}[/]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
    )

    # ── Per-status breakdown table ────────────────────────────────────
    max_count = max(track.values()) if total else 1

    table = Table(
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold white",
        show_lines=False,
        padding=(0, 1),
        title="[bold white]Application Status[/]",
        title_style="bold white",
    )
    table.add_column("Status", min_width=20)
    table.add_column("Bar", min_width=22, no_wrap=True)
    table.add_column("Count", justify="right", width=6)
    table.add_column("%", justify="right", width=8)

    for status, count in track.items():
        style = STATUS_STYLE.get(status, "white")
        icon = STATUS_ICONS.get(status, "")

        bar_length = int((count / max_count) * 20) if count else 0
        bar = "\u2588" * bar_length  # █

        percentage = (count / total * 100) if total else 0

        table.add_row(
            f"[{style}]{icon}  {status}[/]",
            f"[{style}]{bar}[/]",
            f"[bold]{count}[/]",
            f"[dim]{percentage:>5.1f}%[/]",
        )

    console.print(table)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Resume match report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def print_resume_report(score, matched, missing, jd_skills, format_skill_fn):
    """
    Render the resume-vs-JD match report.

    Parameters
    ----------
    score       : float   – match percentage
    matched     : set     – skills found in both resume and JD
    missing     : set     – skills in JD but not resume
    jd_skills   : set     – all skills extracted from the JD
    format_skill_fn : callable – e.g. resume_matcher.format_skill
    """
    # ── Score panel ───────────────────────────────────────────────────
    if score >= 85:
        grade = "[bold green]\U0001f7e2 Excellent Match[/]"
        border = "green"
    elif score >= 70:
        grade = "[bold yellow]\U0001f7e1 Good Match[/]"
        border = "yellow"
    elif score >= 50:
        grade = "[bold yellow]\U0001f7e0 Moderate Match[/]"
        border = "yellow"
    else:
        grade = "[bold red]\U0001f534 Low Match[/]"
        border = "red"

    score_text = (
        f"  [bold white]\U0001f4ca Match Score:[/]  "
        f"[bold]{score:.1f}%[/]  "
        f"[dim]({len(matched)}/{len(jd_skills)} skills matched)[/]\n\n"
        f"  {grade}"
    )
    console.print()
    console.print(
        Panel(
            score_text,
            title="[bold white]Resume Match Report[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style=border,
            padding=(1, 2),
        )
    )

    # ── Matched skills ────────────────────────────────────────────────
    if matched:
        matched_lines = "\n".join(
            f"  [green]\u2713[/] {format_skill_fn(s)}" for s in sorted(matched)
        )
    else:
        matched_lines = "  [dim]No matching skills found.[/]"

    console.print(
        Panel(
            matched_lines,
            title=f"[bold green]\u2705 Matched Skills ({len(matched)})[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="green",
            padding=(1, 2),
        )
    )

    # ── Missing skills ────────────────────────────────────────────────
    if missing:
        missing_lines = "\n".join(
            f"  [red]\u2717[/] {format_skill_fn(s)}" for s in sorted(missing)
        )
    else:
        missing_lines = "  [dim]None! Your resume covers every detected skill.[/]"

    console.print(
        Panel(
            missing_lines,
            title=f"[bold red]\u274c Missing Skills ({len(missing)})[/]",
            title_align="left",
            box=box.ROUNDED,
            border_style="red",
            padding=(1, 2),
        )
    )
