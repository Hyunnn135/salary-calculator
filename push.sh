#!/bin/bash
git add .
git commit -m "${1:-업데이트}"
git push
echo "✅ GitHub 푸시 완료! Cloudflare 배포 중... (1~2분 소요)"
echo "🌐 https://salary-calculator.hyunnn135.workers.dev"
