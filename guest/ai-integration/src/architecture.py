"""AWS deployment architecture for the guest lecture, drawn with the `diagrams` library.

Renders four images with the same layout, one per build step of the slide:
  arch-1.png  ingest and extract
  arch-2.png  + reconcile and expert review
  arch-3.png  + search past content and generate text
  arch-4.png  + security and monitoring
Every node, edge label and group exists in every image. Parts of later stages
are drawn transparent, so the layout and the image size never change between
steps. Run from this folder:

    pip install diagrams      # needs Graphviz (`dot`) on the PATH
    python architecture.py
"""
from diagrams import Cluster, Diagram, Edge, Node
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import StepFunctions
from diagrams.aws.management import Cloudwatch
from diagrams.aws.ml import Bedrock, Textract
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.security import IAM, KMS, Cognito
from diagrams.aws.storage import S3

TEXT, MUTED, LINE, NOW, GONE = "#f1f4f2", "#a7b1ac", "#6f7a75", "#8fd14f", "transparent"
FONT = "Helvetica"
OUT = "../img/arch-{}"


def draw(step):
    def node(cls, label, stage):
        lines = label.count("\n") + 1
        attrs = {"fontcolor": TEXT, "fontsize": "36", "fontname": FONT,
                 "imagepos": "tc", "height": str(1.55 + 0.53 * lines)}
        if stage > step:
            attrs.update(style="invis", fontcolor=GONE)
        return cls(label, **attrs)

    def people(label, stage):
        shown = stage <= step
        return Node(label, shape="box", style="rounded,invis" if not shown else "rounded",
                    color="#b794ff" if shown else GONE, fontcolor=TEXT if shown else GONE,
                    penwidth="3", fontsize="36", fontname=FONT, width="2.8", height="1.5",
                    labelloc="c", imagescale="false", fixedsize="false")

    def link(stage, label="", **extra):
        attrs = {"label": label, "fontsize": "31", "fontname": FONT, **extra}
        if stage > step:
            attrs.update(style="invis", fontcolor=GONE)
        elif stage == step:
            attrs.update(color=NOW, fontcolor=NOW, penwidth="5")
        else:
            attrs.update(color=LINE, fontcolor=MUTED, penwidth="3.5")
        return Edge(**attrs)

    def group(label, stage):
        shown = stage <= step
        return {"label": label, "style": "rounded,dashed", "bgcolor": "transparent",
                "pencolor": "#3a4641" if shown else GONE, "fontcolor": MUTED if shown else GONE,
                "fontsize": "30", "fontname": FONT, "margin": "22"}

    graph = {"bgcolor": "transparent", "pad": "0.2", "nodesep": "0.5", "ranksep": "1.9",
             "fontname": FONT, "splines": "spline"}
    with Diagram("", filename=OUT.format(step), show=False, direction="LR",
                 outformat="png", graph_attr=graph):
        teams = people("5 source\nteams", 1)
        experts = people("Product\nexperts", 2)

        with Cluster("AWS cloud", graph_attr=group("AWS cloud", 1)):
            raw = node(S3, "S3\nraw files", 1)
            past = node(S3, "S3\npast seasons", 3)
            flow = node(StepFunctions, "Step Functions\nLambda steps", 1)
            search = node(ElasticsearchService, "Knowledge Base\nsearch", 3)
            read = node(Textract, "Textract\nreads files", 1)
            llm = node(Bedrock, "Bedrock\nClaude LLM", 2)
            db = node(Dynamodb, "DynamoDB\nall records", 1)

            with Cluster("Expert review app", graph_attr=group("Expert review app", 2)):
                save = node(Lambda, "Lambda\nreads, saves", 2)
                api = node(APIGateway, "API Gateway", 2)
                web = node(CloudFront, "CloudFront\nreview page", 2)
                login = node(Cognito, "Cognito\nsign-in", 2)

            export = node(Lambda, "Lambda\nexports Excel", 2)
            excel = node(S3, "S3\nExcel file", 2)

            with Cluster("Across every service", graph_attr=group("Across every service", 4)):
                watch = node(Cloudwatch, "CloudWatch\nlogs, alarms", 4)
                perms = node(IAM, "IAM\npermissions", 4)
                keys = node(KMS, "KMS\nencryption", 4)

        # stage 1: files in, fields out
        teams >> link(1, "upload") >> raw >> link(1, "new file") >> flow
        flow >> link(1) >> read >> link(1, "fields") >> db
        # stage 2: conflicts, suggestions, expert decisions, Excel
        flow >> link(2, "conflicts") >> llm >> link(2, "suggestions") >> db
        db >> link(2, dir="both") >> save >> link(2, dir="both") >> api
        api >> link(2, dir="both") >> web
        api >> Edge(style="invis") >> experts
        web >> link(2, dir="both", constraint="false") >> experts
        save >> Edge(style="invis") >> login
        web >> link(2, constraint="false") >> login
        db >> link(2, "approved") >> export >> link(2) >> excel
        # stage 3: search past content, write stories
        past >> link(3) >> search >> link(3, "similar") >> llm
        # stage 4: no data flow; invisible edges only place the row under the app
        db >> Edge(style="invis") >> watch >> Edge(style="invis") >> perms >> Edge(style="invis") >> keys


if __name__ == "__main__":
    for s in (1, 2, 3, 4):
        draw(s)
