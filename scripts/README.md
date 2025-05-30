# Scripts for WildberryEyeZero

---

## 1. Install Dependencies
Ensure your system has Python 3 and required packages:
```bash
sudo apt update
sudo apt install -y python3 python3-psutil python3-pandas python3-matplotlib python3-scipy
```

# 2. Configure Logging via Cron
```bash
crontab -e
```
Start battery logger at reboot
```bash
@reboot /usr/bin/env python3 $HOME/wildberryeye/scripts/battery_logger_txt.py >> $HOME/wildberryeye/logs/battery_logger.log 2>&1 &
```
Save and exit. This will launch the logger script in the background on startup, writing per-boot telemetry into logs/wildberry_logs/ inside the repo.

# 3. Run Analysis
After you have several logs, generate graphs:
```bash
chmod +x scripts/analyze_wildberry.py
scripts/analyze_wildberry.py
```
Output PNGs will appear in docs/images/wilberry_analysis/.

# 4. Clean Up Short Logs
To delete any cycles shorter than, say, 30 minutes:
```bash
chmod +x scripts/clean_short_logs.sh
scripts/clean_short_logs.sh 30
```
