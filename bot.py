import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = "8467518146:AAGhTVW8bnbWEl2HbZvDItcPhgXTp_n9b1k"

MAX_PAGES = 3     # kitne pages tak auto refresh kare
MAX_LINKS = 25    # total kitne links bheje
DELAY = 1         # seconds delay

visited = set()

def extract_links(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            link = a["href"]
            if link.startswith("http"):
                links.append(link)
        return list(set(links))
    except:
        return []

def handle_message(update, context):
    text = update.message.text.strip()
    chat_id = update.message.chat_id

    if text == "/start":
        update.message.reply_text("👋 Welcome!\n\nMujhe koi link bhejo, main aage ke links auto refresh karke bhej dunga.")
        return

    if not text.startswith("http"):
        update.message.reply_text("❌ Please koi valid link bhejo")
        return

    update.message.reply_text("🔄 Link process ho raha hai...")

    queue = [text]
    sent = 0
    pages = 0

    while queue and pages < MAX_PAGES and sent < MAX_LINKS:
        url = queue.pop(0)
        if url in visited:
            continue

        visited.add(url)
        pages += 1

        links = extract_links(url)

        for l in links:
            if sent >= MAX_LINKS:
                break

            if l not in visited and len(queue) < 5:
                queue.append(l)

            context.bot.send_message(chat_id=chat_id, text=l)
            sent += 1
            import time
            time.sleep(DELAY)

    update.message.reply_text(f"✅ Done! Total links sent: {sent}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
