import os
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from neo4j import GraphDatabase
from dotenv import load_dotenv

CWD = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR = os.path.join(CWD, 'frontend')

load_dotenv()

# Serve frontend static files so the UI and API share the same origin.
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt+s://db-db698bac.databases.cognodb.com")
NEO4J_USER = os.environ.get("NEO4J_USER", "cognodb")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "7d60ed662e3883796ab9f0744178fe94")

driver = None

def get_driver():
    global driver
    if driver is None:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
    return driver

def db_query(cypher, params=None):
    with get_driver().session() as session:
        result = session.run(cypher, params or {})
        return [record.data() for record in result]

@app.route("/api/health")
def health():
    try:
        db_query("RETURN 1 AS ok")
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 503

@app.route("/api/movies")
def list_movies():
    q = """
    MATCH (m:Movie)
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
    OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
    RETURN m.id AS id, m.title AS title, m.year AS year,
           m.rating AS rating, m.poster AS poster, m.tagline AS tagline,
           collect(DISTINCT a.name)[0..3] AS topCast,
           collect(DISTINCT g.name) AS genres
    ORDER BY m.year DESC
    """
    return jsonify(db_query(q))

@app.route("/api/movies/search")
def search_movies():
    term = request.args.get("q", "").strip()
    if not term:
        return jsonify([])
    q = """
    MATCH (m:Movie)
    WHERE toLower(m.title) CONTAINS toLower($term)
    OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
    RETURN m.id AS id, m.title AS title, m.year AS year,
           m.rating AS rating, m.poster AS poster,
           collect(DISTINCT g.name) AS genres
    ORDER BY m.year DESC LIMIT 20
    """
    return jsonify(db_query(q, {"term": term}))

@app.route("/api/movies/<movie_id>")
def movie_detail(movie_id):
    q = """
    MATCH (m:Movie {id: $id})
    OPTIONAL MATCH (m)<-[r:ACTED_IN]-(a:Person)
    OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
    OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
    OPTIONAL MATCH (m)-[:INFLUENCED]->(inf:Movie)
    OPTIONAL MATCH (src:Movie)-[:INFLUENCED]->(m)
    RETURN m.id AS id, m.title AS title, m.year AS year,
           m.rating AS rating, m.poster AS poster, m.tagline AS tagline,
           m.overview AS overview,
           collect(DISTINCT {name: a.name, id: a.id, role: r.role}) AS cast,
           collect(DISTINCT {name: d.name, id: d.id}) AS directors,
           collect(DISTINCT g.name) AS genres,
           collect(DISTINCT {id: inf.id, title: inf.title, year: inf.year}) AS influenced,
           collect(DISTINCT {id: src.id, title: src.title, year: src.year}) AS influencedBy
    """
    rows = db_query(q, {"id": movie_id})
    if not rows:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(rows[0])

@app.route("/api/people/<person_id>")
def person_detail(person_id):
    q = """
    MATCH (p:Person {id: $id})
    OPTIONAL MATCH (p)-[:ACTED_IN]->(m:Movie)
    OPTIONAL MATCH (p)-[:DIRECTED]->(dm:Movie)
    RETURN p.id AS id, p.name AS name, p.born AS born,
           collect(DISTINCT {id: m.id, title: m.title, year: m.year, rating: m.rating}) AS movies,
           collect(DISTINCT {id: dm.id, title: dm.title, year: dm.year}) AS directed
    """
    rows = db_query(q, {"id": person_id})
    if not rows:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(rows[0])

@app.route("/api/influence-chain/<movie_id>")
def influence_chain(movie_id):
    descendants_q = """
    MATCH path = (m:Movie {id: $id})-[:INFLUENCED*1..4]->(descendant:Movie)
    RETURN [node IN nodes(path) | {id: node.id, title: node.title, year: node.year}] AS chain,
           length(path) AS depth
    ORDER BY depth LIMIT 30
    """
    ancestors_q = """
    MATCH path = (ancestor:Movie)-[:INFLUENCED*1..4]->(m:Movie {id: $id})
    RETURN [node IN nodes(path) | {id: node.id, title: node.title, year: node.year}] AS chain,
           length(path) AS depth
    ORDER BY depth LIMIT 30
    """
    return jsonify({
        "descendants": db_query(descendants_q, {"id": movie_id}),
        "ancestors": db_query(ancestors_q, {"id": movie_id})
    })

@app.route("/api/collaborators/<person_id>")
def collaborators(person_id):
    q = """
    MATCH (p:Person {id: $id})-[:ACTED_IN|DIRECTED]->(m:Movie)
          <-[:ACTED_IN|DIRECTED]-(collab:Person)
    WHERE collab.id <> $id
    WITH collab, collect(DISTINCT {id: m.id, title: m.title, year: m.year}) AS shared
    RETURN collab.id AS id, collab.name AS name, shared,
           size(shared) AS sharedCount
    ORDER BY sharedCount DESC LIMIT 20
    """
    return jsonify(db_query(q, {"id": person_id}))

@app.route("/api/recommendations/<movie_id>")
def recommendations(movie_id):
    q = """
    MATCH (m:Movie {id: $id})-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)
    WHERE rec.id <> $id
    WITH rec, count(DISTINCT g) AS genreOverlap
    OPTIONAL MATCH (m:Movie {id: $id})<-[:ACTED_IN]-(a:Person)-[:ACTED_IN]->(rec)
    WITH rec, genreOverlap, count(DISTINCT a) AS castOverlap
    RETURN rec.id AS id, rec.title AS title, rec.year AS year,
           rec.rating AS rating, rec.poster AS poster,
           genreOverlap, castOverlap,
           (genreOverlap * 2 + castOverlap * 3) AS score
    ORDER BY score DESC LIMIT 12
    """
    return jsonify(db_query(q, {"id": movie_id}))

@app.route("/api/genres")
def list_genres():
    q = """
    MATCH (g:Genre)<-[:IN_GENRE]-(m:Movie)
    RETURN g.name AS name, count(m) AS movieCount
    ORDER BY movieCount DESC
    """
    return jsonify(db_query(q))

@app.route("/api/genres/<genre_name>/movies")
def movies_by_genre(genre_name):
    q = """
    MATCH (g:Genre {name: $name})<-[:IN_GENRE]-(m:Movie)
    RETURN m.id AS id, m.title AS title, m.year AS year,
           m.rating AS rating, m.poster AS poster
    ORDER BY m.rating DESC LIMIT 30
    """
    return jsonify(db_query(q, {"name": genre_name}))

@app.route("/api/stats")
def stats():
    q = """
    MATCH (m:Movie) WITH count(m) AS movies
    MATCH (p:Person) WITH movies, count(p) AS people
    MATCH (g:Genre) WITH movies, people, count(g) AS genres
    MATCH ()-[r:INFLUENCED]->()
    WITH movies, people, genres, count(r) AS influences
    RETURN movies, people, genres, influences
    """
    rows = db_query(q)
    return jsonify(rows[0] if rows else {})


# Serve the frontend index
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.name, "detail": e.description}), e.code
    return jsonify({"error": "Server error", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
