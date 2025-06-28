import argparse
import pickle
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--partition', type=int, required=True)
parser.add_argument('--next', type=str, required=True)
args = parser.parse_args()

# Load model + partition info
with open('/app/tree_model.pkl', 'rb') as f:
    clf = pickle.load(f)

with open('/app/partition_data.json', 'r') as f:
    partition_info = json.load(f)

part_nodes = set(partition_info[str(args.partition)])

@app.route('/infer', methods=['POST'])
def infer():
    data = request.json
    x = data['features']
    node = data['node']

    tree = clf.tree_

    while node in part_nodes:
        if tree.feature[node] == -2:
            pred = int(tree.value[node].argmax())
            return jsonify({'prediction': pred})
        feat = tree.feature[node]
        thresh = tree.threshold[node]
        if x[feat] <= thresh:
            node = tree.children_left[node]
        else:
            node = tree.children_right[node]

    if args.next == 'none':
        return jsonify({'error': 'No next partition, but not classified'})
    
    # Forward to next partition
    ip, port = args.next.split(':')
    r = requests.post(f'http://{ip}:{port}/infer', json={'features': x, 'node': node})
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 + args.partition)

