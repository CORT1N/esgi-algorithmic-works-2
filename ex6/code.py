"""Sixth exercise."""
from __future__ import annotations

import time
from typing import Any, Callable

from logger import logger


class AVLNode:
    """Node class for AVL Tree."""

    def __init__(self, key: int) -> None:
        """Initialize an AVL Node."""
        self.key: int = key
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height = 1

def get_height(node: AVLNode | None) -> int:
    """Get the height of the node."""
    return node.height if node else 0

def update_height(node: AVLNode | None) -> None:
    """Update the height of the node."""
    if not node:
        return
    node.height = 1 + max(get_height(node.left), get_height(node.right))

def get_balance(node: AVLNode | None) -> int:
    """Get the balance factor of the node."""
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(z: AVLNode) -> AVLNode:
    """Perform a right rotation on the subtree rooted at z."""
    y = z.left
    if y is None:
        return z
    t3 = y.right

    y.right = z
    z.left = t3

    update_height(z)
    update_height(y)

    return y

def left_rotate(z: AVLNode) -> AVLNode:
    """Perform a left rotation on the subtree rooted at z."""
    y = z.right
    if y is None:
        return z
    t2 = y.left

    y.left = z
    z.right = t2

    update_height(z)
    update_height(y)

    return y

def avl_insert(node: AVLNode | None, key: int) -> AVLNode:
    """Insert a key into the AVL tree and balance it."""
    if not node:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    else:
        node.right = avl_insert(node.right, key)

    update_height(node)

    balance = get_balance(node)

    if balance > 1 and node.left is not None and key < node.left.key:
        return right_rotate(node)
    if balance < -1 and node.right is not None and key > node.right.key:
        return left_rotate(node)
    if balance > 1 and node.left is not None and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and node.right is not None and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

def min_value_node(node: AVLNode) -> AVLNode:
    """Get the node with the minimum key in the subtree rooted at node."""
    current = node
    while current.left:
        current = current.left
    return current

def avl_delete(node: AVLNode | None, key: int) -> AVLNode | None:
    """Delete a key from the AVL tree and balance it."""
    if node is None:
        return None

    if key < node.key:
        node.left = avl_delete(node.left, key)
    elif key > node.key:
        node.right = avl_delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        temp = min_value_node(node.right)
        node.key = temp.key
        node.right = avl_delete(node.right, temp.key)

    update_height(node)
    balance = get_balance(node)

    new_root = node

    if balance > 1 and node.left is not None:
        if get_balance(node.left) >= 0:
            new_root = right_rotate(node)
        else:
            node.left = left_rotate(node.left)
            new_root = right_rotate(node)

    elif balance < -1 and node.right is not None:
        if get_balance(node.right) <= 0:
            new_root = left_rotate(node)
        else:
            node.right = right_rotate(node.right)
            new_root = left_rotate(node)

    return new_root

def avl_pre_order(node: AVLNode | None) -> list[int]:
    """Return the pre-order traversal of the AVL tree."""
    if not node:
        return []
    return [node.key, *avl_pre_order(node.left), *avl_pre_order(node.right)]

class BSTNode:
    """Node class for Binary Search Tree (BST)."""

    def __init__(self, key: int) -> None:
        """Initialize a BST Node."""
        self.key: int = key
        self.left: BSTNode | None = None
        self.right: BSTNode | None = None

def bst_insert(node: BSTNode | None, key: int) -> BSTNode:
    """Insert a key into the BST."""
    if not node:
        return BSTNode(key)
    if key < node.key:
        node.left = bst_insert(node.left, key)
    else:
        node.right = bst_insert(node.right, key)
    return node

def bst_min_value_node(node: BSTNode) -> BSTNode:
    """Get the node with the minimum key in the subtree rooted at node."""
    current = node
    while current.left:
        current = current.left
    return current

def bst_delete(node: BSTNode | None, key: int) -> BSTNode | None:
    """Delete a key from the BST."""
    if not node:
        return node

    if key < node.key:
        node.left = bst_delete(node.left, key)
    elif key > node.key:
        node.right = bst_delete(node.right, key)
    else:
        if not node.left:
            return node.right
        if not node.right:
            return node.left

        temp = bst_min_value_node(node.right)
        node.key = temp.key
        node.right = bst_delete(node.right, temp.key)
    return node

def bst_pre_order(node: BSTNode | None) -> list[int]:
    """Return the pre-order traversal of the BST."""
    if not node:
        return []
    return [node.key, *bst_pre_order(node.left), *bst_pre_order(node.right)]

def measure_time(func: Callable[..., Any], *args: object) -> tuple[float, Any]:
    """Measure the execution time of a function."""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def run(config: dict) -> None:
    """Run the AVL and BST tests."""
    data = config.get("insert_sequence", [])
    delete_data = config.get("delete_sequence", [])

    if not data:
        logger.error("Aucune séquence d'insertion fournie dans la config.")
        return

    logger.info(f"Test AVL avec séquence d'insertion : {data}")
    root_avl = None

    def insert_avl_all() -> None:
        nonlocal root_avl
        for key in data:
            root_avl = avl_insert(root_avl, key)

    insert_time_avl, _ = measure_time(insert_avl_all)
    logger.info(f"AVL - Temps d'insertion : {insert_time_avl:.6f} secondes")
    logger.info(f"AVL - Arbre après insertions (pré-ordre) : {avl_pre_order(root_avl)}")

    def delete_avl_all() -> None:
        nonlocal root_avl
        for key in delete_data:
            root_avl = avl_delete(root_avl, key)

    delete_time_avl, _ = measure_time(delete_avl_all)
    logger.info(f"AVL - Temps de suppression : {delete_time_avl:.6f} secondes")
    logger.info(
        f"AVL - Arbre après suppressions (pré-ordre) : {avl_pre_order(root_avl)}",
        )

    logger.info(f"Test BST avec séquence d'insertion : {data}")
    root_bst = None

    def insert_bst_all() -> None:
        nonlocal root_bst
        for key in data:
            root_bst = bst_insert(root_bst, key)

    insert_time_bst, _ = measure_time(insert_bst_all)
    logger.info(f"BST - Temps d'insertion : {insert_time_bst:.6f} secondes")
    logger.info(f"BST - Arbre après insertions (pré-ordre) : {bst_pre_order(root_bst)}")

    def delete_bst_all() -> None:
        nonlocal root_bst
        for key in delete_data:
            root_bst = bst_delete(root_bst, key)

    delete_time_bst, _ = measure_time(delete_bst_all)
    logger.info(f"BST - Temps de suppression : {delete_time_bst:.6f} secondes")
    logger.info(
        f"BST - Arbre après suppressions (pré-ordre) : {bst_pre_order(root_bst)}",
        )

    logger.info("Comparaison des performances (en secondes) :")
    logger.info(f"Insertion AVL : {insert_time_avl:.6f} | BST : {insert_time_bst:.6f}")
    logger.info(
        f"Suppression AVL : {delete_time_avl:.6f} | BST : {delete_time_bst:.6f}",
        )
