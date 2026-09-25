# Course glossary, Knowledge Representation

One plain sentence per term, and the session that first defines it on a
slide. A deck may not use a term before the session listed here. When a
new term is introduced anywhere, add it here in the same change.
Sessions 1 to 6 are covered. The decks turn every term here into a clickable
definition automatically: run `python3 scripts/build-glossary.py` after
editing this file (it writes `assets/glossary.js`).

## Session 1 · The supply chain, the data, and why meaning gets lost

| Term | Plain definition |
|---|---|
| **Supply chain** | The path goods take from raw material to customer: suppliers, plants, warehouses, ports, carriers, customers. |
| **Supplier** | A company that sells materials or components to us. |
| **Plant** | A factory that makes products. |
| **Warehouse** | A building where goods are stored between steps. |
| **Port** | A place where goods enter or leave a country, by sea or air. |
| **Carrier** | A company that transports goods (a shipping line, an airline, a trucking firm). |
| **Customer** | A company or person who buys the finished product. |
| **Order** | A request to buy a quantity of a product, with a date and a destination. |
| **Shipment** | The physical movement of goods for an order, handled by a carrier. |
| **ERP** | Enterprise Resource Planning: the system that holds purchase orders, suppliers and money. |
| **WMS** | Warehouse Management System: the system that records what enters and leaves each warehouse. |
| **PLM** | Product Lifecycle Management: the system that holds product designs and bills of materials. |
| **TMS** | Transportation Management System: the system that plans and tracks shipments and carriers. |
| **CRM** | Customer Relationship Management: the system that holds customers and sales contacts. |
| **Bill of materials** | The list of parts that go into a product, and the parts of those parts. |
| **DataCo** | The course's first dataset: 180,519 order lines from a fictional retailer, one wide table of 53 columns. |
| **Brunel** | The course's second dataset: a logistics problem in 7 linked tables (orders, freight rates, plants, ports...). |
| **Schema** | The declared shape of stored data: tables, columns, types, keys. It says how data looks, not what it means. |
| **Semantic layer** | A machine readable description of what the organisation's data means, sitting above the systems that store it. |
| **Ontology** | A precise, machine readable description of the things in a domain, their types, and how they relate. |
| **Knowledge graph** | Data stored as things connected by named relationships, together with the ontology that says what they mean. |
| **Data profiling** | Measuring a dataset to learn its real shape: counts, missing values, ranges, repeated values, links between tables. |
| **Cardinality (of a column)** | How many different values a column holds. |
| **Null** | An empty cell: the value is missing. |
| **Distribution** | How often each value, or each range of values, appears in a column. |
| **Referential integrity** | Every reference points at something that exists, for example every order's plant code is a real plant. |
| **Business rule** | A rule the business follows that the data should obey, for example "a plant only ships through ports it is linked to". |
| **Constraint inventory** | The course's table of business rules found in the data, each with its evidence and source column. |
| **Order line** | One product inside an order, with its quantity. DataCo stores one order line per row. |
| **Grain** | What one row of a table stands for. The first thing to find out before counting anything. |
| **One to many** | One thing on one side links to several on the other, for example seven plants that share one port. |
| **Clustering (of values)** | Grouping values that look alike, such as two spellings, so a person can decide whether they mean the same thing. |
| **Fingerprint** | A key made from a value by removing case, accents and punctuation and sorting its words. Values with the same key form a cluster. |
| **ydata-profiling** | A Python library that measures every column of a table and writes a report of what looks odd. |
| **OpenRefine** | A free desktop tool for exploring and cleaning messy tables, used here to cluster values. |
| **VMI** | Vendor managed inventory: the supplier looks after stock at the customer's site. Brunel's VmiCustomers table lists such pairs without saying so. |
| **CRF** | A service level code in Brunel's OrderList, used on 854 orders, all with carrier V44_3. The file never defines it. |
| **DTD** | Another Brunel service level code, used on 2,143 orders and in FreightRates. The file never defines it. |
| **DTP** | A third Brunel service level code, used on 6,218 orders. The file never defines it. |
| **HTTP** | Hypertext Transfer Protocol: how browsers and servers, including SPARQL endpoints, exchange requests. |
| **Creative Commons (CC)** | A family of public licences. CC BY 4.0 lets anyone reuse a work if they credit its authors; CC0 gives it to the public domain. |
| **DOI** | Digital Object Identifier: a permanent identifier for a published paper or dataset. |
| **GTFS** | General Transit Feed Specification: the format transit agencies use to publish routes, stops and timetables. |
| **OCDS** | Open Contracting Data Standard: a standard for publishing public procurement data. |
| **EDM** | Europeana Data Model: the vocabulary Europeana uses to describe cultural heritage records. |
| **BIBFRAME** | Bibliographic Framework: the Library of Congress vocabulary for library catalogue records. |
| **USDA** | United States Department of Agriculture, which publishes the FoodData Central database. |
| **Open world assumption** | If a fact is missing, it is unknown, not false. Previewed here, used from Session 3. |
| **Closed world assumption** | If a fact is missing, it is false. How SQL databases behave. |
| **WHERE clause** | The part of a SQL or SPARQL query that says which rows or triples to keep. |
| **JOIN** | SQL's way to combine rows from two tables that share a key. |
| **README** | The text file at the top of a project that explains what it is and how to run it. |
| **JDK** | Java Development Kit: the Java runtime and tools that Protégé, Fuseki and ROBOT need. |
| **ISBN** | International Standard Book Number: a stable identifier printed on every book, an example of an identifier the world already agrees on. |
| **DHL** | A global logistics company; one of the carriers that appear in the course data. |
| **XPO** | A freight logistics company; one of the carriers that appear in the course data. |
| **SQL** | Structured Query Language: the language for asking questions of relational (table) databases. |
| **Relational database** | Data kept in tables of rows and columns, linked by keys. |
| **CSV** | Comma separated values: a plain text table, one row per line. |
| **JSON** | JavaScript Object Notation: a plain text format for nested data, used by most web APIs. |
| **W3C** | World Wide Web Consortium: the body that publishes web standards such as RDF, OWL, SPARQL and SHACL. |
| **ISO** | International Organization for Standardization: publishes international standards, BFO among them. |
| **Docker** | A tool that runs software in sealed containers, so the same setup starts the same way on every machine. |
| **PostgreSQL** | A free, widely used relational database, used for the course's operational data. |

