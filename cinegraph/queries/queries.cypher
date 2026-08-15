// CineGraph — Key Cypher Queries

// 1. Multi-hop influence traversal
MATCH path = (m:Movie {id: $id})-[:INFLUENCED*1..4]->(descendant:Movie)
RETURN [node IN nodes(path) | {id: node.id, title: node.title, year: node.year}] AS chain,
       length(path) AS depth
ORDER BY depth;

// 2. Reverse influence chain
MATCH path = (ancestor:Movie)-[:INFLUENCED*1..4]->(m:Movie {id: $id})
RETURN [node IN nodes(path) | {id: node.id, title: node.title, year: node.year}] AS chain,
       length(path) AS depth
ORDER BY depth;

// 3. Collaboration graph
MATCH (p:Person {id: $id})-[:ACTED_IN|DIRECTED]->(m:Movie)
      <-[:ACTED_IN|DIRECTED]-(collab:Person)
WHERE collab.id <> $id
WITH collab, collect(DISTINCT {id:m.id, title:m.title, year:m.year}) AS shared
RETURN collab.id AS id, collab.name AS name, shared,
       size(shared) AS sharedCount
ORDER BY sharedCount DESC
LIMIT 20;

// 4. Graph-scored recommendations
MATCH (m:Movie {id:$id})-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)
WHERE rec.id <> $id
WITH rec, count(DISTINCT g) AS genreOverlap
OPTIONAL MATCH (m:Movie {id:$id})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(rec)
WITH rec, genreOverlap, count(DISTINCT a) AS castOverlap
RETURN rec.id AS id, rec.title AS title, rec.year AS year, rec.rating AS rating,
       genreOverlap, castOverlap, (genreOverlap*2 + castOverlap*3) AS score
ORDER BY score DESC
LIMIT 12;

// 5. Full movie detail
MATCH (m:Movie {id:$id})
OPTIONAL MATCH (m)<-[r:ACTED_IN]-(a:Person)
OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
OPTIONAL MATCH (m)-[:INFLUENCED]->(inf:Movie)
OPTIONAL MATCH (src:Movie)-[:INFLUENCED]->(m)
RETURN m.id AS id, m.title AS title, m.year AS year, m.rating AS rating,
       m.tagline AS tagline, m.overview AS overview,
       collect(DISTINCT {name:a.name,id:a.id,role:r.role}) AS cast,
       collect(DISTINCT {name:d.name,id:d.id}) AS directors,
       collect(DISTINCT g.name) AS genres,
       collect(DISTINCT {id:inf.id,title:inf.title,year:inf.year}) AS influenced,
       collect(DISTINCT {id:src.id,title:src.title,year:src.year}) AS influencedBy;

// 6. Genre statistics
MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie)
RETURN g.name AS name, count(m) AS movieCount
ORDER BY movieCount DESC;

// 7. Database stats
MATCH (m:Movie) WITH count(m) AS movies
MATCH (p:Person) WITH movies, count(p) AS people
MATCH (g:Genre) WITH movies, people, count(g) AS genres
MATCH ()-[r:INFLUENCED]->()
WITH movies, people, genres, count(r) AS influences
RETURN movies, people, genres, influences;
