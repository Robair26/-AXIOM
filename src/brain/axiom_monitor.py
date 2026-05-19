import os
import sys
import time
import threading
import psutil
import requests
from datetime import datetime
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# AXIOM Monitor — runs in background and alerts proactively
class AXIOMMonitor:
    def __init__(self, alert_callback):
        self.alert_callback = alert_callback
        self.running = False
        self.last_alerts = {}
        self.cpu_high_count = 0
        self.check_interval = 30  # seconds

        # Thresholds
        self.CPU_THRESHOLD = 85
        self.MEMORY_THRESHOLD = 85
        self.DISK_THRESHOLD = 90
        self.CPU_SUSTAINED_COUNT = 3  # 3 checks in a row = sustained high

    def check_cpu(self):
        cpu = psutil.cpu_percent(interval=1)
        if cpu > self.CPU_THRESHOLD:
            self.cpu_high_count += 1
            if self.cpu_high_count >= self.CPU_SUSTAINED_COUNT:
                if self._should_alert('cpu_high'):
                    self.alert_callback(f"Sir, your CPU has been running at {cpu:.0f}% for a sustained period. Something may be consuming excessive resources.")
                    self.cpu_high_count = 0
        else:
            self.cpu_high_count = 0

    def check_memory(self):
        memory = psutil.virtual_memory()
        if memory.percent > self.MEMORY_THRESHOLD:
            if self._should_alert('memory_high'):
                available_gb = round(memory.available / (1024**3), 1)
                self.alert_callback(f"Sir, memory usage is at {memory.percent:.0f}%. Only {available_gb} gigabytes remaining. You may want to close some applications.")

    def check_disk(self):
        disk = psutil.disk_usage('/')
        if disk.percent > self.DISK_THRESHOLD:
            if self._should_alert('disk_high'):
                free_gb = round(disk.free / (1024**3), 1)
                self.alert_callback(f"Sir, disk space is critically low at {disk.percent:.0f}% full. Only {free_gb} gigabytes remaining.")

    def check_network(self):
        try:
            net1 = psutil.net_io_counters()
            time.sleep(1)
            net2 = psutil.net_io_counters()
            bytes_sent = net2.bytes_sent - net1.bytes_sent
            bytes_recv = net2.bytes_recv - net1.bytes_recv
            mb_recv = bytes_recv / (1024 * 1024)
            if mb_recv > 50:
                if self._should_alert('high_network'):
                    self.alert_callback(f"Sir, I'm detecting unusually high network activity. {mb_recv:.1f} megabytes received in the last second. You may want to check what's running.")
        except:
            pass

    def check_processes(self):
        try:
            high_cpu_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 50:
                        high_cpu_procs.append(proc.info['name'])
                except:
                    pass
            if high_cpu_procs and self._should_alert('high_proc'):
                names = ', '.join(set(high_cpu_procs[:3]))
                self.alert_callback(f"Sir, I've detected high CPU usage from: {names}. Want me to investigate?")
        except:
            pass

    def morning_briefing(self):
        hour = datetime.now().hour
        if hour == 9 and self._should_alert('morning_brief', cooldown=3600):
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            self.alert_callback(f"Good morning Sir. Systems are nominal. CPU at {cpu:.0f}%, memory at {memory.percent:.0f}%, and you have {round(disk.free/(1024**3), 1)} gigabytes of disk space available. Ready when you are.")

    def _should_alert(self, alert_type, cooldown=300):
        now = time.time()
        last = self.last_alerts.get(alert_type, 0)
        if now - last > cooldown:
            self.last_alerts[alert_type] = now
            return True
        return False

    def run(self):
        self.running = True
        print("🔍 AXIOM Monitor: Online — watching your systems")
        while self.running:
            try:
                self.check_cpu()
                self.check_memory()
                self.check_disk()
                self.check_network()
                self.morning_briefing()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(10)

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def stop(self):
        self.running = False
