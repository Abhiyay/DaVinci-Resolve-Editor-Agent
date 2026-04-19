# Quick Reference

## Start the Application

### 1. Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
cd ..\frontend
npm install
```

### 2. Download AI Model
Download a llama.cpp compatible model (e.g., Mistral 7B Instruct):
```powershell
mkdir models
# Download model to models/mistral-7b.gguf
```

### 3. Run the App
```powershell
cd frontend
npm start
```

This starts:
- React dev server (http://localhost:3000)
- Electron main process
- Python backend service (auto-spawned)

## Test with 20 Edits

Run the acceptance test suite:
```powershell
python tests\acceptance_test.py
```

Expected: 20 actions executed, 100% pass rate.

## Key Files

| File | Purpose |
|------|---------|
| `backend/service.py` | Main backend orchestration + IPC |
| `backend/resolve_bridge.py` | Resolve scripting connection |
| `backend/executor.py` | 18 action implementations |
| `backend/ai_engine.py` | llama.cpp model inference |
| `frontend/main.js` | Electron entry point |
| `frontend/src/App.js` | Main React component |
| `tests/acceptance_test.py` | 20-action test suite |

## User Workflow

1. **Input**: Type text describing edits
2. **AI**: Generates JSON command
3. **Preview**: Review all actions (dry-run)
4. **Approve**: Accept/skip each action one-by-one
5. **Execute**: Run approved actions on Resolve
6. **Log**: View results + export session log

## Troubleshooting

- **Resolve not connecting**: Ensure open + scripting enabled
- **No clips found**: Add to video track 1
- **Model not loaded**: Set path in Settings
- **IPC error**: Ensure Python backend spawned correctly

## Next Steps

1. Install dependencies
2. Download model
3. Run app
4. Set model path in Settings
5. Try example input: "Add a green marker at frame 100"
6. Review dry-run and approve actions

See [SETUP.md](SETUP.md) for detailed instructions.
