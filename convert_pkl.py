"""
Convert WHAM output pkl to Python 3.7 compatible format
Usage: python convert_pkl.py output/demo/IMG_2234/wham_output.pkl
"""
import sys
import joblib
import pickle

if len(sys.argv) < 2:
    print("Usage: python convert_pkl.py <path_to_wham_output.pkl>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = input_path.replace('.pkl', '_py37.pkl')

# Load with joblib (Python 3.9)
data = joblib.load(input_path)

# Save with pickle protocol 2 (Python 3.7 compatible)
with open(output_path, 'wb') as f:
    pickle.dump(dict(data), f, protocol=2)

print(f"Converted: {input_path} -> {output_path}")
