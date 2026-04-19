# Build and setup instructions

## Windows Setup

### Prerequisites
- DaVinci Resolve 18.x or higher (with scripting enabled in preferences)
- Python 3.10+
- Node.js 16+ (for Electron frontend)

### Backend Setup
```powershell
cd "c:\Users\VQ4IEB3.VW\Desktop\DaVinci Resolve plugin"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Frontend Setup
```powershell
cd frontend
npm install
```

### Download AI Model
Download a quantized llama.cpp compatible model (e.g., Mistral 7B GGUF):
```powershell
# Example: Download to models/ folder
mkdir models
# Download and save model to models/mistral-7b.gguf
```

## Running the Application

### Development Mode
```powershell
cd frontend
npm start
```

This will start:
1. React dev server on http://localhost:3000
2. Electron main process
3. Python backend service

### Running Acceptance Test
```powershell
.\.venv\Scripts\Activate.ps1
python tests\acceptance_test.py
```

This runs a fixed suite of 20 editing actions and reports:
- Total actions executed
- Pass/fail count
- Execution duration per action
- Detailed log file

## Project Structure

```
.
├── backend/
│   ├── models.py              # Data models & schemas
│   ├── resolve_bridge.py      # Resolve scripting connection
│   ├── executor.py            # 20 action implementations
│   ├── validator.py           # Command validation
│   ├── logger.py              # Session logging
│   ├── ai_engine.py           # llama.cpp integration
│   ├── service.py             # Main orchestration (IPC entry point)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── main.js                # Electron main process
│   ├── preload.js             # Context isolation bridge
│   ├── package.json           # Electron + React deps
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js             # Main React component
│       ├── App.css            # Application styles
│       ├── components/
│       │   ├── InputPanel.js
│       │   ├── DryRunPreview.js
│       │   ├── ApprovalPanel.js
│       │   ├── LogViewer.js
│       │   └── SettingsPanel.js
│       └── index.js
├── tests/
│   └── acceptance_test.py     # 20-action test suite
├── REQUIREMENTS_LOCKED.md     # Full requirements spec
└── README.md                  # This file
```

## Supported Actions (v1)

1. `add_marker` - Add marker at frame
2. `rename_clip` - Set clip name
3. `set_clip_enabled` - Enable/disable clip
4. `cut_split_at_timecode` - Split clip
5. `set_in_point` - Set clip in-point
6. `set_out_point` - Set clip out-point
7. `move_trim_clip` - Move or trim clip
8. `insert_transition` - Insert transition (6-30 frames, whitelisted types)
9. `add_color_node` - Add color node
10. `set_exposure` - Set exposure
11. `set_contrast` - Set contrast
12. `set_saturation` - Set saturation
13. `set_temperature` - Set temperature
14. `set_lift_gamma_gain` - Set lift/gamma/gain
15. `apply_lut` - Apply LUT
16. `enable_disable_node` - Toggle color node
17. `remove_node` - Remove color node
18. `set_color_label` - Set clip color label

## Workflow

1. **Input**: User types text describing edits (e.g., "Add a green marker at frame 100")
2. **AI Generation**: Embedded AI converts text to strict JSON command with actions
3. **Dry-Run**: Preview all actions with estimated impact
4. **Approval**: User reviews and approves each action one-by-one
5. **Execution**: Approved actions run against Resolve scripting API
6. **Logging**: All results saved to JSON session log

## Logs

Session logs are saved to:
```
~\.resolve-ai-agent\logs\session_<id>_<timestamp>.json
```

Each log contains:
- User input text
- Full command
- Dry-run results
- Execution results (success/failure per action)
- Total counts (approved, skipped, failed)

## Safety

- **Dry-run preview required** before any real execution
- **Per-action approval** (approve, skip, or cancel batch)
- **Unknown actions** trigger manual confirmation
- **Transition guardrails**: Whitelist + duration range enforced
- **Auto-rollback on batch cancel** (subsequent actions not executed)

## Troubleshooting

### "Could not connect to Resolve"
- Ensure DaVinci Resolve is open
- Enable scripting: Preferences → Developer → Enable Script Editor

### "No clips found"
- Add clips to video track 1 in active timeline
- Acceptance test requires at least one clip

### "AI model not loaded"
- Set model path in Settings → Load Model
- Ensure llama.cpp compatible GGUF model exists

## Next Steps (v2+)

- Speech-to-text input
- Additional edit actions (keyframes, effects, etc.)
- Multi-timeline batching
- Undo/rollback generation
- In-app fine-tuning
- Cloud API fallback
