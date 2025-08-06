# VRChat Avatar URL Extractor

A simple, user-friendly desktop application to extract the VRChat avatar ID from a file and generate the corresponding VRChat Home URL.

## Table of Contents
- [Features](#features)
- [How to Use the Application](#how-to-use-the-application)
  - [Installation and Setup](#installation-and-setup)
  - [Main Functionality](#main-functionality)
  - [Customization (Settings)](#customization-settings)
- [How the Application Works (Technical Breakdown)](#how-the-application-works-technical-breakdown)
  - [Core Dependencies](#core-dependencies)
  - [Program Flow and Logic](#program-flow-and-logic)
- [License](#license)

## Features
- **Drag and Drop Interface:** Easily process files by dropping them directly onto the application window.
- **File Dialog Support:** Use a standard file explorer to select VRChat files.
- **URL Generation:** Automatically constructs a valid VRChat Home URL from the avatar ID in the file name.
- **Copy to Clipboard:** One-click functionality to copy the generated URL.
- **Auto-Copy Option:** A quality-of-life setting to automatically copy the URL upon successful file processing.
- **Customizable Appearance:** Switch between dark and light themes or choose a custom background color.
- **Dependency Management:** Automatically installs the required `tkinterdnd2` package if it's missing.

## How to Use the Application

The application is designed to be intuitive and offers two primary ways to find your avatar URL.

### Installation and Setup
1.  **Dependencies:** Ensure you have Python installed on your system.
2.  **Required Packages:** The script will automatically check for and install the necessary package, `tkinterdnd2`, if it's not present. If automatic installation fails, you can manually install it by running the following command in your terminal:
    ```bash
    pip install tkinterdnd2
    ```
3.  **Running the Script:** Save the provided code as a Python file (e.g., `vrchat_url_extractor.py`) and run it from your terminal:
    ```bash
    python vrchat_url_extractor.py
    ```

### Main Functionality
Once the application window appears, you can use it in one of two ways:

1.  **Drag and Drop (Recommended):**
    * Locate the VRChat avatar file you want to use. This file typically has an ID in its name, such as `avtr_12345678-xxxx-xxxx-xxxx-xxxxxxxxxxxx.unity3d`.
    * Drag the file from your file explorer directly onto the application window.
    * The application will instantly extract the avatar ID and display the full VRChat URL in the text box.

2.  **"Select File" Button:**
    * Click the **"Select File"** button. This will open a standard file dialog.
    * Navigate to and select the desired VRChat file.
    * After you select the file, the URL will appear in the text box.

After the URL appears, you have a few options:
* **Copy the URL:** Click the **"Copy URL"** button to copy the URL to your clipboard. A confirmation message will appear.
* **Clear the Interface:** Click the **"Clear"** button to reset the display and prepare for another file.

### Customization (Settings)
The application includes a settings menu to customize the appearance:

1.  **Accessing Settings:** Click the **"Settings"** button to switch to the customization menu.
2.  **Change Background Color:** Click the **"Change Background Color"** button to open a color chooser and select a custom background color for the application. The button and text colors will automatically adjust for readability.
3.  **Toggle Dark/Light Mode:** Click the **"Toggle Dark/Light Mode"** button to quickly switch between the predefined dark and light color themes.
4.  **Auto-Copy URL to Clipboard:** This is a convenient quality-of-life feature. Check the box to automatically copy the generated URL to your clipboard every time you successfully process a file, saving you an extra click.
5.  **Return to Main UI:** Click the **"Back"** button to return to the main file processing screen.

---

### How the Application Works (Technical Breakdown)

The script is a self-contained Python program that handles its own dependencies and UI logic.

#### Core Dependencies
* **`tkinter` and `ttk`:** These are Python's standard GUI libraries. `tkinter` provides the basic window and widgets, while `ttk` (Themed Tkinter) offers a more modern and customizable look and feel.
* **`tkinterdnd2`:** This third-party library is crucial for the drag-and-drop functionality. It extends `tkinter` by adding event bindings that allow the application to respond when a file is dropped onto its window.
* **`subprocess` and `sys`:** Used to programmatically install missing Python packages via `pip`. This ensures the application can set itself up without manual intervention.

#### Program Flow and Logic
1.  **Initialization:** When the script runs, the `install_missing_dependencies()` function is called first. It checks if `tkinterdnd2` is installed and attempts to install it if it's not found.
2.  **GUI Setup:** The main application window (`root`) is created. If `tkinterdnd2` is available, a custom `DragDropTk` class is used to enable the drag-and-drop feature. Otherwise, a standard `tk.Tk` window is created, and a warning is displayed.
3.  **File Processing (`process_file`):** This is the heart of the application's logic.
    * A `filepath` is passed to this function, either from a drag-and-drop event or the file dialog.
    * The `extract_avatar_id()` function is called, which uses a regular expression (`re.search(r"(avtr_[0-9a-fA-F-]+)", filename)`) to find a specific pattern in the file name: `avtr_` followed by a sequence of hexadecimal characters and hyphens. This pattern reliably identifies VRChat avatar IDs.
    * If an ID is found, the function constructs the full VRChat URL using a formatted string: `f"https://vrchat.com/home/avatar/{avtr_id}"`.
    * The URL is then displayed in the `url_entry` text box.
    * **Auto-Copy Feature:** A key addition to this function is the check `if auto_copy_var.get():`. If the `auto_copy_var` variable (linked to the settings checkbox) is `True`, the `copy_url()` function is automatically called, copying the new URL to the clipboard.
4.  **Theming (`apply_theme`):** The `apply_theme()` function dynamically changes the application's appearance. It uses pre-defined color dictionaries for dark and light modes and a custom color from the color chooser. It relies on `ttk.Style()` to modify the colors and fonts of the widgets, ensuring a consistent and integrated look.
5.  **User Preferences:** Settings like the theme and the `auto_copy` option are stored in global variables (`dark_mode`, `custom_bg_color`, `auto_copy_var`). While these settings are not persistent between sessions, they allow for a fully dynamic user experience during a single run.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
