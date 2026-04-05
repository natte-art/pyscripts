import sys
import os
import subprocess
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

DOWNLOAD_DIR = os.path.expanduser("~/Pictures/Wallpapers")
BASE_URL = "https://wallhaven.cc/api/v1/search"

def search_wallpapers(query, purity="100", categories="111", limit=10):
    params = {
        "q": query,
        "purity": purity,
        "categories": categories,
        "sorting": "toplist",
        "order": "desc",
        "atleast": "1920x1080",
    }
    res = requests.get(BASE_URL, params=params)
    data = res.json()
    return data.get("data", [])[:limit]

def display_results(wallpapers):
    table = Table(box=box.ROUNDED, border_style="cyan", show_header=True)
    table.add_column("#", style="bold cyan", justify="right")
    table.add_column("ID", style="bold white")
    table.add_column("Resolution", style="bold green")
    table.add_column("Views", style="yellow", justify="right")
    table.add_column("Favorites", style="magenta", justify="right")

    for i, wp in enumerate(wallpapers, 1):
        table.add_row(
            str(i),
            wp["id"],
            wp["resolution"],
            str(wp["views"]),
            str(wp["favorites"]),
        )
    console.print(table)

def preview_wallpaper(url, index, resolution):
    try:
        console.print(f"\n[bold cyan]Preview #{index} — {resolution}[/bold cyan]")
        res = requests.get(url, stream=True)
        with open("/tmp/wp_preview.jpg", "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        subprocess.run(['chafa', '--size', '80x40', '/tmp/wp_preview.jpg'])
    except Exception as e:
        console.print(f"[yellow]Preview unavailable: {e}[/yellow]")

def download_wallpaper(wp):
    url = wp["path"]
    filename = url.split("/")[-1]
    save_path = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(save_path):
        console.print(f"[yellow]Already exists:[/yellow] {filename}")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    console.print(f"[bold cyan]Downloading:[/bold cyan] {filename}")
    res = requests.get(url, stream=True)
    with open(save_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=8192):
            f.write(chunk)
    console.print(f"[bold green]Saved to:[/bold green] {save_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] python3 wallhaven.py <query>")
        console.print("[dim]Example: python3 wallhaven.py 'anime landscape'[/dim]")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    console.print(f"\n[bold cyan]Searching for:[/bold cyan] {query}\n")

    wallpapers = search_wallpapers(query)

    if not wallpapers:
        console.print("[bold red]No results found.[/bold red]")
        sys.exit(1)

    display_results(wallpapers)

    console.print("\n[dim]Loading previews...[/dim]")
    for i, wp in enumerate(wallpapers, 1):
        preview_wallpaper(wp["path"], i, wp["resolution"])
        console.print(f"[dim]Press Enter for next preview or type 's' to skip to selection:[/dim] ", end="")
        inp = input().strip().lower()
        if inp == 's':
            break

    console.print("\n[bold]Enter numbers to download (e.g. 1 3 5) or 'all':[/bold] ", end="")
    choice = input().strip()

    if choice == "all":
        selected = wallpapers
    else:
        indices = [int(x) - 1 for x in choice.split() if x.isdigit()]
        selected = [wallpapers[i] for i in indices if 0 <= i < len(wallpapers)]

    console.print()
    for wp in selected:
        download_wallpaper(wp)

    console.print(f"\n[bold green]Done! {len(selected)} wallpaper(s) downloaded to {DOWNLOAD_DIR}[/bold green]\n")
