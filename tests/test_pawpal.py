from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    pet = Pet(name="Bella", species="Dog") 
    task = Task(description="Morning Walk", due_time="08:00 AM")
    assert task.is_completed == False
    
    task.mark_complete(pet) 
    
    assert task.is_completed == True

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Bella", species="Dog")
    task = Task(description="Afternoon Feeding", due_time="02:00 PM")
    
    assert len(pet.tasks) == 0
    
    pet.add_task(task)
    
    assert len(pet.tasks) == 1