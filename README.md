# SynImages - Synthetic Image Generation Addon for Blender

SynImages is a Python extension for Blender designed to automate the generation and organization of synthetic image datasets from 3D CAD models. This tool bridges the gap between 3D modeling and machine learning by providing an efficient pipeline to create labeled training data for Convolutional Neural Networks (CNNs).

## Features

* **Automated Dataset Generation:** Rapidly generate large volumes of synthetic images from existing 3D CAD models.
* **Dataset Organization:** Automatically structures and organizes the output files, making them ready for deep learning frameworks like PyTorch and fast.ai.
* **Native Blender Integration:** Built directly into Blender using its Python API, featuring custom operators, panels, and properties for a seamless user experience.

## Project Structure

The addon is modularized for better maintainability:

* `__init__.py`: Addon initialization and metadata.
* `operators.py`: Contains the core logic and Blender operators for image generation.
* `panels.py`: Defines the user interface (UI) within Blender.
* `properties.py`: Manages the variables and settings used across the addon.
* `handler.py`: Manages Blender application handlers.
* `utils.py`: Helper functions for rendering and dataset organization.

## Installation

1. Download the latest release or clone this repository.
2. If you cloned the repository, zip the `AddonSynImages-main` folder.
3. Open Blender and go to **Edit > Preferences > Add-ons**.
4. Click on **Install...** and select the `.zip` file.
5. Check the box next to **SynImages** to enable it.

## Usage

1. Import your 3D CAD model into the Blender scene.
2. Open the SynImages panel in the 3D Viewport sidebar (N-panel).
3. Configure your dataset parameters (camera angles, lighting variations, resolution).
4. Click **Generate Dataset** to start the automated rendering and labeling process.

## Technologies Used

* **Python**
* **Blender API (bpy)**
* Focused on generating data for **PyTorch / fast.ai** models
