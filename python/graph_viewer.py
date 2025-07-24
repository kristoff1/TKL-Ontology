from rdflib import Graph, Namespace, RDF, URIRef, BNode, Literal
import networkx as nx
import matplotlib.pyplot as plt

class OntologyGraphViewer:

    def __init__(self, ttl_file, namespace_uri):
        self.graph = Graph()
        self.graph.parse(ttl_file, format='ttl')
        self.ns = Namespace(namespace_uri)
        self.nx_graph = nx.DiGraph()
        self.material_nodes = set()

    def get_material_individuals(self):
        query = f"""
        SELECT ?m WHERE {{
            ?m rdf:type {self.ns.Material.n3()} .
        }}
        """
        materials = [row[0] for row in self.graph.query(query)]
        self.material_nodes = {self.extract_label(m) for m in materials}
        return materials
    
    def _traverse_and_add(self, node, depth, visited):
        if depth < 0 or node in visited:
            return
        visited.add(node)

        for s, p, o in self.graph.triples((node, None, None)):
            if isinstance(o, (URIRef, BNode)):
                s_label = self.extract_label(s)
                p_label = self.extract_label(p)
                o_label = self.extract_label(o)

                self.nx_graph.add_node(s_label)
                self.nx_graph.add_node(o_label)
                self.nx_graph.add_edge(s_label, o_label, label=p_label)

                self._traverse_and_add(o, depth - 1, visited)

    def build_graph(self, depth_limit=3):
        materials = self.get_material_individuals()

        for material in materials:
            visited = set()
            self._traverse_and_add(material, depth_limit, visited)

    

    def extract_label(self, uri):
        uri = str(uri)
        if '#' in uri:
            return uri.split('#')[-1]
        elif '/' in uri:
            return uri.split('/')[-1]
        return uri

    def visualize(self):
        # Create initial spring layout
        pos = nx.spring_layout(self.nx_graph, k=0.7, seed=42)

        # Separate Material and non-Material nodes
        material_nodes = list(self.material_nodes)
        other_nodes = [n for n in self.nx_graph.nodes if n not in self.material_nodes]

        # Re-position Material nodes to the center
        for i, m in enumerate(material_nodes):
            angle = i * (360 / len(material_nodes))  # Spread in a small circle
            pos[m] = [0.1 * i, 0]  # Keep close to center (adjust x spacing)

        plt.figure(figsize=(20, 8))

        # Draw Material nodes in red
        nx.draw_networkx_nodes(self.nx_graph, pos,
                            nodelist=material_nodes,
                            node_color='red', node_size=1000)

        # Draw other nodes in light blue
        nx.draw_networkx_nodes(self.nx_graph, pos,
                            nodelist=other_nodes,
                            node_color='lightblue', node_size=800)

        # Draw edges and labels
        nx.draw_networkx_edges(self.nx_graph, pos, arrows=True)
        nx.draw_networkx_labels(self.nx_graph, pos, font_size=10)

        edge_labels = nx.get_edge_attributes(self.nx_graph, 'label')
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Ontology Graph (Material in Red)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    ontology_file = "../ontology/tkl-ontology-extended.ttl"  # Replace with your .ttl file
    namespace_uri = "http://www.tkl-ontology.org/2#"  # Replace with your actual namespace

    viewer = OntologyGraphViewer(ontology_file, namespace_uri)
    viewer.build_graph(depth_limit=1)
    viewer.visualize()
