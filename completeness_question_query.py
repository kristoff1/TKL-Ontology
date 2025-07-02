from rdflib import Graph, Namespace
from rdflib.namespace import RDFS

class CompletenessQuery:
    def __init__(self):
        self.graph = Graph()
        self.graph.parse("tkl_ontology-v4.ttl", format='ttl')

        # Namespaces here
        self.ns = Namespace("http://tkl-ontology/")

    def get_label_concept(self, label_individual):

        query = f"""
            SELECT ?label_class
            WHERE {{
                <{label_individual}> rdf:type ?label_class .
            }}
        """
        print(query)
        print([str(row[0]) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]

    def get_rule_sub_object_properties(self, label_class):

        query = f"""
            SELECT ?object_property
            WHERE {{
                ?object_property rdfs:subPropertyOf {self.ns.indicatesRuleOf.n3()} .
                ?object_property rdfs:domain  <{label_class}> .
            }}
            """
        print(query)
        print([str(row[0]) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]

    def get_condition_sub_object_properties(self, label_class):

        query = f"""
            SELECT ?object_property
            WHERE {{
                ?object_property rdfs:subPropertyOf {self.ns.indicatesConditionOf.n3()} .
                ?object_property rdfs:domain <{label_class}> .
            }}
            """
        print(query)
        # print([str(row[0]) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]
    
    def get_purpose_sub_object_properties(self, label_class):
        query = f"""
            SELECT ?object_property
            WHERE {{
                ?object_property rdfs:subPropertyOf {self.ns.indicatesPurposeOf.n3()} .
                ?object_property rdfs:domain <{label_class}> .
            }}
            """
        print(query)
        # print([str(row[0]) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]
    

    def get_range_classes_of_property(self, property_uri):
        query = f"""
            SELECT ?range_class
            WHERE {{
                <{property_uri}> rdfs:range ?range_class .
            }}
        """
        print(query)
        # print([str(row[0]) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]
    
    def get_label_individuals(self):
        #rdfs:subClassOf* <Label> matches any class that is a subclass of Label directly or indirectly (transitive closure).
        query = f"""
            SELECT ?individual
            WHERE {{
                {{
                    ?individual rdf:type {self.ns.Traditional_Knowledge_Label.n3()} .
                }} UNION {{
                    ?individual rdf:type {self.ns.Biocultural_Label.n3()} .
                }}
            }}
        """
        print(query)
        print([str(row.individual) for row in self.graph.query(query)])
        return [str(row[0]) for row in self.graph.query(query)]

    def get_indicated_rules_of_label(self, label_individual):
        result = {}

        # Step 1: Get sub-properties of indicatesRuleOf
        query_subprops = f"""
        SELECT ?subprop WHERE {{
            ?subprop rdfs:subPropertyOf {self.ns.indicatesRuleOf.n3()} .
        }}
        """
        print([row.subprop for row in self.graph.query(query_subprops)]) 
        subprops = [row.subprop for row in self.graph.query(query_subprops)]

        # Step 2: Get all classes of the label_instance
        query_types = f"""
        SELECT ?type WHERE {{
            <{label_individual}> rdf:type ?type .
        }}
        """
        print({row.type for row in self.graph.query(query_types)})
        label_classes = {row.type for row in self.graph.query(query_types)}

        # Step 3: For each sub-property, check if its domain matches any label class
        for subprop in subprops:
            query_domain = f"""
            SELECT ?domain WHERE {{
                <{subprop}> rdfs:domain ?domain .
            }}
            """
            domains = {row.domain for row in self.graph.query(query_domain)}
            has_match = any(cls in domains for cls in label_classes)

            # Step 4: Format key without 'Of' (if present)
            key = subprop.split("/")[-1].replace("Of", "")
            result[key] = has_match
        
        return result

    def get_indicated_conditions_of_label(self, label_individual):
        result = {}

        # Step 1: Get sub-properties of indicatesConditionOf
        query_subprops = f"""
        SELECT ?subprop WHERE {{
            ?subprop rdfs:subPropertyOf {self.ns.indicatesConditionOf.n3()} .
        }}
        """
        print([row.subprop for row in self.graph.query(query_subprops)]) 
        subprops = [row.subprop for row in self.graph.query(query_subprops)]

        # Step 2: Get all classes of the label_instance
        query_types = f"""
        SELECT ?type WHERE {{
            <{label_individual}> rdf:type ?type .
        }}
        """
        print({row.type for row in self.graph.query(query_types)})
        label_classes = {row.type for row in self.graph.query(query_types)}

        # Step 3: For each sub-property, check if its domain matches any label class
        for subprop in subprops:
            query_domain = f"""
            SELECT ?domain WHERE {{
                <{subprop}> rdfs:domain ?domain .
            }}
            """
            domains = {row.domain for row in self.graph.query(query_domain)}
            has_match = any(cls in domains for cls in label_classes)

            # Step 4: Format key without 'Of' (if present)
            key = subprop.split("/")[-1].replace("Of", "")
            result[key] = has_match
        
        return result
    
    def get_indicated_purposes_of_label(self, label_individual):
        result = {}

        # Step 1: Get sub-properties of indicatesPurposeOf
        query_subprops = f"""
        SELECT ?subprop WHERE {{
            ?subprop rdfs:subPropertyOf {self.ns.indicatesPurposeOf.n3()} .
        }}
        """
        print([row.subprop for row in self.graph.query(query_subprops)]) 
        subprops = [row.subprop for row in self.graph.query(query_subprops)]

        # Step 2: Get all classes of the label_instance
        query_types = f"""
        SELECT ?type WHERE {{
            <{label_individual}> rdf:type ?type .
        }}
        """
        print({row.type for row in self.graph.query(query_types)})
        label_classes = {row.type for row in self.graph.query(query_types)}

        # Step 3: For each sub-property, check if its domain matches any label class
        for subprop in subprops:
            query_domain = f"""
            SELECT ?domain WHERE {{
                <{subprop}> rdfs:domain ?domain .
            }}
            """
            domains = {row.domain for row in self.graph.query(query_domain)}
            has_match = any(cls in domains for cls in label_classes)

            # Step 4: Format key without 'Of' (if present)
            key = subprop.split("/")[-1].replace("Of", "")
            result[key] = has_match
        
        return result
    
    def get_indicated_information_of_label(self, label_individual):
        result = {}

        # Step 1: Get sub-properties of indicatesInformationOf
        query_subprops = f"""
        SELECT ?subprop WHERE {{
            ?subprop rdfs:subPropertyOf {self.ns.indicatesInformationOf.n3()} .
        }}
        """
        print([row.subprop for row in self.graph.query(query_subprops)]) 
        subprops = [row.subprop for row in self.graph.query(query_subprops)]

        # Step 2: Get all classes of the label_instance
        query_types = f"""
        SELECT ?type WHERE {{
            <{label_individual}> rdf:type ?type .
        }}
        """
        print({row.type for row in self.graph.query(query_types)})
        label_classes = {row.type for row in self.graph.query(query_types)}

        # Step 3: For each sub-property, check if its domain matches any label class
        for subprop in subprops:
            query_domain = f"""
            SELECT ?domain WHERE {{
                <{subprop}> rdfs:domain ?domain .
            }}
            """
            domains = {row.domain for row in self.graph.query(query_domain)}
            has_match = any(cls in domains for cls in label_classes)

            # Step 4: Format key without 'Of' (if present)
            key = subprop.split("/")[-1].replace("Of", "")
            result[key] = has_match
        
        return result
        

    

    
        