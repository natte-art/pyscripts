import os
import subprocess
import psutil
import requests
import time
from datetime import datetime
from atproto import Client
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.live import Live

load_dotenv()

console = Console()

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD")

def get_system():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu": cpu,
        "ram_used": ram.used / (1024**3),
        "ram_total": ram.total / (1024**3),
        "disk_used": disk.used / (1024**3),
        "disk_total": disk.total / (1024**3),
    }

def get_weather():
    try:
        res = requests.get("https://wttr.in/Nairobi?format=j1", timeout=5)
        data = res.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        humidity = data['current_condition'][0]['humidity']
        return f"{temp}°C  {desc}  Humidity: {humidity}%"
    except:
        return "Weather unavailable"

def get_latest_post():
    try:
        bsky = Client()
        bsky.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        feed = bsky.get_author_feed(actor=BLUESKY_HANDLE, limit=1)
        return feed.feed[0].post.record.text
    except:
        return "No posts found"

def get_media():
    try:
        title = subprocess.check_output(
            ['playerctl', 'metadata', 'title'], stderr=subprocess.DEVNULL
        ).decode().strip()
        artist = subprocess.check_output(
            ['playerctl', 'metadata', 'artist'], stderr=subprocess.DEVNULL
        ).decode().strip()
        status = subprocess.check_output(
            ['playerctl', 'status'], stderr=subprocess.DEVNULL
        ).decode().strip()
        if artist:
            return f"{status}  {artist} — {title}"
        return f"{status}  {title}"
    except:
        return "Nothing playing"

def build_dashboard():
    now = datetime.now().strftime("%A, %B %d  %I:%M:%S %p")
    sys = get_system()

    # Time
    time_panel = Panel(
        Text(now, justify="center", style="bold cyan"),
        title="🕐 Time",
        border_style="cyan",
        box=box.ROUNDED,
    )

    # System
    sys_table = Table(box=None, show_header=False, padding=(0, 2))
    sys_table.add_column(style="bold green")
    sys_table.add_column()
    sys_table.add_row("CPU", f"{sys['cpu']}%")
    sys_table.add_row("RAM", f"{sys['ram_used']:.1f}GB / {sys['ram_total']:.1f}GB")
    sys_table.add_row("Disk", f"{sys['disk_used']:.1f}GB / {sys['disk_total']:.1f}GB")
    sys_panel = Panel(sys_table, title="🖥  System", border_style="green", box=box.ROUNDED)

    # Weather
    weather = get_weather()
    weather_panel = Panel(
        Text(weather, justify="center"),
        title="🌤  Weather - Nairobi",
        border_style="yellow",
        box=box.ROUNDED,
    )

    # Bluesky
    post = get_latest_post()
    bluesky_panel = Panel(
        Text(post, justify="center"),
        title="🦋  Latest Bluesky Post",
        border_style="blue",
        box=box.ROUNDED,
    )

    # Media
    media = get_media()
    media_panel = Panel(
        Text(media, justify="center"),
        title="🎵  Now Playing",
        border_style="magenta",
        box=box.ROUNDED,
    )

    return Columns([time_panel, sys_panel, weather_panel, bluesky_panel, media_panel], equal=True)

def run():
    with Live(build_dashboard(), refresh_per_second=1, screen=True) as live:
        while True:
            live.update(build_dashboard())
            time.sleep(5)

if __name__ == "__main__":
    run()
