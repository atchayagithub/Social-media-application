# SPLAY TREE 

class Node:
    def _init_(self,key):
        self.key = key
        self.left = None
        self.right = None

def newNode(key):
    node = Node(key)
    return node

def leftRotate(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y

def rightRotate(x):
    y = x.left
    x.left = y.right
    y.right = x
    return y

def splay(root, key):
    if root is None or root.key == key:
        return root
    if root.key > key:
        if root.left is None:
            return root
        if root.left.key > key:
            root.left.left = splay(root.left.left, key)
            root = rightRotate(root)
        elif root.left.key < key:
            if root.left.right:
                root.left = leftRotate(root.left)
        return (root.left is None) and root or rightRotate(root)
    else:
        if root.right is None:
            return root
        if root.right.key < key:
            root.right.right = splay(root.right.right, key)
            root = leftRotate(root)
        elif root.right.key > key:
            if root.right.left:
                root.right = rightRotate(root.right)
        return (root.right is None) and root or leftRotate(root)

def search(root, key):
    return splay(root, key)

def insert(root, key):
    if root.key == key:
        return root
    if root is None:
        return newNode(key)
    root = splay(root, key)
    if root.key > key:
        new = newNode(key)
        new.right = root
        new.left = root.left
        root.left = None
        return new
    else:
        new = newNode(key)
        new.left = root
        new.right = root.right
        root.right = None
        return new

def delete(root, key):
    if root is None:
        return root
    root = splay(root, key)
    if root.key != key:
        return root
    if root.left is None:
        new_root = root.right
    else:
        new_root = splay(root.left, key)
        new_root.right = root.right
    return new_root

def preOrder(root):
    if root:
        print(root.key, end=' ')
        preOrder(root.left)
        preOrder(root.right)