from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import RDFS

class OntologyQuery:
    def __init__(self):
        self.graph = Graph()
        self.graph.parse("tkl_ontology-v4-inferred.ttl", format='ttl')

        # Namespaces here
        self.ns_hashtag = Namespace("http://www.tkl-ontology.org/2#")
        self.ns = Namespace("http://www.tkl-ontology.org/2/")

    def get_materials(self):
        query = f"""
        SELECT ?material
        WHERE {{
            ?material rdf:type {self.ns_hashtag.Material.n3()} .
        }}
        """
        return [str(row[0]) for row in self.graph.query(query)]

    def get_image_path(self, material_uri):
        query = f"""
        SELECT ?image
        WHERE {{
            <{material_uri}> {self.ns.hasObjectImage.n3()} ?image .
        }}
        """
        result = self.graph.query(query)
        for row in result:
            return str(row[0])
        return None

    def get_related_individuals(self, material_uri, property_name):
        query = f"""
        SELECT ?related
        WHERE {{
            <{material_uri}> {self.ns[property_name].n3()} ?related .
        }}
        """
        return [self.format_individual_with_class_hierarchy(row[0]) for row in self.graph.query(query)]
    
    def format_individual_with_class_hierarchy(self, individual_uri):
        # Get direct classes
        class_query = f"""
        SELECT ?class
        WHERE {{
            <{individual_uri}> rdf:type ?class .
            FILTER(?class != owl:NamedIndividual)
        }}
        """
        direct_classes = [row[0] for row in self.graph.query(class_query)]

        # Get parents and grandparents
        parents = set()
        grandparents = set()

        for cls in direct_classes:
            for p in self.graph.objects(cls, RDFS.subClassOf):
                parents.add(p)
                for gp in self.graph.objects(p, RDFS.subClassOf):
                    grandparents.add(gp)

        filtered_direct = set(direct_classes) - parents - grandparents
        filtered_parents = set(direct_classes) - filtered_direct - grandparents
        filtered_grandparents = set(direct_classes) - filtered_parents - filtered_direct

        # Convert URIs to labels
        direct_labels = [self.extract_label(c) for c in filtered_direct]
        parent_labels = [self.extract_label(p) for p in filtered_parents]
        grandparent_labels = [self.extract_label(gp) for gp in filtered_grandparents]
        individual_label = self.extract_label(individual_uri)

        # Format the hierarchy
        lines = [
            ", ".join(grandparent_labels) if grandparent_labels else "—",
            ", ".join(parent_labels) if parent_labels else "—",
            ", ".join(direct_labels ),
            self.extract_label(individual_uri)
        ]

        return {
            "grandparents": grandparent_labels,
            "parents": parent_labels,
            "direct_classes": direct_labels,
            "individual": individual_label,
        }

    def extract_label(self, uri):
        uri_str = str(uri)
        if '#' in uri_str:
            return uri_str.split('#')[-1]
        elif '/' in uri_str:
            return uri_str.split('/')[-1]
        else:
            return uri_str