import uuid


# codes = list(set(codes))
for _ in range(1000):
    codes = [str(uuid.uuid4()) for _ in range(1000)]
    if any(codes.count(x) > 1 for x in codes):
        print("duplicate found")
        break
