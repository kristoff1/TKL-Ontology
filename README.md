# Project Title

Brief description of your project: what it does, its purpose, and the technologies used (e.g., Python, RDF/OWL, Turtle).

## 📦 Requirements
### Python Version
3.13.3
### List of dependencies for this project
<ul>
<li>rdflib</li>
<li>networkx</li>
<li>matplotlib</li>
<li>PyQt6</li>
<li>requests</li>
</ul>

### To Install
pip install -r requirements.txt

## 🧠 Ontology Files (.ttl)
#### tkl_ontology-v4.ttl
<p>The original TKL Ontology file.</p>
<p>Results Inference are temporary and can be saved to another files.</p>

#### tkl-ontology-extended.ttl
<p>An ontology file with examples of inferred axioms. This is the file used for competency questions visualization, containing inferrence results.</p>

#### filtered.ttl
<p>1000 triples that have been extracted from NMVW image-object https://data.colonialcollections.nl/nmvw/collection-archives.</p>

#### assigned_merged_ontology.ttl
<p>An example of integrated NMVW triples with TKL Ontology with assigned properties produced by auto_assignment.py.</p>

## 🐍 Python Scripts
### Label Completeness Test Scripts
#### completeness_question_viewer.py
<p>Visualize the completeness of the labels</p>

#### completeness_question_query.py
<p>SPARQL Queries to test label completeness</p>

### Material Completeness Test Scripts
#### competency_question_viewer.py
<p>Visualize the completeness of the materials</p>

#### competency_question_query.py
<p>SPARQL Queries to test use case completeness</p>

### NMVW Integration Scripts
#### merged_linked_open_data_competency_question_viewer.py

<p>Visualize the image objects from the NMVW with TKL Ontology</p>

#### merged_competency_question_query.py
<p>Visualize the competency question query</p>

#### cultural_heritage_merger.py
<p>Integrate filtered NMVW triples with hasObjectImage property from TKL ontology.
This script gets all images with https://linked.art/ns/terms/ predicate and integrate them with TKL Ontology.
The result of this merge is merged_ontology.ttl in the same folder.<p>

#### auto_assignment.py
<p>This script auto-assigns any chosen object properties of TKL Ontology to the merged_ontology_ttl.
Add any object property to assign to all materials.
The result is going to be assigned_merged_ontology.ttl in the same folder.<p>
