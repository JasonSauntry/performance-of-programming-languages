package benchmarkJava;

class HeapNode<T extends Comparable> {
    T value;
    HeapNode<T> left;
    HeapNode<T> right;

    private boolean empty = false;

    HeapNode(T value, HeapNode<T> left, HeapNode<T> right) {
        this.value = value;
        this.left = left;
        this.right = right;
    }

    HeapNode(T value) {
        this(value, null, null);
    }

    public void push(T new_value) {
        if (new_value.compareTo(this.value) >= 0) {
            if (this.left == null) {
                this.left = new HeapNode<T>(new_value);
            } else if (this.right == null) {
                this.right = new HeapNode<T>(new_value);
            } else {
                HeapNode<T> expand_side = this.left.depth() < this.right.depth()
                    ? this.left
                    : this.right;
                expand_side.push(new_value);
            }
        } else {
            T old_value = this.value;
            HeapNode<T> old_left = this.left;
            HeapNode<T> old_right = this.right;

            this.value = new_value;
            this.right = null;
            this.left = new HeapNode(old_value, old_left, old_right);
        }
    }

    public T pop() {
        T ret = this.value;

        if (this.left != null && this.right != null) {
            HeapNode<T> pop_side = this.left.value.compareTo(this.right.value) < 0
                ? this.left
                : this.right;
            this.value = pop_side.pop();
        } else if (this.left != null) {
            this.value = this.left.value;
            this.right = this.left.right;
            this.left = this.left.left;
        } else if (this.right != null) {
            this.value = this.right.value;
            this.left = this.right.left;
            this.right = this.right.right;
        } else {
            this.empty = true;
        }

        if (this.left != null && this.left.empty) {
            this.left = null;
        }
        if (this.right != null && this.right.empty) {
            this.right = null;
        }

        return ret;
    }

    protected int depth() {
        int ldepth = this.left != null ? this.left.depth() + 1 : 1;
        int rdepth = this.right != null ? this.right.depth() + 1 : 1;

        return Math.max(ldepth, rdepth);
    }

    public String toString() {
        String l = this.left != null ? this.left.toString() : "φ";
        String r = this.right != null ? this.right.toString() : "φ";
        return String.format("HeapNode(%s, %s, %s)", this.value.toString(), l, r);
    }

    public boolean isEmpty() {
        return this.empty;
    }
}
