import tensorflow as tf


def remove_default_values(graph_def):
    def strip_node_default_valued_attrs(node_def, op_defs):
        from tensorflow.python.framework import meta_graph
        op_def = op_defs[node_def.op]
        attrs_to_strip = set()
        for attr_name, attr_value in node_def.attr.items():
            if meta_graph._is_default_attr_value(op_def, attr_name, attr_value):
                attrs_to_strip.add(attr_name)
        for attr in attrs_to_strip:
            del node_def.attr[attr]

    if list(map(int, tf.VERSION.split('.'))) >= [1, 8]:
        with tf.Graph().as_default() as graph:
            tf.graph_util.import_graph_def(graph_def)
        op_defs = {o.op_def.name: o.op_def for o in graph.get_operations()}
        for node_def in graph_def.node:
            strip_node_default_valued_attrs(node_def, op_defs)
