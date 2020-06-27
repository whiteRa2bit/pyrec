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


def save_frozen(checkpoint_dir, meta_graph_fname, output_graph_fname, output_node_names):
    saver = tf.train.import_meta_graph(meta_graph_fname, clear_devices=True)

    def restore_fn(session):
        checkpoint = tf.train.latest_checkpoint(checkpoint_dir)
        print("checkpoint", checkpoint)
        saver.restore(session, checkpoint)

    config = tf.ConfigProto()
    config.intra_op_parallelism_threads = 16
    config.inter_op_parallelism_threads = 16

    with tf.Session(config=config) as session:
        restore_fn(session)

        # We use a built-in TF helper to export variables to constants
        output_graph_def = tf.graph_util.convert_variables_to_constants(
            session,  # The session is used to retrieve the weights
            tf.get_default_graph().as_graph_def(),  # The graph_def is used to retrieve the nodes
            output_node_names  # The output node names are used to select the usefull nodes
        )

    remove_default_values(output_graph_def)

    # Finally we serialize and dump the output graph to the filesystem
    with tf.gfile.GFile(output_graph_fname, "wb") as stream:
        stream.write(output_graph_def.SerializeToString())
    print("%d ops in the final graph." % len(output_graph_def.node))