## Session 2 · Data as a graph: RDF and SPARQL

| Term | Plain definition |
|---|---|
| **Graph** | Data drawn as nodes (things) joined by edges (relationships). |
| **Node** | One thing in a graph: an order, a carrier, a port. |
| **Edge** | One named connection between two nodes, for example order 101 "handled by" DHL. |
| **RDF** | Resource Description Framework: the standard for writing a graph as a list of three part statements. |
| **Triple** | One RDF statement: subject, predicate, object. One edge of the graph. |
| **Subject** | The thing a triple is about (the start of the edge). |
| **Predicate** | The relationship in a triple (the label on the edge). |
| **Object** | The value or thing the relationship points to (the end of the edge). |
| **IRI** | Internationalised Resource Identifier: a globally unique name for a thing, written like a web address. |
| **Namespace** | The shared first part of a group of IRIs, for example `https://ul.edu.lb/kr/scm#`. |
| **Prefix** | A short nickname for a namespace, for example `ul:` for `https://ul.edu.lb/kr/scm#`. |
| **Literal** | A plain value in a triple: a number, a date, a piece of text. |
| **Datatype** | The kind of a literal, for example integer or date (`xsd:integer`, `xsd:date`). |
| **Turtle** | A compact, readable text format for writing triples. |
| **N-Triples** | A one triple per line format, simple to process in bulk. |
| **JSON-LD** | Triples written as JSON, used by web APIs. |
| **Blank node** | A node with no global name, used for something that only matters through its links (for example an address). |
| **Named graph** | A set of triples with its own name, used to keep track of where the triples came from. |
| **rdf:type** | The predicate that says what class a thing belongs to. |
| **RDFS** | RDF Schema: the first, simple vocabulary for classes and properties (subclass, domain, range, label). |
| **Entailment** | A fact that follows from the stated facts and rules, even though nobody wrote it down. |
| **Constraint** | A rule that data must obey; breaking it is reported as an error. |
| **SPARQL** | The query language for RDF graphs. |
| **Triple pattern** | A triple with some parts replaced by variables, the basic unit of a SPARQL query. |
| **Variable** | A placeholder in a query, written `?name`, filled by every match. |
| **Aggregation** | Combining many matches into one number: COUNT, SUM, AVG, grouped by something. |
| **Property path** | A query shortcut to follow a relationship one or more times (`+`), in sequence (`/`) or backwards (`^`). |
| **Federation** | One SPARQL query that asks more than one endpoint at once. |
| **SELECT** | The SPARQL (and SQL) query form that returns a table of values for the variables you name. |
| **OPTIONAL** | SPARQL keyword: keep the result even when this part of the pattern has no match, leaving the variable empty. |
| **FILTER** | SPARQL keyword: keep only the results where a condition is true, for example a date after 2024. |
| **CONSTRUCT** | The SPARQL query form that returns new triples instead of a table. |
| **ASK** | The SPARQL query form that answers only yes or no. |
| **DESCRIBE** | The SPARQL query form that returns the triples a store holds about a resource. |
| **GROUP BY** | Query clause that puts results into groups so counts or sums can be computed per group. |
| **TDB2** | Apache Jena's on disk triple store, the storage Fuseki uses. |
| **Endpoint** | A web address that answers SPARQL queries. |
| **Triple store** | A database built to store and query triples. |
| **Fuseki** | The Apache Jena triple store and SPARQL endpoint used in the lab. |
| **Property graph** | A graph model where nodes and edges carry key value properties, used by Neo4j. |
| **Cypher** | Neo4j's query language for property graphs. |
| **Neo4j** | The best known property graph database, queried with Cypher. |
| **EAV** | Entity, attribute, value: storing data as three column rows in a table, a relational imitation of triples. |
| **CTE** | Common table expression: a named sub query in SQL; a recursive CTE is SQL's way to follow links step by step. |
| **URI** | Uniform Resource Identifier: the older, ASCII only form of an IRI. |

