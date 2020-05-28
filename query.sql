SELECT gdp.id, gdp.country, gdp.gdp, gdp.country_code, world_table.population
FROM gdp
INNER JOIN world_table
ON gdp.country_code = world_table.country_code;