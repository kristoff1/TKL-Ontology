from rdflib import Graph, Namespace, RDFS, URIRef
import networkx as nx
import matplotlib.pyplot as plt

class ClassHierarchyViewer:
    def __init__(self, ttl_file, namespace_uri):
        self.graph = Graph()
        self.graph.parse(ttl_file, format='ttl')
        self.ns = Namespace(namespace_uri)
        self.nx_graph = nx.DiGraph()

    def extract_label(self, uri):
        uri = str(uri)
        if '#' in uri:
            return uri.split('#')[-1]
        elif '/' in uri:
            return uri.split('/')[-1]
        return uri

    def build_class_hierarchy(self):
        for s, p, o in self.graph.triples((None, RDFS.subClassOf, None)):
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                s_label = self.extract_label(s)
                o_label = self.extract_label(o)
                self.nx_graph.add_node(s_label)
                self.nx_graph.add_node(o_label)
                self.nx_graph.add_edge(o_label, s_label)  # Parent → Child

    def compute_tree_layout(self, root_nodes):
        pos = {}
        layer_spacing = 1.5
        sibling_spacing = 1.0

        def dfs(node, depth, x_offset):
            pos[node] = (x_offset[0], -depth * layer_spacing)
            children = list(self.nx_graph.successors(node))
            for child in children:
                x_offset[0] += sibling_spacing
                dfs(child, depth + 1, x_offset)

        x_offset = [0.0]
        for root in root_nodes:
            dfs(root, 0, x_offset)

        return pos

    def visualize(self):
    # Find roots (classes with no superclass)
        root_nodes = [n for n in self.nx_graph.nodes if self.nx_graph.in_degree(n) == 0]
        pos = self.compute_tree_layout(root_nodes)

        plt.figure(figsize=(12, 10))

        nx.draw_networkx_nodes(self.nx_graph, pos,
                            node_size=50, node_color='gray')

        nx.draw_networkx_edges(self.nx_graph, pos, arrows=True, alpha=0.5)

        plt.title("Class Hierarchy (Top-to-Bottom Tree)", fontsize=14)
        plt.axis('off')
        plt.tight_layout()

        plt.savefig("class_hierarchy.png", format="png", dpi=300)

        plt.show()


if __name__ == "__main__":
    ttl_file = "../ontology/tkl-ontology-extended.ttl"  # Replace with target TTL
    namespace_uri = "http://www.tkl-ontology.org/2#"  # Replace with target namespace

    viewer = ClassHierarchyViewer(ttl_file, namespace_uri)
    viewer.build_class_hierarchy()
    viewer.visualize()