"""
RagilGitClone - Main GUI Application
Modern batch GitHub repository cloner with sleek Apple-like UI

Author: Ragilmalik
Version: 1.0.0
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os
from datetime import datetime
from typing import List

# Import our modules
from url_parser import extract_urls_from_file, parse_manual_input
from git_operations import clone_repository
from report_generator import generate_report


# Modern Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RagilGitCloneApp(ctk.CTk):
    """Main application window with modern UI"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Ragilmalik Git Cloner")
        self.geometry("900x750")
        self.minsize(800, 700)

        # Configure window colors - Pure black background
        self.configure(fg_color="#000000")

        # Application state
        self.selected_file_path = None
        self.selected_destination = None
        self.urls_to_clone = []
        self.clone_results = []
        self.is_cloning = False
        self.stop_requested = False

        # Initialize UI
        self.create_widgets()

    def create_widgets(self):
        """Create all UI components with modern styling and scrollable layout"""
        
        # 1. Fixed Header (Top)
        # We create a wrapper frame for the header to ensure it stays at the top
        header_wrapper = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        header_wrapper.pack(side="top", fill="x", padx=0, pady=0)
        
        self.create_header(header_wrapper)

        # 3. Fixed Footer (Bottom) - Created before scroll frame to ensure it's at bottom
        # This ensures buttons are always visible above taskbar
        footer_wrapper = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0, height=80)
        footer_wrapper.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.create_action_buttons(footer_wrapper)

        # 2. Scrollable Content (Middle)
        # This takes up all remaining space
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#000000",
            corner_radius=0,
            label_text=""
        )
        self.scroll_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(10, 0))

        # Add sections to scrollable area
        
        # File Input Section
        self.create_file_section(self.scroll_frame)

        # Manual URL Input Section
        self.create_manual_input_section(self.scroll_frame)

        # Destination Folder Section
        self.create_destination_section(self.scroll_frame)

        # Settings Section (Delay + Report Format)
        self.create_settings_section(self.scroll_frame)

        # Progress Section
        self.create_progress_section(self.scroll_frame)

        # Status Log Section
        self.create_log_section(self.scroll_frame)

    def create_header(self, parent):
        """Create application header"""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color="#000000",
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=(0, 20))

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 Ragilmalik Git Cloner",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(0, 5))

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Batch GitHub Repository Cloner with Smart Reporting",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        subtitle_label.pack()

    def create_file_section(self, parent):
        """Create file input section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="x", pady=(0, 15))

        # Section label
        label = ctk.CTkLabel(
            section_frame,
            text="📁 Import URLs from File",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 10))

        # File selection container
        file_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        file_container.pack(fill="x", padx=20, pady=(0, 15))

        # Open File Button
        self.open_file_btn = ctk.CTkButton(
            file_container,
            text="Choose File",
            command=self.open_file_dialog,
            width=140,
            height=40,
            corner_radius=10,
            fg_color="#1E90FF",
            hover_color="#1873CC",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"  # Black text
        )
        self.open_file_btn.pack(side="left", padx=(0, 10))

        # File path label
        self.file_path_label = ctk.CTkLabel(
            file_container,
            text="No file selected",
            font=ctk.CTkFont(size=13),
            text_color="#666666",
            anchor="w"
        )
        self.file_path_label.pack(side="left", fill="x", expand=True)

    def create_manual_input_section(self, parent):
        """Create manual URL input section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="x", pady=(0, 15))

        # Section label
        label = ctk.CTkLabel(
            section_frame,
            text="✍️ Manual URL Input",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 10))

        # Help text
        help_label = ctk.CTkLabel(
            section_frame,
            text="Enter GitHub URLs (one per line). .git suffix will be added automatically.",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            anchor="w"
        )
        help_label.pack(fill="x", padx=20, pady=(0, 10))

        # Text input
        self.manual_urls_text = ctk.CTkTextbox(
            section_frame,
            height=100,
            corner_radius=10,
            fg_color="#0F0F0F",
            border_width=1,
            border_color="#2A2A2A",
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF"
        )
        self.manual_urls_text.pack(fill="x", padx=20, pady=(0, 15))
        
    def create_destination_section(self, parent):
        """Create destination folder section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="x", pady=(0, 15))

        # Section label
        label = ctk.CTkLabel(
            section_frame,
            text="📂 Destination Folder",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 10))

        # Folder selection container
        folder_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        folder_container.pack(fill="x", padx=20, pady=(0, 15))

        # Choose Folder Button
        self.choose_folder_btn = ctk.CTkButton(
            folder_container,
            text="Choose Folder",
            command=self.choose_destination_folder,
            width=140,
            height=40,
            corner_radius=10,
            fg_color="#1E90FF",
            hover_color="#1873CC",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"  # Black text
        )
        self.choose_folder_btn.pack(side="left", padx=(0, 10))

        # Folder path label
        self.folder_path_label = ctk.CTkLabel(
            folder_container,
            text="No folder selected",
            font=ctk.CTkFont(size=13),
            text_color="#666666",
            anchor="w"
        )
        self.folder_path_label.pack(side="left", fill="x", expand=True)

    def create_settings_section(self, parent):
        """Create settings section (delay + report format)"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="x", pady=(0, 15))

        # Section label
        label = ctk.CTkLabel(
            section_frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 10))

        # Settings container
        settings_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        settings_container.pack(fill="x", padx=20, pady=(0, 15))

        # Left side - Delay slider
        delay_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        delay_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))

        self.delay_label = ctk.CTkLabel(
            delay_frame,
            text="Clone Delay: 5 seconds",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        self.delay_label.pack(fill="x", pady=(0, 8))

        self.delay_slider = ctk.CTkSlider(
            delay_frame,
            from_=1,
            to=60,
            number_of_steps=59,
            command=self.update_delay_label,
            width=300,
            height=20,
            button_color="#00BCD4",
            button_hover_color="#0097A7",
            progress_color="#00BCD4",
            fg_color="#2A2A2A"
        )
        self.delay_slider.set(5)  # Default 5 seconds
        self.delay_slider.pack(fill="x")

        # Right side - Report format
        report_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        report_frame.pack(side="left")

        report_label = ctk.CTkLabel(
            report_frame,
            text="Report Format:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        report_label.pack(fill="x", pady=(0, 8))

        # Radio buttons container
        radio_container = ctk.CTkFrame(report_frame, fg_color="transparent")
        radio_container.pack()

        self.report_format = ctk.StringVar(value="xlsx")

        xlsx_radio = ctk.CTkRadioButton(
            radio_container,
            text="XLSX",
            variable=self.report_format,
            value="xlsx",
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            fg_color="#00BCD4",
            hover_color="#0097A7"
        )
        xlsx_radio.pack(side="left", padx=(0, 15))

        csv_radio = ctk.CTkRadioButton(
            radio_container,
            text="CSV",
            variable=self.report_format,
            value="csv",
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            fg_color="#00BCD4",
            hover_color="#0097A7"
        )
        csv_radio.pack(side="left")

    def create_progress_section(self, parent):
        """Create progress bar section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="x", pady=(0, 15))

        # Progress label
        self.progress_label = ctk.CTkLabel(
            section_frame,
            text="Ready to clone",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        self.progress_label.pack(fill="x", padx=20, pady=(15, 8))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            section_frame,
            width=400,
            height=12,
            corner_radius=6,
            fg_color="#2A2A2A",
            progress_color="#00FFFF",
            border_width=0
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)

    def create_log_section(self, parent):
        """Create status log section"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#0A0A0A",
            corner_radius=15,
            border_width=1,
            border_color="#1E1E1E"
        )
        section_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Log label
        label = ctk.CTkLabel(
            section_frame,
            text="📋 Status Log",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 10))

        # Log textbox
        self.log_text = ctk.CTkTextbox(
            section_frame,
            height=120,
            corner_radius=10,
            fg_color="#0F0F0F",
            border_width=1,
            border_color="#2A2A2A",
            font=ctk.CTkFont(size=12, family="Consolas"),
            text_color="#00FFFF"  # Cyan
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Make read-only but selectable
        # We block all keys except Copy (Ctrl+C)
        def prevent_write(event):
            # Allow Ctrl+C (Copy)
            if (event.state & 4) and event.keysym.lower() == 'c':
                return None
            # Allow arrow keys for navigation
            if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Home', 'End', 'Prior', 'Next'):
                return None
            # Block everything else
            return "break"

        self.log_text.bind("<Key>", prevent_write)

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 0))

        # Start Clone Button
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Start Clone",
            command=self.start_cloning,
            width=140,
            height=36,
            corner_radius=10,
            fg_color="#00BCD4",  # Cyan
            hover_color="#0097A7",  # Darker Cyan
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"  # Black text
        )
        self.start_btn.pack(side="left", padx=(0, 10))

        # Stop Button
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏸️ Stop",
            command=self.stop_cloning,
            width=100,
            height=36,
            corner_radius=10,
            fg_color="#FF3333",
            hover_color="#CC0000",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 10))

        # Clear Button
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            width=100,
            height=36,
            corner_radius=10,
            fg_color="#666666",
            hover_color="#555555",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF",
            anchor="center"  # Centered text
        )
        self.clear_btn.pack(side="left")

    # Event handlers
    def open_file_dialog(self):
        """Open file dialog to select input file"""
        file_path = filedialog.askopenfilename(
            title="Select file with GitHub URLs",
            filetypes=[
                ("All supported", "*.txt *.csv *.xlsx *.md"),
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.selected_file_path = file_path
            self.file_path_label.configure(text=os.path.basename(file_path), text_color="#FFFFFF")
            self.log_message(f"✓ File selected: {os.path.basename(file_path)}")

    def choose_destination_folder(self):
        """Choose destination folder for cloned repositories"""
        folder_path = filedialog.askdirectory(title="Select destination folder")

        if folder_path:
            self.selected_destination = folder_path
            self.folder_path_label.configure(text=folder_path, text_color="#FFFFFF")
            self.log_message(f"✓ Destination set: {folder_path}")

    def update_delay_label(self, value):
        """Update delay label when slider moves"""
        seconds = int(float(value))
        self.delay_label.configure(text=f"Clone Delay: {seconds} seconds")

    def log_message(self, message, color=None):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        # We keep state="normal" so user can select text,
        # but we prevented writing via key bindings.
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")

    def clear_all(self):
        """Clear all inputs and logs"""
        self.selected_file_path = None
        self.selected_destination = None
        self.urls_to_clone = []
        self.clone_results = []

        self.file_path_label.configure(text="No file selected", text_color="#666666")
        self.folder_path_label.configure(text="No folder selected", text_color="#666666")
        self.manual_urls_text.delete("1.0", "end")

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready to clone")

        self.log_message("✓ All fields cleared")

    def start_cloning(self):
        """Start the cloning process"""
        # Gather URLs
        self.urls_to_clone = []

        # From file
        if self.selected_file_path:
            try:
                file_urls = extract_urls_from_file(self.selected_file_path)
                self.urls_to_clone.extend(file_urls)
                self.log_message(f"✓ Extracted {len(file_urls)} URLs from file")
            except Exception as e:
                self.log_message(f"✗ Error reading file: {str(e)}")

        # From manual input
        manual_text = self.manual_urls_text.get("1.0", "end").strip()
        if manual_text:
            manual_urls = parse_manual_input(manual_text)
            self.urls_to_clone.extend(manual_urls)
            self.log_message(f"✓ Added {len(manual_urls)} URLs from manual input")

        # Remove duplicates
        self.urls_to_clone = list(set(self.urls_to_clone))

        # Validate
        if not self.urls_to_clone:
            messagebox.showerror("Error", "No valid GitHub URLs found!")
            return

        if not self.selected_destination:
            messagebox.showerror("Error", "Please select a destination folder!")
            return

        # Start cloning in thread
        self.is_cloning = True
        self.stop_requested = False
        self.clone_results = []

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.log_message(f"🚀 Starting batch clone of {len(self.urls_to_clone)} repositories...")

        threading.Thread(target=self.clone_worker, daemon=True).start()

    def stop_cloning(self):
        """Stop the cloning process"""
        self.stop_requested = True
        self.stop_btn.configure(state="disabled")

    def generate_final_report(self):
        """Generate final report"""
        if not self.clone_results:
            return

        report_format = self.report_format.get()
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
        report_name = f"Git_Clone_Batch_{timestamp}"

        report_path = os.path.join(self.selected_destination, report_name)

        success, message = generate_report(self.clone_results, report_path, report_format)

        if success:
            self.log_message(f"✓ {message}")
            messagebox.showinfo(
                "Success",
                f"Cloning completed!\n\n{message}"
            )
        else:
            self.log_message(f"✗ Failed: {message}")
            messagebox.showerror("Report Error", message)


    def interpolate_color(self, start_hex, end_hex, progress):
        """Interpolate between two hex colors"""
        def hex_to_rgb(h):
            return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

        def rgb_to_hex(r, g, b):
            return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

        start_rgb = hex_to_rgb(start_hex)
        end_rgb = hex_to_rgb(end_hex)

        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress

        return rgb_to_hex(r, g, b)

    def clone_worker(self):
        """Worker thread for cloning repositories"""
        total = len(self.urls_to_clone)
        delay = int(self.delay_slider.get())

        # Colors for progress bar (Red to Green)
        color_start = "#FF0000"
        color_end = "#00FF00"

        for index, url in enumerate(self.urls_to_clone, 1):
            if self.stop_requested:
                self.log_message("⏸️ Cloning stopped by user")
                break

            # Update progress
            progress = (index - 1) / total
            current_color = self.interpolate_color(color_start, color_end, progress)
            self.progress_bar.configure(progress_color=current_color)
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"Cloning {index}/{total}: {url}")

            # Clone repository
            self.log_message(f"⏳ Cloning {url}...")
            result = clone_repository(url, self.selected_destination)
            self.clone_results.append(result)

            if result['success']:
                self.log_message(f"✓ Success: {result['repo_name']} ({result['size_kb']} kB)")
            else:
                self.log_message(f"✗ Failed: {result['error']}")

            # Update progress
            progress = index / total
            current_color = self.interpolate_color(color_start, color_end, progress)
            self.progress_bar.configure(progress_color=current_color)
            self.progress_bar.set(progress)

            # Delay before next clone
            if index < total and not self.stop_requested:
                self.log_message(f"⏰ Waiting {delay} seconds...")
                time.sleep(delay)

        # Finish
        if not self.stop_requested:
            self.progress_bar.set(1.0)
            self.progress_bar.configure(progress_color=color_end) # Final green
            self.progress_label.configure(text=f"✓ Completed {total} repositories")
            self.log_message("=" * 50)
            self.log_message(f"✓ Batch clone completed!")

            # Generate report
            self.generate_final_report()

        # Reset UI
        self.is_cloning = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")



def main():
    """Main entry point"""
    app = RagilGitCloneApp()
    app.mainloop()


if __name__ == "__main__":
    main()
