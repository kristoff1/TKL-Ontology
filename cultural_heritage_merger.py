from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import XSD, RDF, RDFS, OWL

# TKL Ontology
ontology = Graph()
ontology.parse("tkl_ontology-v4.ttl", format="turtle")  # TKL Ontology file

# Load the filtered Turtle data
filtered_data = Graph()
filtered_data.parse("filtered.ttl", format="turtle")

# Define namespaces
MY = Namespace("http://tkl-ontology/")  # TKL Ontology namespace
LA = Namespace("https://linked.art/ns/terms/")

# Prepare the merged graph
merged = ontology  # We'll add to the existing ontology

# Ensure required classes/properties exist
merged.add((MY.Material, RDF.type, RDFS.Class))
merged.add((MY.hasObjectImage, RDF.type, OWL.DatatypeProperty))
merged.add((MY.hasObjectImage, RDFS.domain, MY.Material))
merged.add((MY.hasObjectImage, RDFS.range, XSD.anyURI))

# Process each triple from filtered data
for s, p, o in filtered_data.triples((None, LA.access_point, None)):
    # Add the individual as Material
    merged.add((s, RDF.type, MY.Material))
    print(f"Processing subject: {s}")
    print(f"Processing predicate: {p}")
    print(f"Processing object: {o}")
    
    # Add the access link property
    merged.add((s, MY.hasObjectImage, o))  # Preserves xsd:anyURI type
    print(f"Added access link: {s} -> {o}")


# Save the merged ontology
merged.serialize("merged_ontology.ttl", format="turtle")
print("Successfully merged filtered.ttl into your ontology!")