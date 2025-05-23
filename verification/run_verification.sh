#!/bin/bash
# Cron job to automatically verify Sunheart AI capabilities
# Recommended to run daily

cd /nix/store/x9d49vaqlrkw97p9ichdwrnbh013kq7z-bash-interactive-5.2p37/bin/..
python verification/verification_system.py > verification/last_run.log 2>&1
