import datetime
import math

class SmartParkingSystem:
    def __init__(self, total_slots):
        # Design slot dictionary with vehicle number and entry time
        self.slots = {i: None for i in range(1, total_slots + 1)}
        self.hourly_rate = 50  # Base rate
        self.daily_revenue = [] # Maintain a daily revenue list

    def allocate_slot(self, vehicle_number, vehicle_type="Car"):
        """Find the next free slot and assign vehicles automatically."""
        for slot, data in self.slots.items():
            if data is None:
                # Record entry time using datetime.datetime.now()
                entry_time = datetime.datetime.now()
                self.slots[slot] = {
                    'vehicle_no': vehicle_number,
                    'type': vehicle_type,
                    'entry_time': entry_time
                }
                print(f"Slot {slot} allocated to {vehicle_number} at {entry_time.strftime('%H:%M:%S')}")
                return slot
        print("Error: No available slots!")
        return None

    def calculate_billing(self, entry_time):
        """Calculate parking charges based on total time parked."""
        exit_time = datetime.datetime.now()
        duration = exit_time - entry_time
        
        # Convert duration to hours (rounding up)
        hours_parked = math.ceil(duration.total_seconds() / 3600)
        
        # Premium Add-on: Variable pricing (first 2 hours fixed, then per-hour)
        if hours_parked <= 2:
            fee = 40  # Fixed rate for first 2 hours
        else:
            fee = 40 + (hours_parked - 2) * self.hourly_rate
            
        return fee, hours_parked

    def process_exit(self, slot_id):
        """Process exit, compute fees, and update availability."""
        if slot_id not in self.slots or self.slots[slot_id] is None:
            print(f"Invalid Request: Slot {slot_id} is already empty or does not exist.")
            return

        vehicle_data = self.slots[slot_id]
        fee, hours = self.calculate_billing(vehicle_data['entry_time'])
        
        # Add revenue to tracker
        self.daily_revenue.append(fee)
        
        print(f"Vehicle {vehicle_data['vehicle_no']} exiting slot {slot_id}.")
        print(f"Total Time: {hours} hour(s) | Total Fee: ${fee}")
        
        # Freeing up the slot
        self.slots[slot_id] = None

    def show_revenue_report(self):
        """Track revenue, total vehicles, and parking usage."""
        total_earned = sum(self.daily_revenue)
        total_vehicles = len(self.daily_revenue)
        print("\n--- DAILY REVENUE REPORT ---")
        print(f"Total Vehicles Processed: {total_vehicles}")
        print(f"Total Revenue Collected: ${total_earned}")
        print("----------------------------\n")

# --- Test the code ---
if __name__ == "__main__":
    parking_lot = SmartParkingSystem(total_slots=10)
    parking_lot.allocate_slot("ABC-1234", "Car")
    parking_lot.process_exit(1)
    parking_lot.show_revenue_report()