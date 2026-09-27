import mysql.connector

def generate_dot():
    conn = mysql.connector.connect(
        host='localhost',
        database='bacchus_winery',
        user='root',
        password=''
    )
    cursor = conn.cursor()

    dot_content = "digraph BacchusERD {\n"
    dot_content += "  graph [rankdir=LR, nodesep=0.5, ranksep=0.8];\n"
    dot_content += "  node [shape=plaintext, fontname=\"Helvetica\", fontsize=10];\n"
    dot_content += "  edge [fontname=\"Helvetica\", fontsize=8, color=\"#555555\"];\n\n"

    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]

    relationships = []

    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()

        dot_content += f'  {table} [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#FFFFFF">\n'
        dot_content += f'    <TR><TD BGCOLOR="#1a5276" ALIGN="CENTER"><FONT COLOR="#FFFFFF"><B>{table.upper()}</B></FONT></TD></TR>\n'

        for col in columns:
            field, col_type, null, key, default, extra = col
            is_pk = " (PK)" if key == "PRI" else ""
            is_fk = " (FK)" if key == "MUL" else ""
            field_label = f"{field}{is_pk}{is_fk}"
            
            if key == "PRI":
                dot_content += f'    <TR><TD ALIGN="LEFT"><U><B>{field_label}</B></U> <FONT COLOR="#777777">: {col_type}</FONT></TD></TR>\n'
            elif key == "MUL":
                dot_content += f'    <TR><TD ALIGN="LEFT"><I>{field_label}</I> <FONT COLOR="#777777">: {col_type}</FONT></TD></TR>\n'
            else:
                dot_content += f'    <TR><TD ALIGN="LEFT">{field_label} <FONT COLOR="#777777">: {col_type}</FONT></TD></TR>\n'

        dot_content += "  </TABLE>>];\n\n"

        cursor.execute(f"""
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'bacchus_winery' 
              AND TABLE_NAME = '{table}' 
              AND REFERENCED_TABLE_NAME IS NOT NULL;
        """)
        fks = cursor.fetchall()
        for fk_col, ref_table in fks:
            relationships.append(f'  {ref_table} -> {table} [label="{fk_col}", dir=back, arrowtail=crow, arrowhead=none];')

    dot_content += "\n".join(relationships)
    dot_content += "\n}\n"

    with open("schema.dot", "w") as f:
        f.write(dot_content)

    print("[+] 'schema.dot' generated successfully!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    generate_dot()