## Session 3 · Ontologies, OWL and reasoning

| Term | Plain definition |
|---|---|
| **Class** | A named group of things of the same kind, for example Shipment. |
| **Individual** | One particular thing, a member of one or more classes, for example shipment 4472. |
| **Object property** | A relationship from one thing to another thing, for example "handled by". |
| **Datatype property** | A relationship from a thing to a value, for example "weight in kg". |
| **Annotation property** | A note for humans (label, definition, comment); the reasoner ignores it. |
| **Axiom** | One statement in an ontology, for example "every late shipment is a shipment". |
| **TBox** | The rules part of an ontology: axioms about classes and properties. |
| **ABox** | The data part: axioms about individuals. |
| **Subclass** | A is a subclass of B when every member of A is also a member of B. |
| **owl:Thing** | The class of everything; every class sits below it. |
| **owl:Nothing** | The empty class; a class the reasoner places here can never have a member. |
| **OWL** | Web Ontology Language: the standard for writing ontologies a machine can reason with. |
| **Restriction** | A class defined by a condition on a property, for example "handled by some Sanctioned carrier". |
| **some (existential restriction)** | "At least one link of this kind goes to a member of that class." |
| **only (universal restriction)** | "Every link of this kind, if there is any, goes to a member of that class." |
| **Manchester syntax** | The readable way Protégé writes axioms, with the words some, only, and, or, not, min, max, exactly. |
| **Intersection (and)** | Members of both classes. |
| **Union (or)** | Members of either class. |
| **Complement (not)** | Everything that is not a member of the class. |
| **Disjoint classes** | Classes that can share no member. |
| **Cardinality restriction** | A rule that counts links: exactly 1, at least 2 (min 2), at most 3 (max 3). |
| **Domain** | The class a property's subject is inferred to belong to. In OWL it infers, it never rejects. |
| **Range** | The class a property's object is inferred to belong to. In OWL it infers, it never rejects. |
| **Primitive class** | A class with only SubClassOf axioms: members must meet the conditions, but meeting them does not make you a member. |
| **Defined class** | A class with an EquivalentTo axiom: anything meeting the conditions is a member, and the reasoner puts it there. |
| **Transitive property** | If A relates to B and B to C, then A relates to C, for example "part of". |
| **Functional property** | A property with at most one value per subject. |
| **Inverse property** | The same relationship read backwards, for example "handles" and "handled by". |
| **Punning** | Using the same IRI as both a class and an individual; allowed in OWL 2, easy to misuse. |
| **Reasoner** | A program that works out every fact that follows from an ontology's axioms. |
| **Inference** | A fact the reasoner derived that nobody stated. |
| **Consistency check** | The reasoner's test that the ontology does not contradict itself. |
| **Classification** | The reasoner computing the full class tree, including subclass links nobody stated. |
| **Subsumption** | The "is a subclass of" relationship, stated or inferred. |
| **Realization** | The reasoner computing which classes each individual belongs to. |
| **Satisfiable class** | A class that could have at least one member without contradiction. |
| **Unsatisfiable class** | A class that can never have a member; Protégé shows it in red under owl:Nothing. |
| **Justification (explanation)** | The smallest set of axioms that together cause an inference; Protégé shows it behind the "?" button. |
| **Upper ontology** | A very general ontology of basic categories (things, happenings, qualities) that domain ontologies build on. |
| **BFO** | Basic Formal Ontology, an ISO standard upper ontology. |
| **IOF Core** | The Industrial Ontologies Foundry's middle layer, built on BFO: products, processes, agents. |
| **OBO** | Open Biological and Biomedical Ontologies: a community of ontologies that share rules and build on BFO; BFO's files live at `purl.obolibrary.org/obo/`. |
| **IOF** | Industrial Ontologies Foundry: the OBO idea applied to industry and manufacturing, also built on BFO. |
| **GS1** | The standards body behind barcodes; publishes the GS1 Web Vocabulary for products and supply chain data. |
| **SCRO** | IOF's Supply Chain Reference Ontology, built on IOF Core. The base our ontology extends. |
| **Continuant** | A thing that persists through time, for example a truck or a warehouse. |
| **Occurrent** | Something that happens and unfolds in time, for example a delivery. |
| **Process** | An occurrent with parts that happen one after another, for example loading then shipping. |
| **Independent continuant** | A thing that exists on its own, for example a truck. |
| **Specifically dependent continuant** | Something that exists only in one bearer, for example the truck's colour or its role as a carrier. |
| **Generically dependent continuant** | Information that can be copied between bearers, for example the text of a purchase order. |
| **Material entity** | An independent continuant made of matter, for example a pallet of parts. |
| **Quality** | A dependent characteristic, for example weight or colour. |
| **Role** | A dependent part a thing plays, for example being a supplier. |
| **Alignment** | Linking our classes to classes in another ontology. |
| **owl:sameAs** | States that two IRIs name exactly the same individual; the reasoner merges everything about them. |
| **owl:equivalentClass** | States that two classes have exactly the same members. |
| **Competency question** | A question the ontology must be able to answer; it decides what belongs in the ontology. |
| **Description logic (DL)** | The family of logics OWL is built on: first order logic cut down so that a reasoner is guaranteed to finish. |
| **First order logic (FOL)** | The general logic of "for all" and "there exists"; more expressive than OWL, but no program can always decide it. |
| **PURL** | Persistent URL: a web address that is guaranteed to keep working, used for ontology IRIs such as `purl.obolibrary.org`. |
| **MIT licence (MIT)** | A short, permissive open source licence: anyone may use, change and share the work if they keep the copyright notice. IOF SCRO and IOF Core use it. |
| **ODC PDDL** | Open Data Commons Public Domain Dedication and License: a statement that a dataset is free for anyone to use. |
| **OWL profile** | A restricted part of OWL chosen so reasoning stays fast: EL, QL or RL. |
| **OWL 2 EL** | The profile built for large class trees; fast; no only, no counting, no not. |
| **OWL 2 QL** | The profile built for querying data kept in a relational database. |
| **OWL 2 RL** | The profile built for rule engines. |
| **OWL 2 DL** | Full OWL with all features; reasoning always finishes but can be slow. |
| **Decidable** | A reasoning problem for which a program is guaranteed to finish with the right answer. |
| **ELK** | A very fast reasoner for OWL 2 EL; it ignores axioms outside EL, such as counting. |
| **HermiT** | A complete OWL 2 DL reasoner; slower, but reads every axiom. |
| **Protégé** | The free desktop editor for ontologies used in the lab. |
| **ROBOT** | A command line tool that reasons over an ontology, explains problems, and writes a quality report. |
| **Catalog file** | `catalog-v001.xml`: tells Protégé and ROBOT where to find imported ontologies on disk, so they open offline. |
| **Quality report** | ROBOT's list of findings about an ontology, each marked ERROR, WARN or INFO. |

