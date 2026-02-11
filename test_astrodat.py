import unittest
import sqlite3
from Database_code import DatabaseManager
from ObservationService import ObservationService
import time

class TestAstrodatLogic(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(db_name=":memory:")
        self.service = ObservationService(self.db)

    def test_create_observation_success(self):
        success, message = self.service.create_observation(
            "M31 Andromeda", "2026-02-10", "Telescope 8\"", "Clear skies"
        )
        self.assertTrue(success)
        self.assertEqual(message, "Success!")
        
        obs = self.service.get_observations()
        self.assertEqual(len(obs), 1)
        self.assertEqual(obs[0].object, "M31 Andromeda")

    def test_create_observation_missing_fields(self):
        success, message = self.service.create_observation("", "2026-02-10", "", "No info")
        self.assertFalse(success)
        self.assertEqual(message, "Error: Empty Fields")

    def test_duplicate_entry_prevention(self):
        data = ("Jupiter", "2026-02-10", "Binoculars", "Great view")
        self.service.create_observation(*data)
        
        success, message = self.service.create_observation(*data)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Entry Exists")

    def test_search_functionality(self):
        self.service.create_observation("Mars", "2026-01-01", "Scope", "Red planet")
        self.service.create_observation("Saturn", "2026-01-02", "Scope", "Rings")
        
        results = self.service.get_observations("Mars")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].object, "Mars")

    def test_delete_observation(self):
        self.service.create_observation("Moon", "2026-02-10", "Eye", "Full moon")
        obs_id = self.service.get_observations()[0].id
        
        self.service.remove_observation(obs_id)
        results = self.service.get_observations()
        self.assertEqual(len(results), 0)

    def test_stress_and_search_performance(self):
        start_time = time.time()
        for i in range(1000):
            self.db.add_observation((f"Galaxy {i}", "2026-02-10", "Telescope", f"Note number {i}"))
        
        end_time = time.time()
        print(f"\n[Stress Test] Time to insert 1000 records: {end_time - start_time:.4f}s")

        search_start = time.time()
        results = self.service.get_observations("999")
        search_end = time.time()
        
        print(f"[Stress Test] Time to search in 1000 records: {search_end - search_start:.4f}s")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].object, "Galaxy 999")

if __name__ == "__main__":
    unittest.main()