from pawpal_system import Scheduler, Owner, Pet, Task

def main():
    scheduler = Scheduler()
    owner = Owner(name="Test Owner")
    scheduler.register_owner(owner)

    pet1 = Pet(name="Bella", species="Dog")
    pet2 = Pet(name="Mochi", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # purposely scheduling two tasks at the exact same time!
    task1 = Task(description="Morning Walk", due_time="08:00 AM")
    task2 = Task(description="Give Medicine", due_time="08:00 AM")
    task3 = Task(description="Midday Play", due_time="12:00 PM")
    
    pet1.add_task(task1)
    pet2.add_task(task2)
    pet1.add_task(task3)

    print("\n--- SORTED DAILY SCHEDULE ---")
    raw_schedule = scheduler.get_daily_schedule(owner)
    sorted_schedule = scheduler.sort_by_time(raw_schedule)
    
    for item in sorted_schedule:
        print(f"[{item['task'].due_time}] {item['pet_name']}: {item['task'].description}")

    print("\n--- RUNNING CONFLICT CHECK ---")
    warnings = scheduler.check_for_conflicts(sorted_schedule)
    
    if warnings:
        for w in warnings:
            print(w)
    else:
        print("✅ No conflicts detected!")

if __name__ == "__main__":
    main()