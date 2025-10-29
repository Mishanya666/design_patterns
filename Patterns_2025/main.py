import connexion
from flask import Response
from Src.start_service import start_service
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity


app = connexion.FlaskApp(__name__)
start = start_service()
start.start()
factory = factory_entities()
repo = start.data


@app.route("/api/accessibility", methods=['GET'])
def accessibility():
    return "SUCCESS"

@app.route("/api/nomenclatures/<format>", methods=['GET'])
def get_nomenclatures(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.nomenclature_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/ranges/<format>", methods=['GET'])
def get_ranges(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.range_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/groups/<format>", methods=['GET'])
def get_groups(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.group_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/receipts/<format>", methods=['GET'])
def get_receipts(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.receipt_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)