## Session 4 · Constraints, quality and provenance: SHACL

| Term | Plain definition |
|---|---|
| **SHACL** | Shapes Constraint Language: the W3C standard for checking that graph data obeys rules, with a closed world view. |
| **Shape** | A named set of rules that some nodes of the graph must obey. |
| **Node shape** | A shape about a whole node, for example "every order". |
| **Property shape** | A shape about one property of a node, for example "has exactly one carrier". |
| **Target** | Which nodes a shape checks, for example every member of a class (`sh:targetClass`). |
| **Focus node** | The node being checked when a shape runs. |
| **Validation report** | SHACL's output: conforms or not, and one result per broken rule, with the node and the message. |
| **Severity** | How serious a broken rule is: Violation, Warning or Info. |
| **SHACL-SPARQL** | A SHACL rule written as a SPARQL query, for checks the built in rules cannot express, such as comparing two dates. |
| **pySHACL** | The Python library that runs SHACL validation, used in the lab. |
| **Provenance** | The record of where data came from, who produced it, and how. |
| **PROV-O** | The W3C ontology for writing provenance as triples: an entity (a file, a graph) was generated by an activity (a run), associated with an agent (a person or a program). |
| **EPCIS** | GS1's standard for recording supply chain events: what was seen, where, when and why. |
| **PROV** | The W3C family of provenance standards; PROV-O is its ontology. |
| **XSD** | XML Schema Datatypes: the standard names for value types, such as `xsd:date` and `xsd:integer`. |
| **CI** | Continuous integration: checks that run automatically on every change, and fail the build when a rule breaks. |
| **UML** | Unified Modeling Language: box and line diagrams for software designs. |
| **Triage** | Going through a validation report result by result and deciding, for each, whether the rule or the data is wrong, and what to do about it. |
| **Version IRI** | The name of one release of an ontology (`owl:versionIRI`), next to the ontology IRI that names it across all releases. |
| **Validation gate** | A check every change must pass before it is accepted; here, validation with no Violation. |
| **GitHub Actions** | GitHub's service that runs checks automatically on every push; a failed check marks the commit red. |

