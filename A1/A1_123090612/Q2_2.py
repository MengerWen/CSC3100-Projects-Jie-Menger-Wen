import sys
import threading

def main():
    sys.setrecursionlimit(1 << 25)
    
    n, q = map(int, sys.stdin.readline().split())
    permutation = list(map(int, sys.stdin.readline().split()))
    l_list = list(map(int, sys.stdin.readline().split()))
    r_list = list(map(int, sys.stdin.readline().split()))

    position = {}
    for idx, val in enumerate(permutation):
        position[val] = idx

    parent = {}
    min_pos = {}
    max_pos = {}
    size = {}

    # Initialize Union-Find structures
    for val in permutation:
        parent[val] = val
        pos = position[val]
        min_pos[val] = pos
        max_pos[val] = pos
        size[val] = 1

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)

        if root_x != root_y:
            # Union by size (merge smaller tree into larger tree)
            if size[root_x] > size[root_y]:
                root_x, root_y = root_y, root_x  # Ensure root_x is smaller

            # Perform the union
            parent[root_x] = root_y
            min_pos[root_y] = min(min_pos[root_x], min_pos[root_y])
            max_pos[root_y] = max(max_pos[root_x], max_pos[root_y])
            size[root_y] = size[root_x] + size[root_y]

    valid = True

    # Process operations in reverse
    for i in range(q - 1, -1, -1):
        x = l_list[i]
        y = r_list[i]

        if x not in parent or y not in parent:
            valid = False
            break

        root_x = find(x)
        root_y = find(y)

        if root_x != root_y:
            new_min = min(min_pos[root_x], min_pos[root_y])
            new_max = max(max_pos[root_x], max_pos[root_y])
            total_size = new_max - new_min + 1
            total_elements = size[root_x] + size[root_y]
            if total_size != total_elements:
                valid = False
                break
            else:
                union(x, y)

    print(1 if valid else 0)

if __name__ == '__main__':
    threading.Thread(target=main).start()
