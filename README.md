# WCW Backstage Assault — Native Windows Recompilation

Experimental unofficial Windows x64 recompilation of the PlayStation USA release (SLUS-01274), originally developed by Kodiak Interactive, using static MIPS-to-C recompilation and PSXRecomp, SDL3, OpenGL and OpenBIOS.

## Credits

Development was informed by [dotGrx/WCW-Mayhem-RECOMP](https://github.com/dotGrx/WCW-Mayhem-RECOMP), particularly its technical approach, build structure and runtime integration. WCW Mayhem is a separate game and project. Thanks also to the PSXRecomp, SDL3 and OpenBIOS contributors.

## Development status — Stage 15B.3

- Stage 14: Windows gameplay reported near-perfect with keyboard input.
- Wired PS4 controller: D-pad and left analogue movement confirmed.
- Stage 15B.1: FPS overlay confirmed working.
- Stage 15B.2: F9 aspect ratio stretching confirmed working.
- Stage 15B.3: experimental 16:9, 17:9 and 21:9 GTE projection modes compiled; additional scenery rendering and clipping remain unverified.
- Advanced Options: separate prototype; original menu integration pending.

## Roadmap

- True widescreen and ultrawide with correct geometry clipping, HUD and video proportions.
- Right analogue stick camera control, R3 reset and automatic camera preservation.
- Direct HDD/SSD asset loading while preserving virtual CD-ROM timing, interrupts and XA sector data.
- Faster MDEC playback with audio synchronisation, deblocking, deringing and improved scaling.
- Integrated advanced graphics, controller, audio and diagnostics options.
- Reproducible Windows x64 builds and regression testing.

## Build and distribution

Development used LLVM-MinGW UCRT, SDL3 3.4.18 and PSXRecomp revision `8077e71098ce0347d7d41d267630bc856816cf77`. Source import is pending. Users must supply their own legally obtained game disc and any required BIOS resources. No original disc or extracted game assets are included. Game-derived generated code requires a separate rights assessment before public distribution. Respect upstream licences, including PSXRecomp's noncommercial terms. This project is not affiliated with the original rights holders.
