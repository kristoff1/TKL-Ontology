from rdflib import Graph, Namespace, URIRef, RDF

# Load the merged ontology
g = Graph()
g.parse("merged_ontology.ttl", format="ttl")

# Define namespaces
tkl = Namespace("http://tkl-ontology/")

# Add all object properties that you want to assign to all materials 
material_class = tkl.Material
has_rule_property = tkl.hasRule
rule_individual = URIRef("http://tkl-ontology/_test_circulation_rule_1")

# Find all individuals of type Material and add hasRule
for s in g.subjects(RDF.type, material_class):
    g.add((s, has_rule_property, rule_individual))

# Save the modified graph to a new TTL file
g.serialize(destination="assigned_merged_ontology.ttl", format="turtle")
