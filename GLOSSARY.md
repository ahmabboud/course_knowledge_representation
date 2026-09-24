# Course glossary, Knowledge Representation

One plain sentence per term, and the session that first defines it on a
slide. A deck may not use a term before the session listed here. When a
new term is introduced anywhere, add it here in the same change.
Sessions 1 to 3 are complete; later sessions are added as they are rebuilt.

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
| **Open world assumption** | If a fact is missing, it is unknown, not false. Previewed here, used from Session 3. |
| **Closed world assumption** | If a fact is missing, it is false. How SQL databases behave. |

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
| **Endpoint** | A web address that answers SPARQL queries. |
| **Triple store** | A database built to store and query triples. |
| **Fuseki** | The Apache Jena triple store and SPARQL endpoint used in the lab. |
| **Property graph** | A graph model where nodes and edges carry key value properties, used by Neo4j. |
| **Cypher** | Neo4j's query language for property graphs. |

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
