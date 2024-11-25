with open("config.txt", "r") as config:
    config_path = config.readline().strip()

print(config_path)