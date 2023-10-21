-- Write a SQL script that creates an index idx_name_first on the table names and the first letter of name.

-- Requirements:

-- Import this table dump: names.sql.zip
-- Only the first letter of name must be indexed
-- Context: Index is not the solution for any performance issue, but well used, it’s really powerful!

-- Add a virtual column for the first letter of the name
-- Add a new column 'first_letter'
-- Create an index on the 'first_letter' column

CREATE INDEX idx_name_first
ON names (name(1));