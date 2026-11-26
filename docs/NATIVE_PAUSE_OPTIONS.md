# Native pause options expansion
Priority: CPU movement disable, then directional movement improvements. Preserve original START pause menu and native graphics/navigation. No unverified guest memory writes.

## Match Rules
Players, Difficulty, Special Rules (Regular / First Blood), Brawl Length, Realism, Blood, Pinfall, Submission, Knock Outs. Trace original variables and interactions before adding independent overrides. Mid-match player ownership requires validation.

## Volume Settings
Music Volume, Speech Volume, Sound FX, Crowd Volume. Share original global settings.

## Video Settings
Rename Intro Videos to Entrance Videos after confirming original semantics.
- Startup Logo: VEADOLBY
- Game Intro: VMAYHEM
- Entrance Videos: numbered 0–60
- Hardcore Title Video: HARDCORE
- US Title Video: US
- World Title Video: WORLD
- All Videos: master override
Asset classifications supplied by tester; verify against disc directory. Trace original entrance toggle, request dispatcher, completion and skip path. Preserve audio cleanup and state transitions. Persist startup flags before playback. Unknown assets retain original behavior.

## HUD / UI Settings
Master HUD, Wrestler Names, Match Clock, P1/P2/CPU Indicators, Health Bars, Stamina Bars, Momentum, Move Names, Go for KO, Knockout, Stunned, Max Momentum, Aerial Opportunity, Damage Multiplier, Other Messages. Hide rendering only, not gameplay state.

## Controller Settings
Original/enhanced movement, 360-degree analogue, enhanced D-pad, smooth turning, deadzone, sensitivity, turning speed, camera tracking, vibration.

## Gameplay Testing
CPU Movement (default ON), CPU Turning, Attacks, Grappling, Blocking, Weapon Use; proposed infinite health/stamina and freeze timer. Suppress autonomous commands, preserve physics and reactions.

## Acceptance
Original defaults and saved settings remain compatible. Verify native menu navigation, CPU idle and resume, controller trace, each FMV category, match transitions and HUD isolation. This document is a specification, not implemented features.

## Display and persistence
Preserve F1–F12 assignments; no new hotkeys. Display Settings exposes existing resolution, aspect, fullscreen, filtering, scanlines, geometry, vsync and FPS controls. Use game.toml defaults, settings.toml overrides and existing CLI precedence. Preserve compatibility with AdvancedOptions.exe; exact standalone source not yet identified. Native menu is primary interface.

## Diagnostics & Reporting
Master switch plus independent controls for freeze dumps (psx_freeze_dump_psx-runtime_*), overlay_captures.json, psx_freeze_heartbeat.json, psx_last_run_report.json, starvation_dump.jsonl, wcw-pup-trace.csv, wcw-pad-trace.csv, wcw-pause-trace.csv, psx_cps_exit_trace.json and console logging. Store preferences in settings.toml [wcw_diagnostics]. Audit all writers; keep watchdog protection active, distinguish required overlay metadata from optional output, preserve existing files and saves. No new function keys. These are requirements, not implemented switches.

## Approved menu separation (supersedes earlier shared-menu proposals)
Main Menu > Global Options retains original rows and adds Advanced Options as a separate page for display, graphics, audio quality, controller configuration, runtime performance and diagnostics. Main Menu > Cheats is a separate native entry; recover existing cheat window functionality and preserve original button combinations. START > Pause > Options remains a separate gameplay menu for match rules, volume, video, HUD, controller and gameplay testing. Do not link pause options to Advanced Options. Shared configuration storage is allowed, not shared menu interfaces. Preserve current function-key assignments. CPU movement and directional movement remain first gameplay priorities. Native menu hooks and cheat integration are not yet implemented.

## Stage 15B.103 — Priority change
Controller movement research is on hold at Stage 15B.102. Preserve working analogue-to-D-pad compatibility and existing research. Prioritize native menu integration: first locate original Global Options menu entry/render/navigation/selection handlers, then add a separate Advanced Options entry and page using existing settings functionality. Cheats and in-match Pause Options remain separate. Do not add hotkeys or replace original menus. No native menu implementation is claimed at this checkpoint.
