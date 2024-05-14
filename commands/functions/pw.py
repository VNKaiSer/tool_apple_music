from faker import Faker
fake = Faker()
fake.password(digits=3,length=10,special_chars=False, upper_case=True, lower_case=True)