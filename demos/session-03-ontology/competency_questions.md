# Competency questions, Session 3 reference ontology

A reference, not a worksheet. All eight are already answered in
`scro-extension-reference.ttl`, each recorded as a `ul:answersCQ`
annotation on the class listed below. Nothing here to fill in, use
this to find your place in the file quickly during the walkthrough, or
to check your own reading of the reasoner output and the ROBOT report
against it.

| # | Competency question | Answered by |
|---|---|---|
| 1 | Which shipments arrived after their committed date last quarter, by carrier? | `ul:LateShipment` |
| 2 | Which plants can legally serve port X, and which of those served it in practice? | `ul:PlantPortAuthorization` |
| 3 | If supplier S fails, which finished goods lose their only source of a component? | `ul:SoleSourcedComponent` |
| 4 | Which freight rate band applies to a consignment of weight W on lane L? | `ul:FreightRateBand` |
| 5 | Which sanctioned carriers were used on shipments in the last quarter? | `ul:SanctionedCarrier` |
| 6 | Which in-flight shipments are at risk of missing their committed date? | `ul:AtRiskShipment` |
| 7 | Which purchase orders are for a finished good that depends on a sole-sourced component? | `ul:OrderForSoleSourcedGood` |
| 8 | Which carriers operate on more than one shipping route? | `ul:MultiRouteCarrier` |

## Four classes in the file have no competency question, on purpose

Run the "classes with no competency question" query from the lecture's
lab brief slide against `scro-extension-reference.ttl` (or just read
`report.tsv` after `robot_report.py` runs) and four classes come back:

- **`ul:CancelledShipment`**, deliberately. This is the exercise: per
  the lecture's own rule, a class with no competency question has not
  earned its place. Discuss live whether to keep it or delete it, do
  not just note that the query found it and move on.
- **`ul:CommittedDate`**, **`ul:Plant`**, and **`ul:Port`**, for a
  different reason: each is a support class, referenced only inside
  another class's own restriction, not a business entity a competency
  question would name on its own. A support class earns its place by
  being used inside a class that answers a question, not by answering
  one itself. Expected, not a finding.

## Where you actually practice writing these

Not here. Drafting real competency questions, from a real constraint
inventory, for classes that do not exist yet, is a genuine skill this
course teaches, and you exercise it on your own team's chosen topic
(see `PROJECT-REDESIGN.md`), starting right after Session 1, not on
this session's shared reference file. The habit to take from today:
before you add a class to your own ontology, name the question it
answers first, out loud, then check whether SCRO, GS1, or your own
topic's published vocabulary already answers it before you write
anything new.
