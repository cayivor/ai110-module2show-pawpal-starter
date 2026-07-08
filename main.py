from pawpal_system import Scheduler, Owner, Pet, Task

def main():
    # 1. Initialize the system brain (Scheduler)
    scheduler = Scheduler()

    # 2. Create an Owner
    owner = Owner(name="Chelsea")
    scheduler.register_owner(owner)

    # 3. Create two Pets
    pet1 = Pet(name="Bella", species="Dog")
    pet2 = Pet(name="Oliver", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # 4. Add three Tasks across the pets
    task1 = Task(description="Morning Walk", due_time="08:00 AM", frequency="Daily")
    task2 = Task(description="Afternoon Feeding", due_time="02:00 PM", frequency="Daily")
    task3 = Task(description="Give Medication", due_time="07:00 PM", frequency="Once")

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    # 5. Fetch and print a clean, readable schedule summary
    print("=" * 45)
    print(f"🐾 TODAY'S PAWPAL+ SCHEDULE FOR {owner.name.upper()} 🐾")
    print("=" * 45)
    
    schedule = scheduler.get_daily_schedule(owner)
    
    if not schedule:
        print("🎉 No pending tasks for today!")
    else:
        for item in schedule:
            pet_name = item["pet_name"]
            task = item["task"]
            print(f"⏰ [{task.due_time}] - {pet_name}: {task.description} ({task.frequency})")
            
    print("=" * 45)

if __name__ == "__main__":
    main()