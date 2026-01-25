---
run: |
  Stop-Process -Name "streamlit" -Force -ErrorAction SilentlyContinue; Write-Host "Streamlit app stopped."
---

# Stop App

Stops any running Streamlit application.
