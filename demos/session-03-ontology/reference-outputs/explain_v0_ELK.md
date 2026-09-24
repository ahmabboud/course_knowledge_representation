## [Order for a sole-sourced good](https://ul.edu.lb/kr/scm#OrderForSoleSourcedGood) SubClassOf [Nothing](http://www.w3.org/2002/07/owl#Nothing) ##

  - [Order for a sole-sourced good](https://ul.edu.lb/kr/scm#OrderForSoleSourcedGood) SubClassOf [orders product](https://ul.edu.lb/kr/scm#ordersProduct) some 
([material product](https://spec.industrialontologies.org/ontology/construct/MaterialProduct) and ([depends on product](https://spec.industrialontologies.org/ontology/construct/dependsOnProduct) some [Sole-sourced component](https://ul.edu.lb/kr/scm#SoleSourcedComponent)))
    - [depends on product](https://spec.industrialontologies.org/ontology/construct/dependsOnProduct) SubPropertyOf: [specifically depends on](http://purl.obolibrary.org/obo/BFO_0000195)
      - [specifically depends on](http://purl.obolibrary.org/obo/BFO_0000195) Domain [specifically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000020)
    - [material product](https://spec.industrialontologies.org/ontology/construct/MaterialProduct) EquivalentTo [material entity](http://purl.obolibrary.org/obo/BFO_0000040) and ([has role](https://spec.industrialontologies.org/ontology/construct/hasRole) some [material product role](https://spec.industrialontologies.org/ontology/construct/MaterialProductRole))
      - [has role](https://spec.industrialontologies.org/ontology/construct/hasRole) Domain [independent continuant](http://purl.obolibrary.org/obo/BFO_0000004)
  -  DisjointClasses: [independent continuant](http://purl.obolibrary.org/obo/BFO_0000004), [specifically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000020), [generically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000031)

# Axiom Impact 
## Axioms used 1 times
- [material product](https://spec.industrialontologies.org/ontology/construct/MaterialProduct) EquivalentTo [material entity](http://purl.obolibrary.org/obo/BFO_0000040) and ([has role](https://spec.industrialontologies.org/ontology/construct/hasRole) some [material product role](https://spec.industrialontologies.org/ontology/construct/MaterialProductRole)) [<https://spec.industrialontologies.org/ontology/core/Core/>]
- [Order for a sole-sourced good](https://ul.edu.lb/kr/scm#OrderForSoleSourcedGood) SubClassOf [orders product](https://ul.edu.lb/kr/scm#ordersProduct) some 
([material product](https://spec.industrialontologies.org/ontology/construct/MaterialProduct) and ([depends on product](https://spec.industrialontologies.org/ontology/construct/dependsOnProduct) some [Sole-sourced component](https://ul.edu.lb/kr/scm#SoleSourcedComponent))) [v0]
-  DisjointClasses: [independent continuant](http://purl.obolibrary.org/obo/BFO_0000004), [specifically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000020), [generically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000031) [bfo.owl]
- [depends on product](https://spec.industrialontologies.org/ontology/construct/dependsOnProduct) SubPropertyOf: [specifically depends on](http://purl.obolibrary.org/obo/BFO_0000195) [<https://spec.industrialontologies.org/ontology/supplychain/SupplyChain/>]
- [specifically depends on](http://purl.obolibrary.org/obo/BFO_0000195) Domain [specifically dependent continuant](http://purl.obolibrary.org/obo/BFO_0000020) [bfo.owl]
- [has role](https://spec.industrialontologies.org/ontology/construct/hasRole) Domain [independent continuant](http://purl.obolibrary.org/obo/BFO_0000004) [<https://spec.industrialontologies.org/ontology/core/Core/>]



# Ontologies used: 
- <https://spec.industrialontologies.org/ontology/supplychain/SupplyChain/> (https://spec.industrialontologies.org/ontology/supplychain/SupplyChain/)
- <https://spec.industrialontologies.org/ontology/core/Core/> (https://spec.industrialontologies.org/ontology/core/Core/)
- bfo.owl (http://purl.obolibrary.org/obo/bfo.owl)
- v0 (https://ul.edu.lb/kr/scm/v0)
