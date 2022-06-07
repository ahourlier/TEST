from sqlalchemy import text


def get_item(engine, params):
    with engine.connect() as con:

        statement = text(
            f"""
        SELECT {",".join(params.get("columns"))} FROM core.{params.get('table')} WHERE id = :id
        """
        )

        res = con.execute(statement, **params).fetchone()
        if not res:
            return None
        item = {}
        for idx, column in enumerate(params.get("columns")):
            item[column] = res[idx]
        con.close()
    return item


def get_children_ids(engine, params):
    items = []
    with engine.connect() as con:
        statement = text(
            f"""
        SELECT id FROM core.{params.get("children_table")} WHERE {params.get("parent_id_column")} = :id
        """
        )
        res = con.execute(statement, **params).fetchall()
        for item in res:
            items.append(item[0])
        con.close()
    return items
