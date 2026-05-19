import os
import sys
import time
import threading
import schedule
from datetime import datetime
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.search import search_web

load_dotenv()

class AXIOMButler:
    def __init__(self, alert_callback, anthropic_client):
        self.alert_callback = alert_callback
        self.client = anthropic_client
        self.running = False
        self.watchlist = []
        self.last_watch_results = {}

        self.BRIEFING_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
Based on the news and information provided, give a concise morning briefing in 3-4 sentences.
Speak naturally and conversationally. Address the user as Sir.
No bullet points, no formatting. Just natural speech like a real assistant."""

        self.PREDICTION_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
Based on the current news and context, predict what today might bring in 2-3 sentences.
Be specific and insightful. Address the user as Sir. Natural conversational tone."""

        self.WATCHDOG_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
You found new information about something the user is monitoring.
Summarize what changed or what's new in 1-2 sentences. Address user as Sir. Natural tone."""

    def generate_response(self, prompt, content):
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=300,
                system=prompt,
                messages=[{"role": "user", "content": content}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Sir, I encountered an error generating the briefing: {str(e)}"

    def morning_briefing(self):
        """Runs every morning and delivers a spoken briefing"""
        print("🌅 AXIOM Butler: Generating morning briefing...")
        try:
            news = search_web("top news today world")
            tech_news = search_web("AI technology news today")
            weather = search_web("Los Angeles weather today")

            content = f"""Today is {datetime.now().strftime('%A, %B %d, %Y')}.

World News: {news[:500]}

Tech & AI News: {tech_news[:500]}

Weather: {weather[:300]}

Generate a morning briefing covering the most important points."""

            briefing = self.generate_response(self.BRIEFING_PROMPT, content)
            self.alert_callback(f"Good morning Sir. Here is your morning briefing. {briefing}")
            time.sleep(5)
            prediction_content = f"Based on today's news: {news[:300]}\n\nWhat should Sir expect or watch out for today?"
            prediction = self.generate_response(self.PREDICTION_PROMPT, prediction_content)
            self.alert_callback(f"As for today Sir, {prediction}")

        except Exception as e:
            self.alert_callback(f"Sir, I had trouble generating your morning briefing. {str(e)}")

    def add_to_watchlist(self, topic):
        """Add a topic to monitor"""
        if topic not in self.watchlist:
            self.watchlist.append(topic)
            return f"Sir, I will now monitor '{topic}' and alert you when something new comes up."
        return f"Sir, I am already monitoring '{topic}'."

    def remove_from_watchlist(self, topic):
        """Remove a topic from monitoring"""
        if topic in self.watchlist:
            self.watchlist.remove(topic)
            return f"Sir, I have stopped monitoring '{topic}'."
        return f"Sir, '{topic}' was not on the watchlist."

    def get_watchlist(self):
        """Get current watchlist"""
        if not self.watchlist:
            return "Sir, your watchlist is currently empty."
        return f"Sir, I am currently monitoring: {', '.join(self.watchlist)}"

    def check_watchlist(self):
        """Check all watched topics for new developments"""
        if not self.watchlist:
            return
        print(f"🔍 AXIOM Butler: Checking watchlist — {len(self.watchlist)} items")
        for topic in self.watchlist:
            try:
                results = search_web(f"{topic} latest news update")
                result_hash = hash(results[:200])
                if topic in self.last_watch_results:
                    if self.last_watch_results[topic] != result_hash:
                        content = f"Topic being monitored: {topic}\nNew information found: {results[:400]}\nAlert the user about what changed."
                        alert = self.generate_response(self.WATCHDOG_PROMPT, content)
                        self.alert_callback(f"Sir, update on {topic}. {alert}")
                self.last_watch_results[topic] = result_hash
                time.sleep(2)
            except Exception as e:
                print(f"Watchlist error for {topic}: {e}")

    def run(self):
        self.running = True
        print("🤵 AXIOM Butler: Online — morning briefings and watchdog active")

        # Schedule morning briefing at 8 AM
        schedule.every().day.at("08:00").do(self.morning_briefing)

        # Check watchlist every 30 minutes
        schedule.every(30).minutes.do(self.check_watchlist)

        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def stop(self):
        self.running = False
