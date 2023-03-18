import pickle
# Replace 'file_path.pkl' with the path to your pickle file
file_path = 'players.pickle'

with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Now 'data' contains the content of the pickle file
print(len(data))
print(data[0])

