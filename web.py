import json
import sys
import time
import webbrowser

webbrowser.register("firefox", None, webbrowser.BackgroundBrowser("/usr/bin/firefox"))

with open("urls.json") as f:
    URLS = json.load(f)


def save_urls():
    with open("urls.json", "w") as f:
        json.dump(URLS, f, indent=4)


def list_sets():
    print("Available sets:\n")
    for name, urls in URLS.items():
        print(f"  {name}")
        for url in urls:
            print(f"    - {url}")
        print()


def interactive_mode():
    sets = list(URLS.keys())
    print("Pick a set:\n")
    for i, name in enumerate(sets, 1):
        print(f"  {i}. {name}")
    print()
    choice = input("Enter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(sets)):
        print("Invalid choice.")
        sys.exit(1)
    return sets[int(choice) - 1]


def open_webpages(urls):
    for url in urls:
        print(url)
        webbrowser.get("firefox").open(url)
        time.sleep(0.5)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--list" in args:
        list_sets()
        sys.exit(0)

    if "--add" in args:
        idx = args.index("--add")
        set_name, url = args[idx + 1], args[idx + 2]
        if set_name not in URLS:
            URLS[set_name] = []
        if url in URLS[set_name]:
            print(f"'{url}' already exists in '{set_name}'")
        else:
            URLS[set_name].append(url)
            save_urls()
            print(f"Added '{url}' to '{set_name}'")
        sys.exit(0)

    if "--remove" in args:
        idx = args.index("--remove")
        set_name, url = args[idx + 1], args[idx + 2]
        if set_name not in URLS:
            print(f"Unknown set: '{set_name}'")
        elif url not in URLS[set_name]:
            print(f"'{url}' not found in '{set_name}'")
        else:
            URLS[set_name].remove(url)
            save_urls()
            print(f"Removed '{url}' from '{set_name}'")
        sys.exit(0)

    if not args:
        set_name = interactive_mode()
    else:
        set_name = args[0]
        if set_name not in URLS:
            print(f"Unknown set: '{set_name}'. Available: {', '.join(URLS.keys())}")
            sys.exit(1)

    open_webpages(URLS[set_name])
