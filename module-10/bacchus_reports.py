"""
Title: Bacchus Winery Management Reports
Assignment: CSD-310 Module 10.1 Milestone #3
Group: Group C
Authors: Neosha Allen, Prince Hubbard, and Nicholas Zankl
Date: September 25, 2026

This program connects to the Bacchus Winery MySQL/MariaDB database and
produces three reports used to support purchasing, distribution, and labor
decisions.
"""

import os
import mysql.connector
from mysql.connector import Error


REPORTS = [
    (
        "REPORT 1 - SUPPLIER DELIVERY PERFORMANCE",
        """
        SELECT
            s.supplier_name AS Supplier,
            COUNT(so.order_id) AS Total_Orders,
            SUM(CASE WHEN so.actual_delivery_date IS NOT NULL THEN 1 ELSE 0 END)
                AS Completed,
            SUM(CASE
                    WHEN so.actual_delivery_date <= so.expected_delivery_date THEN 1
                    ELSE 0
                END) AS On_Time,
            SUM(CASE WHEN so.actual_delivery_date IS NULL THEN 1 ELSE 0 END)
                AS Pending,
            ROUND(AVG(CASE
                WHEN so.actual_delivery_date IS NOT NULL
                THEN DATEDIFF(so.actual_delivery_date, so.expected_delivery_date)
            END), 1) AS Avg_Days_Late
        FROM suppliers s
        LEFT JOIN supply_orders so ON s.supplier_id = so.supplier_id
        GROUP BY s.supplier_id, s.supplier_name
        ORDER BY Avg_Days_Late, s.supplier_name;
        """,
    ),
    (
        "REPORT 2 - DISTRIBUTOR SALES PERFORMANCE",
        """
        SELECT
            d.distributor_name AS Distributor,
            COUNT(DISTINCT sh.shipment_id) AS Shipments,
            COALESCE(SUM(si.quantity_cases), 0) AS Cases,
            COALESCE(ROUND(SUM(si.quantity_cases * w.unit_price), 2), 0)
                AS Wholesale_Value
        FROM distributors d
        LEFT JOIN shipments sh ON d.distributor_id = sh.distributor_id
        LEFT JOIN shipment_items si ON sh.shipment_id = si.shipment_id
        LEFT JOIN wines w ON si.wine_id = w.wine_id
        GROUP BY d.distributor_id, d.distributor_name
        ORDER BY Cases DESC, Wholesale_Value DESC;
        """,
    ),
    (
        "REPORT 3 - QUARTERLY EMPLOYEE HOURS BY DEPARTMENT",
        """
        SELECT
            e.department AS Department,
            t.quarter_number AS Quarter,
            t.work_year AS Year,
            COUNT(DISTINCT e.employee_id) AS Employees,
            ROUND(SUM(t.hours_worked), 2) AS Total_Hours,
            ROUND(AVG(t.hours_worked), 2) AS Avg_Hours
        FROM employees e
        INNER JOIN timesheets t ON e.employee_id = t.employee_id
        GROUP BY e.department, t.quarter_number, t.work_year
        ORDER BY Total_Hours DESC;
        """,
    ),
]


def format_table(headers, rows):
    """Return query results as a fixed-width text table."""
    values = [["" if item is None else str(item) for item in row] for row in rows]
    widths = []
    for index, header in enumerate(headers):
        widths.append(max(len(str(header)), *(len(row[index]) for row in values)))

    border = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    def make_row(row):
        return "| " + " | ".join(
            str(value).ljust(widths[index]) for index, value in enumerate(row)
        ) + " |"

    lines = [border, make_row(headers), border]
    lines.extend(make_row(row) for row in values)
    lines.append(border)
    return "\n".join(lines)


def run_reports():
    """Connect to the database, execute each report, and print its results."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("BACCHUS_DB_HOST", "localhost"),
            user=os.getenv("BACCHUS_DB_USER", "root"),
            password=os.getenv("BACCHUS_DB_PASSWORD", ""),
            database=os.getenv("BACCHUS_DB_NAME", "bacchus_winery"),
        )
        cursor = connection.cursor()

        print("=" * 78)
        print("BACCHUS WINERY MANAGEMENT REPORTS")
        print("=" * 78)

        for title, query in REPORTS:
            cursor.execute(query)
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            print(f"\n{title}")
            print(format_table(headers, rows))

        print("\nAll three reports completed successfully.")

    except Error as error:
        print(f"Database error: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    run_reports()
