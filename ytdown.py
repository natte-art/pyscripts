import sys
import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def download(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '/home/natte/Videos/Pytube/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        console.print("\n[bold cyan]Fetching video info...[/bold cyan]")
        info = ydl.extract_info(url, download=False)

        title = info.get('title', 'N/A')
        views = f"{info.get('view_count', 0):,}"
        duration = info.get('duration', 0)
        minutes, seconds = divmod(duration, 60)
        filesize = info.get('filesize') or info.get('filesize_approx', 0)
        size_mb = f"{filesize / (1024 * 1024):.1f} MB" if filesize else "N/A"
        ext = info.get('ext', 'N/A')
        save_path = f"/home/natte/Videos/{title}.{ext}"

        console.print("[bold cyan]Downloading...[/bold cyan]")
        ydl.download([url])

        summary = Text()
        summary.append(f"  Title:     ", style="bold green")
        summary.append(f"{title}\n")
        summary.append(f"  Views:     ", style="bold green")
        summary.append(f"{views}\n")
        summary.append(f"  Duration:  ", style="bold green")
        summary.append(f"{minutes}m {seconds}s\n")
        summary.append(f"  Size:      ", style="bold green")
        summary.append(f"{size_mb}\n")
        summary.append(f"  Format:    ", style="bold green")
        summary.append(f"{ext}\n")
        summary.append(f"  Saved to:  ", style="bold green")
        summary.append(f"{save_path}\n")

        console.print(Panel(summary, title="[bold green]Download Complete[/bold green]", border_style="green"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] python3 ytdown.py <url>")
        sys.exit(1)
    download(sys.argv[1])
