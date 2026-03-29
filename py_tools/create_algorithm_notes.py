#!/usr/bin/env python3
"""
Create the Algorithm-Notes folder structure and copy .md files from a source directory.

Usage:
  python create_algorithm_notes.py --source "D:\\The_Great_Way\\Algorithm-Notes" --dest "./Algorithm-Notes"

If a source file exists it will be copied; otherwise an empty file will be created.
"""
import os
import shutil
import argparse

TREE = {
    "01-Array-and-String": [
        "Array-Basics.md",
        "String-Processing.md",
        "Prefix-Sum.md",
        "Frequency-Counting.md",
    ],
    "02-HashMap-and-Set": [
        "HashMap-Usage.md",
        "Set-Usage.md",
        "Counting-and-Dedup.md",
    ],
    "03-Two-Pointers-and-Sliding-Window": [
        "Two-Pointers.md",
        "Sliding-Window.md",
        "Subarray-Problems.md",
    ],
    "04-Stack-and-Queue": [
        "Stack-Basics.md",
        "Monotonic-Stack.md",
        "Queue-and-Deque.md",
        "BFS-Queue-Patterns.md",
    ],
    "05-Sorting-and-Greedy": [
        "Sorting.md",
        "Custom-Comparator.md",
        "Greedy-Strategy.md",
        "Interval-Greedy.md",
    ],
    "06-Binary-Search": [
        "Binary-Search-Basics.md",
        "Answer-Space-Binary-Search.md",
        "Lower-Bound-Upper-Bound.md",
    ],
    "07-Graph": [
        "Graph-Basics.md",
        "BFS-and-DFS.md",
        "Connected-Components.md",
        "Union-Find.md",
        "Shortest-Path.md",
        "Topological-Sort.md",
    ],
    "08-Tree": [
        "Binary-Tree.md",
        "Binary-Search-Tree.md",
        "Tree-Traversal.md",
        "LCA.md",
        "Tree-DP.md",
    ],
    "09-Dynamic-Programming": [
        "DP-Basics.md",
        "1D-DP.md",
        "2D-DP.md",
        "Knapsack.md",
        "State-Compression.md",
        "DP-Optimization.md",
    ],
    "10-Heap-and-Priority-Queue": [
        "Heap-Basics.md",
        "Top-K-Problems.md",
        "Merge-Structures.md",
    ],
    "11-Backtracking": [
        "Backtracking-Template.md",
        "Permutations.md",
        "Combinations.md",
        "Pruning.md",
    ],
    "12-Interval-and-Sweep-Line": [
        "Interval-Problems.md",
        "Merge-Intervals.md",
        "Sweep-Line.md",
    ],
    "13-Math-and-Bit-Manipulation": [
        "Math-Tricks.md",
        "Bitwise-Operations.md",
        "Modulo.md",
    ],
    "14-Design-and-Data-Structure": [
        "Design-Patterns.md",
        "LRU-Cache.md",
        "Custom-Data-Structure.md",
    ],
}

def copy_from_sample(sample_path: str, dst_path: str):
    """
    Copy sample markdown file to dst_path,
    and replace the first line title with filename-based title.
    """
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(sample_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 新标题 = 文件名（去掉 .md）
    title = os.path.splitext(os.path.basename(dst_path))[0]
    lines[0] = f"# {title}\n"

    with open(dst_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def build_tree(dest_root: str, sample_path: str):
    os.makedirs(dest_root, exist_ok=True)
    created = []

    for rel_dir, files in TREE.items():
        target_dir = os.path.join(dest_root, rel_dir)
        os.makedirs(target_dir, exist_ok=True)

        for fname in files:
            dst = os.path.join(target_dir, fname)
            copy_from_sample(sample_path, dst)
            created.append(dst)

    return created


def main():
    sample = r"D:\The_Great_Way\Algorithm-Notes\01-Array-and-String\Array-Basics.md"
    dest_root = r"D:\The_Great_Way\Algorithm-Notes3"

    print(f"Sample: {sample}")
    print(f"Destination: {dest_root}")

    created = build_tree(dest_root, sample)

    print("\nSummary:")
    print(f"  Files created from sample: {len(created)}")



if __name__ == "__main__":
    main()
