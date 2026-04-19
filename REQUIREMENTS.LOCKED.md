# DaVinci Resolve AI Editor Agent - v1 Requirements (LOCKED)

## Core Vision
Build a local, standalone desktop application that converts user text input into AI-powered structured JSON commands, then executes those commands against DaVinci Resolve's scripting API to perform video and color editing on the active timeline and selected clip.

---

## 1. End-to-End Workflow

1. User enters text prompt in desktop app UI.
2. Text is sent to embedded local AI model.
3. AI returns strict JSON command batch targeting the current Resolve timeline + selected clip.
4. App generates dry-run preview of all actions with estimated impact.
5. User reviews each action one-by-one in approval panel.
6. For each action: user chooses **approve**, **skip**, or **cancel batch**.
7. Approved actions execute in Resolve.
8. All actions logged to JSON file (success + failure state).

---

## 2. Input & AI Model

- **Input format**: Strict JSON only (text parsed → JSON).
- **Input modality**: Text only in v1 (no speech-to-text).
- **AI approach**: Fully offline local model (no cloud calls).
- **Runtime**: llama.cpp packaged inside app (embedded inference).
- **Training**: Inference only in v1 (no fine-tuning inside app).
- **Schema version**: Implicit (no schema_version field required).
- **Unknown fields/actions**: Trigger manual confirmation before executing.

---

## 3. Supported Editing Actions in v1

### Timeline & Clip Management
- `add_marker` - Add marker at frame with color, name, note, duration.
- `rename_clip` - Set clip name.
- `set_clip_enabled` - Enable/disable clip on timeline.
- `cut_split_at_timecode` - Split clip at specified timecode.
- `set_in_point` - Set in-point of clip.
- `set_out_point` - Set out-point of clip.
- `move_trim_clip` - Move or trim clip (offset/duration).

### Transitions
- `insert_transition` - Insert transition between clips.
  - **Whitelist**: Cross Dissolve, Dip to Color only.
  - **Duration range**: 6–30 frames (enforced hard).
  - **Type/duration**: AI decides, app enforces guardrails.

### Color Corrections
- `add_color_node` - Add color correction node to clip.
- `set_exposure` - Set exposure/offset.
- `set_contrast` - Set contrast/pivot.
- `set_saturation` - Set saturation.
- `set_temperature` - Set temperature/tint.
- `set_lift_gamma_gain` - Set lift, gamma, gain values.
- `apply_lut` - Apply LUT by name.
- `enable_disable_node` - Toggle color node on/off.
- `remove_node` - Remove color correction node.

### Metadata & Labels
- `set_color_label` - Assign clip color label/tag.

---

## 4. Target Selection

- **Primary target**: Current active timeline in Resolve.
- **Clip selection logic**:
  - If user selects a clip in Resolve → use selected clip.
  - If no clip selected → app shows list of clips from video track 1 for user to choose.
- **Track**: Video track 1 only in v1.

---

## 5. Safety & Execution Flow

### Dry-Run Phase
- All actions run in **read-only mode** first.
- Dry-run shows:
  - Action type.
  - Target (clip name/index).
  - Parameters.
  - Estimated impact (e.g., "Marker at 100 frames", "Marker color will be Blue").

### Approval Phase
- User reviews **each action one-by-one**.
- Per-action options: **Approve**, **Skip**, **Cancel Batch**.
- If user cancels batch → stop, no remaining actions execute.
- If user skips action → mark as skipped, move to next.
- If user approves → execute and log result.

### Failure Handling
- If an action fails during execution → ask user:
  - "Action X failed: [error]. Continue with remaining actions?"
  - Yes → continue to next action.
  - No → stop batch, log all results so far.

### Reliability Target
- Success criteria: 20 edits on one timeline, **100% pass rate** (20/20).

---

## 6. User Interface

- **Type**: Desktop application (not web, not CLI).
- **Stack**: Electron + local Python bridge.
- **Components**:
  - Text input panel (user types prompt).
  - Dry-run preview list (read-only).
  - Action approval panel (per-action review).
    - Shows: type, target, params, estimated impact.
  - Execution log viewer (session history).
  - Settings panel (model, Resolve path, etc.).

---

## 7. Logging & Audit

- **Format**: Local JSON log files (one per session).
- **Per-action logged**:
  - Timestamp (ISO 8601 UTC).
  - Action type.
  - Target (clip name/index).
  - Parameters.
  - Dry-run result (if applicable).
  - Execution result (ok: bool, error: string if failed).
  - Duration (milliseconds).
- **Log location**: `~/.resolve-ai-agent/logs/` with session ID in filename.
- **No best-effort undo** in v1.

---

## 8. Resolve Scripting Connection

- **API**: DaVinciResolveScript (Python binding).
- **Platform**: Windows local only.
- **Connection**: Assume Resolve is open, scripting enabled.
- **Module path**: Default Windows path or env var `RESOLVE_SCRIPT_API`.
- **Error handling**: Fail gracefully with clear message if Resolve not accessible.

---

## 9. Command Schema (Strict JSON)

All commands follow this structure:

```json
{
  "timeline_id": "auto",
  "actions": [
    {
      "type": "action_name",
      "target": {
        "clip_id": "auto" | "user_selected" | "clip_name",
        "track": "video_1"
      },
      "params": {
        // action-specific parameters
      }
    }
  ]
}
```

Unknown fields → prompt user for confirmation before execution.

---

## 10. Acceptance Test (v1 Success Criteria)

**Test**: Execute 20 distinct editing actions on a single Resolve timeline.

**Pass threshold**: 100% (all 20 must succeed).

**Sample actions for test**:
1. Add marker at frame 100, green, name "Beat 1".
2. Rename first clip to "Intro".
3. Enable first clip.
4. Split clip at timecode 00:00:05:00.
5. Set in-point to frame 50.
6. Set out-point to frame 200.
7. Add transition (Cross Dissolve, 12 frames).
8. Move clip +2 seconds.
9. Add color node.
10. Set exposure to +0.5.
11. Set contrast to +0.3.
12. Set saturation to +0.2.
13. Set temperature to +100.
14. Set lift to +0.1, gamma to 1.0, gain to +0.1.
15. Apply LUT by name.
16. Enable color node.
17. Remove color node.
18. Set clip color label to "Red".
19. Insert transition (Dip to Color, 10 frames).
20. Add marker at frame 500, blue, name "End".

**Expected outcome**: All 20 log entries show `ok: true`, zero failures.

---

## 11. Future Considerations (NOT in v1)

- Speech-to-text input.
- Cloud API fallback.
- Fine-tuning the embedded model.
- Undo/rollback generation.
- Multi-timeline batching.
- Track selection (non-video track 1).
- Timeline creation/management.

---

## Sign-Off

**Locked by**: User
**Date**: 2026-04-19
**Status**: Ready for implementation.