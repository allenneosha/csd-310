========================================================================
BACCHUS WINERY - MILESTONE #2 TECHNICAL REVIEW GUIDE
========================================================================

INCLUDED FILES:
  1. bacchus_winery.sql  - Complete database dump (11 tables, 3NF, populated)
  2. display_data.py     - Python script to query and display table contents
  3. generate_erd.py    - Python script to extract schema and generate ERD DOT file

EXECUTION SEQUENCE:
  1. Start database:    mariadbd-safe &
  2. Import schema:     mariadb -u root < bacchus_winery.sql
  3. View table data:   python display_data.py
  4. Generate ERD:      python generate_erd.py && dot -Tpng schema.dot -o bacchus_erd.png
========================================================================
