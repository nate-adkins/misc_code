# Planning & Voronoi Diagrams

## Plan

Make a proof of concept for Hybrid Slope/Voronoi Diagram

### Features

- Save/load maps
- Specify cell size
- Specify height map size
- Can paint and create maps
  - brush size
  - does a relative adding to existing cells
  - visualize brush on grid

### Layers

- can turn on/off layers, can slide opacity of layers, can select colors
- Slope Map (default grayscale, white low, black high)
- Voroni Diagram Output (lime green)
- Paths (red)

### Inputs

- Height Map input numpy array
  - Can create
    - Slope Map
    - Voroni Diagram

## Outputs

- Run A* on numpy array
- Run A* on Voroni Diagram
