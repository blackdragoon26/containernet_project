import numpy as np
from sklearn.tree import _tree

class PartitionedDecisionTree:
    def __init__(self, clf, max_depth_per_partition=2):
        self.clf = clf
        self.tree = clf.tree_
        self.max_depth_per_partition = max_depth_per_partition
        self.partitions, self.node_depths = self.partition_tree()

    def partition_tree(self):
        """Partition tree into groups of levels."""
        node_depths = np.zeros(shape=self.tree.node_count, dtype=int)
        stack = [(0, -1)]  # (node_id, parent_depth)

        while stack:
            node_id, parent_depth = stack.pop()
            node_depths[node_id] = parent_depth + 1

            if self.tree.children_left[node_id] != _tree.TREE_LEAF:
                stack.append((self.tree.children_left[node_id], node_depths[node_id]))
                stack.append((self.tree.children_right[node_id], node_depths[node_id]))

        partitions = {}
        for node_id, depth in enumerate(node_depths):
            part_id = depth // self.max_depth_per_partition
            partitions.setdefault(part_id, []).append(node_id)

        return partitions, node_depths

    def evaluate(self, X_sample):
        current_node = 0
        for pid in sorted(self.partitions.keys()):
            print(f"\nProcessing Partition {pid}")
            nodes_in_part = set(self.partitions[pid])
            while current_node in nodes_in_part:
                if self.tree.feature[current_node] == _tree.TREE_UNDEFINED:
                    pred_class = np.argmax(self.tree.value[current_node])
                    print(f"Leaf node {current_node}: Predict class {pred_class}")
                    return pred_class

                feature = self.tree.feature[current_node]
                threshold = self.tree.threshold[current_node]
                value = X_sample[feature]

                if value <= threshold:
                    print(f"Node {current_node}: X[{feature}]={value:.3f} <= {threshold:.3f} → left")
                    current_node = self.tree.children_left[current_node]
                else:
                    print(f"Node {current_node}: X[{feature}]={value:.3f} > {threshold:.3f} → right")
                    current_node = self.tree.children_right[current_node]

            print(f"Partition {pid} done, passing to next partition starting at node {current_node}")

        print("Reached end of partitions without hitting leaf — incomplete tree?")
        return None

