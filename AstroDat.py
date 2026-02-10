import customtkinter as tk
from Database_code import DatabaseManager
from ObservationService import ObservationService

# UI (AstroDat.py) -> Service (ObservationService.py) -> Database (Database_code.py)

class AstrodatApp(tk.CTk):
    """
    The main GUI class
    """
    def __init__(self):
        super().__init__()
        db_manager = DatabaseManager()
        self.service = ObservationService(db_manager)
        
        self.title("Astrodat | Observer Pro")
        self.geometry("1000x600")
        tk.set_appearance_mode("dark")
        
        self.main_container = tk.CTkFrame(self, fg_color="transparent")
        self.detail_container = tk.CTkFrame(self, fg_color="#0F1113")
        
        self._setup_main_view()
        self.show_main_screen()

    def _setup_main_view(self):
        """Initializes all widgets"""

        # Left Panel
        self.entrys_frame = tk.CTkFrame(self.main_container, width=300, corner_radius=0, fg_color="#1A1C1E")
        self.entrys_frame.pack(side="left", fill="y")

        tk.CTkLabel(self.entrys_frame, text="LOG OBSERVATION", font=("Segoe UI", 20, "bold"), text_color="#00978A").pack(pady=(30, 20), padx=20)

        self.entry_object = self._create_input_field(self.entrys_frame, "OBJECT", "e.g. Andromeda")
        self.entry_date = self._create_input_field(self.entrys_frame, "DATE", "YYYY-MM-DD")
        self.entry_equipment = self._create_input_field(self.entrys_frame, "EQUIPMENT", "Telescope/Lens")
        self.entry_note = self._create_input_field(self.entrys_frame, "NOTES", "Sky conditions,etc...")

        self.label_errors = tk.CTkLabel(self.entrys_frame, text="Greetings!", font=("Segoe UI", 12))
        self.label_errors.pack(pady=(20, 5))

        tk.CTkButton(self.entrys_frame, text='ADD TO DATABASE', font=("Segoe UI", 13, "bold"), 
                     fg_color="#00978A", height=45, width=240, command=self.handle_add).pack(pady=10, padx=30)

        # Right Panel
        self.main_view = tk.CTkFrame(self.main_container, fg_color="#0F1113", corner_radius=0)
        self.main_view.pack(side="right", fill="both", expand=True)

        search_container = tk.CTkFrame(self.main_view, fg_color="transparent")
        search_container.pack(fill="x", padx=20, pady=30)

        tk.CTkLabel(search_container, text="History", font=("Segoe UI", 28, "bold"), text_color="#FFFFFF").pack(side="left")

        self.search_entry = tk.CTkEntry(search_container, placeholder_text="Search...", width=300, height=35)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.scroll_frame = tk.CTkScrollableFrame(self.main_view, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True)

    def _create_input_field(self, parent, label_text, placeholder):
        """Helper method to create labeled entry fields"""
        tk.CTkLabel(parent, text=label_text, font=("Segoe UI", 11, "bold"), text_color="#5C5C5C").pack(anchor="w", padx=30, pady=(10, 0))
        entry = tk.CTkEntry(parent, width=240, height=40, placeholder_text=placeholder)
        entry.pack(padx=30, pady=(5, 10))
        return entry

    def show_main_screen(self):
        """Hides details and displays the list of observations."""
        self.detail_container.pack_forget()
        self.main_container.pack(fill="both", expand=True)
        self.refresh_list()

    def show_detail_screen(self, obs):
        """Displays the full details for a selected observation.
        Clears the previous detail view to manage memory."""
        self.main_container.pack_forget()
        for child in self.detail_container.winfo_children():
            child.destroy()
        
        self.detail_container.pack(fill="both", expand=True)
        
        btn_back = tk.CTkButton(self.detail_container, text="← BACK", command=self.show_main_screen, 
                                fg_color="transparent", text_color="#00978A", font=("Segoe UI", 14, "bold"), 
                                hover_color="#022522", width=100)
        btn_back.pack(anchor="w", padx=20, pady=20)

        btn_delete = tk.CTkButton(self.detail_container, text="DELETE", command=lambda: self.handle_delete(obs.id),
                                 fg_color="transparent", text_color="#FF5252", border_color="#FF5252", border_width=1,
                                 font=("Segoe UI", 12, "bold"), hover_color="#491919", width=80)
        btn_delete.place(relx=0.97, rely=0.03, anchor="ne")

        content = tk.CTkFrame(self.detail_container, fg_color="transparent")
        content.pack(padx=50, pady=20, fill="both", expand=True)

        tk.CTkLabel(content, text=obs.object, font=("Segoe UI", 36, "bold"), text_color="#00978A").pack(anchor="w")
        tk.CTkLabel(content, text=f"Observed on: {obs.date}", font=("Segoe UI", 16), text_color="#5C5C5C").pack(anchor="w", pady=(0, 30))

        self._render_detail_item(content, "EQUIPMENT USED:", obs.equipment)
        self._render_detail_item(content, "DETAILED NOTES:", obs.note, True)

    def _render_detail_item(self, parent, label, value, large=False):
        """Internal helper to render data rows in the Detail view."""
        tk.CTkLabel(parent, text=label, font=("Segoe UI", 12, "bold"), text_color="#00978A").pack(anchor="w", pady=(10, 5))
        if large:
            box = tk.CTkTextbox(parent, fg_color="#1A1C1E", border_width=1, border_color="#012D29", font=("Segoe UI", 14))
            box.pack(fill="both", expand=True, pady=10)
            box.insert("1.0", value)
            box.configure(state="disabled")
        else:
            tk.CTkLabel(parent, text=value, font=("Segoe UI", 18), text_color="#E0E0E0").pack(anchor="w", pady=(0, 10))

    def refresh_list(self, filter_text=""):
        for child in self.scroll_frame.winfo_children():
            child.destroy()
        
        observations = self.service.get_observations(filter_text)
        for obs in observations:
            obs_str = f"{obs.object} | {obs.date}"
            card = tk.CTkFrame(self.scroll_frame, fg_color="#1A1C1E", corner_radius=15, border_width=1, border_color="#012D29", cursor="hand2")
            card.pack(pady=5, padx=20, fill="x")
            
            lbl = tk.CTkLabel(card, text=obs_str, font=("Segoe UI", 14), text_color="#E0E0E0")
            lbl.pack(pady=15, padx=20, anchor="w")
            
            # Clicking on the card opens details
            card.bind("<Button-1>", lambda e, o=obs: self.show_detail_screen(o))
            lbl.bind("<Button-1>", lambda e, o=obs: self.show_detail_screen(o))

    def handle_add(self):
        success, message = self.service.create_observation(
            self.entry_object.get(), 
            self.entry_date.get(), 
            self.entry_equipment.get(), 
            self.entry_note.get()
        )
        color = "#4CAF50" if success else "#FF5252"
        self.label_errors.configure(text=message, text_color=color)
        if success:
            self.refresh_list()

    def handle_delete(self, obs_id):
        """Processes deletion and switches back to main screen."""
        self.service.remove_observation(obs_id)
        self.show_main_screen()

    def on_search(self, event):
        """Event handler for the search bar key release."""
        self.refresh_list(self.search_entry.get())

if __name__ == "__main__":
    app = AstrodatApp()
    app.mainloop()