Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& .\.venv\Scripts\Activate.ps1; python backend\main.py"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
