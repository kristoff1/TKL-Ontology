from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import RDFS

class OntologyQuery:
    def __init__(self):
        self.graph = Graph()
        self.graph.parse("assigned_merged_ontology.ttl", format='ttl')

        # Namespaces here
        self.ns_hashtag = Namespace("http://tkl-ontology/")
        self.ns = Namespace("http://tkl-ontology/")

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
    
    def get_explanations(self, individual_uri, generic_prop, specific_prop):
        query = f"""
        SELECT ?type ?literal
        WHERE {{
        OPTIONAL {{
            <{individual_uri}> {self.ns[generic_prop].n3()} ?gen .
            ?gen {self.ns.hasLiteralExplanation.n3()} ?literal .
            BIND("generic" AS ?type)
        }}
        OPTIONAL {{
            <{individual_uri}> {self.ns[specific_prop].n3()} ?spec .
            ?spec {self.ns.hasLiteralExplanation.n3()} ?literal .
            BIND("specific" AS ?type)
        }}
        }}
        """
        results = self.graph.query(query)
        explanations = {"generic": [], "specific": []}
        for row in results:
            if row['type'] and row['literal']: # Check if both are not None
                type_str = str(row['type'])
                if type_str == "generic":
                    explanations["generic"].append(str(row['literal']))
                elif type_str == "specific":
                    explanations["specific"].append(str(row['literal']))
        return explanations   
    
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

        # Convert URIs to labels
        direct_labels = [self.extract_label(c) for c in filtered_direct]
        individual_label = self.extract_label(individual_uri)

        return {
            "uri": str(individual_uri),
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