"""Sixth exercise."""
import time

from logger import logger


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    return node.height if node else 0

def update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(z):
    y = z.left
    T3 = y.right

    y.right = z
    z.left = T3

    update_height(z)
    update_height(y)

    return y

def left_rotate(z):
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    update_height(z)
    update_height(y)

    return y

def avl_insert(node, key):
    if not node:
        return AVLNode(key)
    elif key < node.key:
        node.left = avl_insert(node.left, key)
    else:
        node.right = avl_insert(node.right, key)

    update_height(node)

    balance = get_balance(node)

    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

def min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current

def avl_delete(node, key):
    if not node:
        return node

    if key < node.key:
        node.left = avl_delete(node.left, key)
    elif key > node.key:
        node.right = avl_delete(node.right, key)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left

        temp = min_value_node(node.right)
        node.key = temp.key
        node.right = avl_delete(node.right, temp.key)

    update_height(node)
    balance = get_balance(node)

    if balance > 1 and get_balance(node.left) >= 0:
        return right_rotate(node)
    if balance > 1 and get_balance(node.left) < 0:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and get_balance(node.right) <= 0:
        return left_rotate(node)
    if balance < -1 and get_balance(node.right) > 0:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

def avl_pre_order(node):
    if not node:
        return []
    return [node.key] + avl_pre_order(node.left) + avl_pre_order(node.right)


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def bst_insert(node, key):
    if not node:
        return BSTNode(key)
    if key < node.key:
        node.left = bst_insert(node.left, key)
    else:
        node.right = bst_insert(node.right, key)
    return node

def bst_min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current

def bst_delete(node, key):
    if not node:
        return node

    if key < node.key:
        node.left = bst_delete(node.left, key)
    elif key > node.key:
        node.right = bst_delete(node.right, key)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left

        temp = bst_min_value_node(node.right)
        node.key = temp.key
        node.right = bst_delete(node.right, temp.key)
    return node

def bst_pre_order(node):
    if not node:
        return []
    return [node.key] + bst_pre_order(node.left) + bst_pre_order(node.right)


def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def run(config):
    data = config.get("insert_sequence", [])
    delete_data = config.get("delete_sequence", [])

    if not data:
        logger.error("Aucune séquence d'insertion fournie dans la config.")
        return

    # === AVL ===
    logger.info(f"Test AVL avec séquence d'insertion : {data}")
    root_avl = None

    def insert_avl_all():
        nonlocal root_avl
        for key in data:
            root_avl = avl_insert(root_avl, key)

    insert_time_avl, _ = measure_time(insert_avl_all)
    logger.info(f"AVL - Temps d'insertion : {insert_time_avl:.6f} secondes")
    logger.info(f"AVL - Arbre après insertions (pré-ordre) : {avl_pre_order(root_avl)}")

    def delete_avl_all():
        nonlocal root_avl
        for key in delete_data:
            root_avl = avl_delete(root_avl, key)

    delete_time_avl, _ = measure_time(delete_avl_all)
    logger.info(f"AVL - Temps de suppression : {delete_time_avl:.6f} secondes")
    logger.info(f"AVL - Arbre après suppressions (pré-ordre) : {avl_pre_order(root_avl)}")

    logger.info(f"Test BST avec séquence d'insertion : {data}")
    root_bst = None

    def insert_bst_all():
        nonlocal root_bst
        for key in data:
            root_bst = bst_insert(root_bst, key)

    insert_time_bst, _ = measure_time(insert_bst_all)
    logger.info(f"BST - Temps d'insertion : {insert_time_bst:.6f} secondes")
    logger.info(f"BST - Arbre après insertions (pré-ordre) : {bst_pre_order(root_bst)}")

    def delete_bst_all():
        nonlocal root_bst
        for key in delete_data:
            root_bst = bst_delete(root_bst, key)

    delete_time_bst, _ = measure_time(delete_bst_all)
    logger.info(f"BST - Temps de suppression : {delete_time_bst:.6f} secondes")
    logger.info(f"BST - Arbre après suppressions (pré-ordre) : {bst_pre_order(root_bst)}")

    logger.info("Comparaison des performances (en secondes) :")
    logger.info(f"Insertion AVL : {insert_time_avl:.6f} | BST : {insert_time_bst:.6f}")
    logger.info(f"Suppression AVL : {delete_time_avl:.6f} | BST : {delete_time_bst:.6f}")