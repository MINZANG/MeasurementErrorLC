# Line-to-Point Measurement Error Demo

This repository contains a Manim project demonstrating the **LC error from a point to a line**.

## Animation

### GIF Example

- ❌ <span style="color:red">Incorrect measurement</span>
![LC Error Animation](output/videos/run/480p15/MeasurementErrorLC_ManimCE_v0.19.0.gif)

Using <span style="color:red">line-to-point</span> distance is prone to errors caused by line inclination.

- ✅ <span style="color:green">Correct measurement</span>
![DX Correct Animation](output/videos/run2/480p15/MeasurementDx_ManimCE_v0.19.0.gif)

Using <span style="color:green">point-to-point</span> X-coordinate distance to reduce errors caused by line segment inclination.

## Installation

Before running the scripts, install the required Python packages:

```bash
pip install manim pydub