## Session 5 · Integrating operational data

| Term | Plain definition |
|---|---|
| **Mapping** | Rules that turn rows of a table or file into triples. |
| **R2RML** | The W3C language for mappings from relational databases to RDF. |
| **RML** | RDF Mapping Language: R2RML extended to CSV, JSON and XML sources. |
| **Materialization** | Converting the data to triples once and storing them in a triple store. |
| **Virtualization** | Leaving the data in its database and translating each SPARQL query into SQL when it is asked. |
| **OBDA** | Ontology based data access: querying a relational database through an ontology, by virtualization. |
| **Ontop** | The open source OBDA engine used in the lab. |
| **Morph-KGC** | The open source tool that runs RML mappings to materialize a knowledge graph. |
| **Knowledge graph construction** | Building a knowledge graph from existing sources through mappings. |
| **Entity resolution** | Deciding which records in different sources describe the same real thing. |
| **Blocking** | Only comparing records that share a cheap key, so entity resolution does not compare every pair. |
| **Precision** | Of the matches we reported, the share that are correct. |
| **Recall** | Of the true matches, the share we found. |
| **F1** | One score that balances precision and recall (their harmonic mean). |
| **XML** | Extensible Markup Language: a tagged text format for structured data. |
| **CLI** | Command line interface: a program used by typing commands in a terminal. |

## Session 6 · Learning over the graph

| Term | Plain definition |
|---|---|
| **Embedding** | A list of numbers that stands for a node or a relation, learned so that similar things get similar numbers. |
| **Knowledge graph embedding** | An embedding of every node and relation, trained so that true triples score higher than false ones. |
| **KGE** | Short for knowledge graph embedding. |
| **TransE** | A knowledge graph embedding model where a relation is a step: head plus relation should land near tail. |
| **PyKEEN** | The Python library for training knowledge graph embeddings, used in the lab. |
| **GNN** | Graph neural network: a model that learns from a node's neighbours by passing messages along edges. |
| **Message passing** | Each node repeatedly collects information from its neighbours and updates its own numbers. |
| **Heterogeneous graph** | A graph with several kinds of nodes and edges, such as orders, carriers and ports. |
| **Node classification** | Predicting a label for a node, for example whether a shipment will be late. |
| **Link prediction** | Predicting an edge that is missing or will appear, for example which carrier will handle an order. |
| **Baseline** | A simple model to beat, such as a table model on the same data; a result only counts if it beats it. |
| **Train/test split** | Keeping some data aside that the model never sees in training, to measure it honestly. |
| **Temporal leakage** | Letting information from the future into training, which makes a model look better than it is. |
| **MRR** | Mean reciprocal rank: for link prediction, how high the true answer ranks on average (1 is perfect). |
| **XGBoost** | A strong, widely used table model, used as the baseline. |
| **DGL** | Deep Graph Library: an older Python library for graph neural networks, no longer actively developed. |
| **PyTorch Geometric** | The Python library for graph neural networks, used in the lab. |
| **SLA** | Service level agreement: a promised delivery time or quality level. |
