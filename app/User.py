class User:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.step = 0

    def update_step(self):
        self.step += 1
    
    def set_gender(self, gender: str):
        self.gender = gender
    
    def set_age(self, age: str):
        self.age = age