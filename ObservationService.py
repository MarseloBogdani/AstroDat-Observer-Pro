class ObservationService:
    
    def __init__(self, db_manager):
        self.db = db_manager

    def create_observation(self, obj, date, equip, note):
        if not all([obj, date, equip]):
            return False, "Error: Empty Fields"
        
        data = (obj, date, equip, note)
        success = self.db.add_observation(data)
        
        if success:
            return True, "Success!"
        return False, "Error: Entry Exists"

    def get_observations(self, search_term=""):
        if not search_term:
            return self.db.get_all_observations()
        return self.db.search_observations(search_term)

    def remove_observation(self, obs_id):
        self.db.delete_observation(obs_id)