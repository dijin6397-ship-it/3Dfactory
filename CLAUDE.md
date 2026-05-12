# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 3D visualization project for Shanghai Beizhai Road Vehicle Depot Maintenance Workshop (上海北翟路车辆段检修库). It converts CAD/DXF floor plans into interactive 3D models using Three.js.

## Tech Stack

- **Frontend**: Three.js + Vite (single-page app in `3d-factory-viewer/`)
- **Data Pipeline**: Python script `parse_dxf.py` extracts entities from `.dxf` files to JSON
- **CAD Files**: `.dwg` and `.dxf` source drawings in the project root

## Development Commands

```bash
cd 3d-factory-viewer
npm install
npm run dev      # Start dev server on http://localhost:3000
npm run build    # Production build
npm run preview  # Preview production build
```

For the DXF parser:
```bash
pip install ezdxf
python parse_dxf.py
```

## Architecture

### Data Flow

1. **Source**: `.dxf` CAD drawing (root directory)
2. **Extraction**: `parse_dxf.py` reads DXF → outputs `src/dxf_raw_data.json`
3. **Visualization**: `src/main.js` hardcodes factory layout data and renders via Three.js

### Key Files

- `src/main.js` — All 3D scene logic: factory data model, mesh creation, camera controls, raycasting for tooltips
- `src/style.css` — UI overlay styling (dark theme)
- `index.html` — Entry point with control panel UI
- `parse_dxf.py` — DXF entity extraction (lines, polylines, circles, arcs, text, blocks)

### 3D Scene Structure

The scene hierarchy: Scene → Floor → Walls → Tracks → Zones → Stations → Labels

- **Tracks** (股道): 20 parallel rail lines rendered as blue boxes with sleeper decorations
- **Zones** (区域): 6 functional areas (parking, maintenance, inspection, cleaning, equipment, office) as semi-transparent colored planes
- **Stations** (工位): 60 workstations distributed across zones as green boxes with sprite labels
- **Labels**: Canvas-based sprite textures for zone names and station IDs

### Interaction Model

- OrbitControls for camera (pan, rotate, zoom)
- Raycaster-based hover tooltips on stations and zones
- Toggle controls for tracks/zones/labels/floor visibility
- Preset camera views (reset, top-down, side)

## Notes

- Factory dimensions and positions are hardcoded in `factoryData` — update there for layout changes
- The `parse_dxf.py` output (`dxf_raw_data.json`) is not currently consumed by the frontend; the 3D model uses manually defined coordinates
- Chinese language throughout (UI, comments, data)

## User Preferences

- **始终使用中文**：所有回复、说明、解释必须使用中文。代码本身（变量名、函数名等）保持英文。
