-- query for country /index
SELECT
    g.year,
    (SUM(g.valor)/ 1e12) as valor
FROM
    gdp as g
GROUP BY
    g.year
ORDER BY
    g.year ASC;


-- query for gain /index
WITH q AS (
    WITH cte AS (
        SELECT
            g.year,
            (SUM(g.valor)/ 1e12) as valor
        FROM
            gdp as g
        GROUP BY
            g.year
        ORDER BY
            g.year ASC
    )
    SELECT
        LAG(cte.year, 1, 0) OVER (ORDER BY cte.year) || ' -> ' || cte.year AS years
        , LAG(cte.year, 1, 0) OVER (ORDER BY cte.year) AS LAG_year
        , (cte.valor / (LAG(cte.valor, 1, 0) OVER (ORDER BY cte.year))) - 1 AS gain
    FROM cte
)
SELECT q.years, q.gain FROM q WHERE q.LAG_year != 0;


-- query for /states
SELECT
    s.id AS state_id,
    s.shortname AS state_short,
    s.name AS state_name,
    g.year,
    SUM(g.valor) AS valor
FROM
    gdp AS g
LEFT JOIN cities AS c
    on g.cities_id = c.id
LEFT JOIN states AS s
    on c.states_id = s.id
GROUP BY s.id, s.shortname, s.name, g.year
ORDER BY s.id ASC, g.year ASC;

-- states rank /states
with q as (
    SELECT
        s.id AS state_id,
        s.shortname AS state_short,
        s.name AS state_name,
        g.year,
        SUM(g.valor) AS valor
    FROM
        gdp AS g
    LEFT JOIN cities AS c
        on g.cities_id = c.id
    LEFT JOIN states AS s
        on c.states_id = s.id
    GROUP BY s.id, s.shortname, s.name, g.year
    ORDER BY s.id ASC, g.year ASC
)
SELECT
    q.*,
    (q.valor / SUM(q.valor) OVER (PARTITION BY q.year)) AS year_share,
    RANK() OVER (PARTITION BY q.year ORDER BY q.valor DESC) AS rank
FROM q;
    
-- query for city-states /cities
SELECT
    c.id,
    c.name,
    s.name AS state_name
FROM
    cities c
LEFT JOIN states s
    ON c.states_id = s.id
ORDER BY c.name ASC, s.name ASC;

-- query for GDP /cities
SELECT
    c.id as city_id,
    c.name as city_name,
    g.year,
    g.valor
FROM
    gdp AS g
LEFT JOIN cities AS c
    on g.cities_id = c.id;


-- query for POPULATION /cities
SELECT
    p.year,
    p.valor,
    c.name AS city_name,
    c.id
FROM population p
LEFT JOIN cities c
    on p.cities_id = c.id
ORDER BY p.year ASC;