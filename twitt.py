import os
import random
import time
from atproto import Client
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console

load_dotenv()

console = Console()

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)

bsky_client = Client()
bsky_client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

def generate_tweet():
    prompts = [
        "Generate a short funny programming joke. Max 250 characters. No hashtags. Just the joke.",
        "Generate a short useful coding tip for developers. Max 250 characters. Just the tip. No hashtags.",
    ]
    prompt = random.choice(prompts)
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()

def post(text):
    bsky_client.send_post(text)

def run_bot():
    console.print("[bold cyan]Bot started![/bold cyan]")
    try:
        console.print("\n[bold yellow]Generating post...[/bold yellow]")
        post_text = generate_tweet()
        console.print(f"[green]Post:[/green] {post_text}")
        post(post_text)
        console.print("[bold green]Posted successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    run_bot()
