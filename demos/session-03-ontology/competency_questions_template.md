# Competency questions, Session 3

Eight questions, recorded as `ul:answersCQ` annotations on the classes
in `scro-extension.ttl` that answer them (declared for you already in
`workspace/scro-extension-starter.ttl`). A class with no `ul:answersCQ`
has not earned its place, per the lecture's own rule: if you cannot
name the question, delete the class.

Two out of three is not a finding, and the same discipline applies
here: a question needs to be something the organisation actually
asks, not a restatement of a column name.

## Given, four to start from

These are already answered by the worked example in
`scro-extension-starter.ttl` (`ul:LateShipment`) or waiting on your
extension:

1. Which shipments arrived after their committed date last quarter, by carrier?
2. Which plants can legally serve port X, and which of those served it in practice?
3. If supplier S fails, which finished goods lose their only source of a component?
4. Which freight rate band applies to a consignment of weight W on lane L?

## Yours, four more

Draft each one here first, in plain language, before it becomes an
annotation. Ground each in something your Session 1 constraint
inventory actually found, not a hypothetical.

5. _______________________________________________

6. _______________________________________________

7. _______________________________________________

8. _______________________________________________

## Once drafted

For each question:

1. Search SCRO (and GS1 Web Vocabulary for terms it doesn't cover)
   for a class or property that already answers it. Reuse before you
   extend, per the lecture's own ordering, you cannot judge whether
   SCRO covers you until you know what you are asking.
2. If nothing published answers it, add the smallest class or
   property to `scro-extension.ttl` that does, with `skos:definition`
   and `ul:answersCQ` set.
3. Tag it `ul:profile "EL"`, `"DL"` or `"QL"`, whichever your
   axioms actually need. Run the profile check before you commit to
   one, per the lecture's own reminder that domain and range are
   entailment rules, not constraints, so an accidental `owl:allValuesFrom`
   or a cardinality restriction can push you out of EL without you
   noticing.

## What "done" looks like

Eight questions here, eight matching `ul:answersCQ` annotations in
`scro-extension.ttl`, and every class in the file traceable back to
one of these eight. At the Session 3 discussion block you swap
ontologies with a partner and try to answer their questions against
your model, so an annotation that does not actually work as a query
is a finding worth having before then, not after.
