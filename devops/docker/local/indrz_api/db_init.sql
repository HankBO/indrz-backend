CREATE SCHEMA IF NOT EXISTS django AUTHORIZATION indrzdev;
CREATE SCHEMA IF NOT EXISTS geodata AUTHORIZATION indrzdev;
ALTER ROLE indrzdev IN DATABASE indrzdev SET search_path TO django,geodata,dxf_tables,pre_django,bookway,routing,public;
