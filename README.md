# DaVinci Resolve AI Agent v1

A local, offline desktop application that converts user text prompts into AI-powered video editing commands for DaVinci Resolve.

**Status**: v1 Implementation Complete (Ready for Testing)

## Quick Start

1. **Install dependencies**:
   ```powershell
   cd backend
   pip install -r requirements.txt
   cd ..\frontend
   npm install
   ```

2. **Download AI model** (llama.cpp compatible):
   ```powershell
   mkdir models
   # Download e.g. Mistral-7B-Instruct-v0.2.gguf to models/
   ```

3. **Start the app**:
   ```powershell
   cd frontend
   npm start
   ```

4. **Run acceptance test** (20 edits):
   ```powershell
   python tests\acceptance_test.py
   ```

---

## Architecture

### Backend (Python)
- **resolve_bridge.py**: Resolve scripting API connection
- **executor.py**: 20 action implementations
- **ai_engine.py**: Local llama.cpp model inference
- **service.py**: Main orchestration + IPC bridge
- **logger.py**: JSON session logging
- **validator.py**: Command validation + dry-run

### Frontend (Electron + React)
- **main.js**: Electron entry point
- **App.js**: Main React component orchestrating workflow
- **Components**: InputPanel, DryRunPreview, ApprovalPanel, LogViewer, SettingsPanel
- **IPC Bridge**: Electron ↔ Python via stdout/stdin

### Workflow
```
User Text Input
    ↓
AI Generation (llama.cpp)
    ↓
Dry-Run Preview
    ↓
Per-Action Approval
    ↓
Execute on Resolve
    ↓
Log Results
```

---

## Supported Actions (18 Total)

| # | Action | Purpose |
|---|--------|---------|
| 1 | `add_marker` | Add marker at frame |
| 2 | `rename_clip` | Set clip name |
| 3 | `set_clip_enabled` | Enable/disable clip |
| 4 | `cut_split_at_timecode` | Split clip at timecode |
| 5 | `set_in_point` | Set clip in-point |
| 6 | `set_out_point` | Set clip out-point |
| 7 | `move_trim_clip` | Move or trim clip |
| 8 | `insert_transition` | Insert transition (6-30f, whitelisted) |
| 9 | `add_color_node` | Add color correction node |
| 10 | `set_exposure` | Set exposure value |
| 11 | `set_contrast` | Set contrast value |
| 12 | `set_saturation` | Set saturation value |
| 13 | `set_temperature` | Set temperature value |
| 14 | `set_lift_gamma_gain` | Set lift/gamma/gain |
| 15 | `apply_lut` | Apply LUT to clip |
| 16 | `enable_disable_node` | Toggle color node |
| 17 | `remove_node` | Remove color node |
| 18 | `set_color_label` | Set clip color label |

---

## Requirements (Locked Spec)

✓ **Input**: Text only (no speech-to-text in v1)  
✓ **AI**: Fully offline local model (llama.cpp)  
✓ **Interface**: Desktop app (Electron + React)  
✓ **Safety**: Dry-run + per-action approval  
✓ **Logging**: Detailed JSON session logs  
✓ **Target**: Current timeline + selected clip (or show list)  
✓ **Platform**: Windows local only  
✓ **Success**: 20 edits at 100% pass rate  

See [REQUIREMENTS_LOCKED.md](REQUIREMENTS_LOCKED.md) for full details.

---

## Setup & Build

### Prerequisites
- DaVinci Resolve 18+
- Python 3.10+
- Node.js 16+

### Full Setup Guide
See [SETUP.md](SETUP.md) for detailed instructions.

### Run Acceptance Test
```powershell
python tests\acceptance_test.py
```

**Expected Output**:
- 20 actions executed sequentially
- Pass/fail per action with duration
- 100% pass rate for success

---

## Project Files

```
DaVinci Resolve plugin/
├── backend/                          # Python backend
│   ├── models.py                    # Data schemas (Pydantic)
│   ├── resolve_bridge.py            # Resolve API connection
│   ├── executor.py                  # 20 action executors
│   ├── ai_engine.py                 # llama.cpp integration
│   ├── validator.py                 # Command validation
│   ├── logger.py                    # Session logging
│   ├── service.py                   # Main orchestration + IPC
│   └── requirements.txt             # Python deps
├── frontend/                         # Electron + React
│   ├── main.js                      # Electron entry
│   ├── preload.js                   # Context bridge
│   ├── package.json                 # Node deps
│   ├── src/
│   │   ├── App.js                   # Main component
│   │   ├── App.css                  # Styles
│   │   ├── components/              # React components
│   │   └── index.js                 # Entry point
│   └── public/
│       └── index.html               # HTML template
├── tests/
│   └── acceptance_test.py           # 20-action test suite
├── REQUIREMENTS_LOCKED.md           # Full requirements spec
├── SETUP.md                         # Setup guide
└── README.md                        # This file
```

---

## Safety & Workflow

**Three Phases**:

1. **Dry-Run**: All actions previewed (no Resolve changes)
2. **Approval**: User reviews each action one-by-one
   - ✓ Approve → execute
   - ⊘ Skip → mark skipped
   - ✗ Cancel → stop batch
3. **Execution**: Approved actions run in order
   - If action fails: ask user to continue or stop

**Guardrails**:
- Unknown/unsupported actions require manual confirmation
- Transitions: whitelist (Cross Dissolve, Dip to Color) + 6–30 frame duration
- All actions logged with timestamp, parameters, result

---

## Logging

Session logs saved to:
```
~\.resolve-ai-agent\logs\session_<id>_<timestamp>.json
```

Each log contains:
- Session ID
- User input text
- Full command
- Dry-run results
- Execution results (per-action: ok, duration, error)
- Aggregated counts

---

## Known Limitations (v1)

- **Text input only** (no speech-to-text)
- **Windows only**
- **Video track 1 only**
- **Single timeline** (no multi-timeline batching)
- **Local inference only** (no cloud fallback)
- **No undo/rollback generation**
- **No in-app fine-tuning**

See [REQUIREMENTS_LOCKED.md](REQUIREMENTS_LOCKED.md) for future v2+ features.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Could not connect to Resolve" | Ensure Resolve is open + scripting enabled (Preferences → Developer) |
| "No clips found" | Add clips to video track 1 in timeline |
| "AI model not loaded" | Load model via Settings panel (llama.cpp compatible GGUF) |
| "Action failed" | Check Resolve logs; some actions depend on color page state |
| Frontend not connecting | Ensure Python backend is running in background |

---

## What's Next (v2+)

- Speech-to-text input
- More editing actions (keyframes, effects, conforming)
- Multi-timeline support
- Undo/rollback generation
- Fine-tuning UI
- Cloud API fallback
- Linux/Mac support

---

## License

MIT

---

## Questions or Issues?

See [SETUP.md](SETUP.md) for detailed troubleshooting.
