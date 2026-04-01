from pawpal_system import Pet, Task
import pandas as pd

def no_pet_duplicates(pet_to_add: Pet, pets_to_check: list[Pet]) -> bool:
    for pet in pets_to_check:
        if pet_to_add.name == pet.name and pet_to_add.species == pet.species and pet_to_add.age == pet.age:
            return False
    return True

def get_first_pet_duplicate(pet_to_check: Pet, pets_to_check: list[Pet]) -> Pet | None:
    for pet in pets_to_check:
        if pet_to_check.name == pet.name and pet_to_check.species == pet.species and pet_to_check.age == pet.age:
            return pet
    return None

def create_pet_dataframe(pets: list[Pet]) -> pd.DataFrame:
    df = pd.DataFrame(pets)
    df = df.drop(columns=["tasks"])
    return df

def create_task_dataframe(tasks: list[Task]) -> pd.DataFrame:
    df = pd.DataFrame(tasks)
    