import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.environ.get("NEO4J_URI", "bolt+s://db-db698bac.databases.cognodb.com")
USER = os.environ.get("NEO4J_USER", "cognodb")
PASSWORD = os.environ.get("NEO4J_PASSWORD", "7d60ed662e3883796ab9f0744178fe94")

if not PASSWORD:
    raise RuntimeError("NEO4J_PASSWORD is missing. Put it in your .env file.")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

GENRES = [
    "Sci-Fi", "Drama", "Thriller", "Action", "Horror",
    "Crime", "Romance", "Animation", "Fantasy", "Documentary",
    "Comedy", "Adventure", "Mystery"
]

PEOPLE = [
    {"id":"p1","name":"Stanley Kubrick","born":1928},{"id":"p2","name":"Ridley Scott","born":1937},
    {"id":"p3","name":"Christopher Nolan","born":1970},{"id":"p4","name":"Denis Villeneuve","born":1967},
    {"id":"p5","name":"Keanu Reeves","born":1964},{"id":"p6","name":"Carrie-Anne Moss","born":1967},
    {"id":"p7","name":"Laurence Fishburne","born":1961},{"id":"p8","name":"Harrison Ford","born":1942},
    {"id":"p9","name":"Sigourney Weaver","born":1949},{"id":"p10","name":"Arnold Schwarzenegger","born":1947},
    {"id":"p11","name":"Leonardo DiCaprio","born":1974},{"id":"p12","name":"Tom Hanks","born":1956},
    {"id":"p13","name":"Cillian Murphy","born":1976},{"id":"p14","name":"Matthew McConaughey","born":1969},
    {"id":"p15","name":"Anne Hathaway","born":1982},{"id":"p16","name":"Timothée Chalamet","born":1995},
    {"id":"p17","name":"Zendaya","born":1996},{"id":"p18","name":"Rebecca Ferguson","born":1983},
    {"id":"p19","name":"Lilly Wachowski","born":1967},{"id":"p20","name":"Lana Wachowski","born":1965},
    {"id":"p21","name":"James Cameron","born":1954},{"id":"p22","name":"Steven Spielberg","born":1946},
    {"id":"p23","name":"Francis Ford Coppola","born":1939},{"id":"p24","name":"Martin Scorsese","born":1942},
    {"id":"p25","name":"Jonathan Nolan","born":1976},{"id":"p26","name":"Ryan Gosling","born":1980},
    {"id":"p27","name":"Ana de Armas","born":1988},{"id":"p28","name":"Oscar Isaac","born":1979},
    {"id":"p29","name":"Jessica Chastain","born":1977},{"id":"p30","name":"Michael B. Jordan","born":1987},
]

MOVIES = [
{"id":"m1","title":"2001: A Space Odyssey","year":1968,"rating":8.3,"tagline":"An epic drama of adventure and exploration","overview":"After discovering a mysterious artifact on the moon, humanity embarks on a voyage to Jupiter — only to encounter an AI with its own agenda.","genres":["Sci-Fi","Drama","Mystery"],"director":"p1","cast":[{"id":"p8","role":"Dr. Heywood Floyd"}]},
{"id":"m2","title":"Blade Runner","year":1982,"rating":8.1,"tagline":"Man has made his match. Now it's his problem.","overview":"A blade runner must pursue and terminate four replicants who have stolen a ship in space and returned to Earth to find their creator.","genres":["Sci-Fi","Drama","Thriller"],"director":"p2","cast":[{"id":"p8","role":"Rick Deckard"}]},
{"id":"m3","title":"The Matrix","year":1999,"rating":8.7,"tagline":"Welcome to the Real World.","overview":"A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.","genres":["Sci-Fi","Action","Thriller"],"director":"p19","cast":[{"id":"p5","role":"Neo"},{"id":"p6","role":"Trinity"},{"id":"p7","role":"Morpheus"}]},
{"id":"m4","title":"Alien","year":1979,"rating":8.5,"tagline":"In space no one can hear you scream.","overview":"After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form.","genres":["Sci-Fi","Horror","Thriller"],"director":"p2","cast":[{"id":"p9","role":"Ellen Ripley"}]},
{"id":"m5","title":"The Terminator","year":1984,"rating":8.1,"tagline":"He'll be back.","overview":"A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine.","genres":["Sci-Fi","Action","Thriller"],"director":"p21","cast":[{"id":"p10","role":"The Terminator"}]},
{"id":"m6","title":"Inception","year":2010,"rating":8.8,"tagline":"Your mind is the scene of the crime.","overview":"A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into a C.E.O.'s mind.","genres":["Sci-Fi","Action","Thriller"],"director":"p3","cast":[{"id":"p11","role":"Dom Cobb"}]},
{"id":"m7","title":"Interstellar","year":2014,"rating":8.6,"tagline":"Mankind was born on Earth. It was never meant to die here.","overview":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","genres":["Sci-Fi","Drama","Adventure"],"director":"p3","cast":[{"id":"p14","role":"Cooper"},{"id":"p15","role":"Brand"},{"id":"p29","role":"Murph (adult)"}]},
{"id":"m8","title":"Blade Runner 2049","year":2017,"rating":8.0,"tagline":"The key to the future is finally unearthed.","overview":"A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.","genres":["Sci-Fi","Drama","Mystery"],"director":"p4","cast":[{"id":"p26","role":"K"},{"id":"p8","role":"Rick Deckard"},{"id":"p27","role":"Joi"}]},
{"id":"m9","title":"Dune","year":2021,"rating":8.0,"tagline":"Beyond fear, destiny awaits.","overview":"Paul Atreides, a brilliant and gifted young man born into a great destiny, must travel to the most dangerous planet in the universe.","genres":["Sci-Fi","Drama","Adventure"],"director":"p4","cast":[{"id":"p16","role":"Paul Atreides"},{"id":"p17","role":"Chani"},{"id":"p18","role":"Lady Jessica"},{"id":"p28","role":"Duke Leto Atreides"}]},
{"id":"m10","title":"Dune: Part Two","year":2024,"rating":8.5,"tagline":"Long live the fighters.","overview":"Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.","genres":["Sci-Fi","Drama","Action"],"director":"p4","cast":[{"id":"p16","role":"Paul Atreides"},{"id":"p17","role":"Chani"},{"id":"p18","role":"Lady Jessica"}]},
{"id":"m11","title":"Oppenheimer","year":2023,"rating":8.9,"tagline":"The world forever changes.","overview":"The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.","genres":["Drama","Thriller","Mystery"],"director":"p3","cast":[{"id":"p13","role":"J. Robert Oppenheimer"},{"id":"p11","role":"Leslie Groves"}]},
{"id":"m13","title":"Ex Machina","year":2014,"rating":7.7,"tagline":"What happens to me if I fail your test?","overview":"A young programmer is selected to participate in a ground-breaking experiment in synthetic intelligence.","genres":["Sci-Fi","Drama","Thriller"],"director":"p2","cast":[{"id":"p27","role":"Ava"}]},
{"id":"m14","title":"Her","year":2013,"rating":8.0,"tagline":"A story about love.","overview":"In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.","genres":["Sci-Fi","Drama","Romance"],"director":"p4","cast":[]},
{"id":"m15","title":"Contact","year":1997,"rating":7.5,"tagline":"If it's just us, it seems like an awful waste of space.","overview":"Dr. Ellie Arroway, after years of searching, finds conclusive radio proof of extraterrestrial intelligence.","genres":["Sci-Fi","Drama","Mystery"],"director":"p22","cast":[]},
{"id":"m16","title":"Arrival","year":2016,"rating":7.9,"tagline":"Why are they here?","overview":"A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.","genres":["Sci-Fi","Drama","Mystery"],"director":"p4","cast":[]},
{"id":"m17","title":"The Godfather","year":1972,"rating":9.2,"tagline":"An offer you can't refuse.","overview":"The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.","genres":["Crime","Drama"],"director":"p23","cast":[]},
{"id":"m18","title":"Goodfellas","year":1990,"rating":8.7,"tagline":"Three decades of life in the mafia.","overview":"The story of Henry Hill and his life in the mob, covering his relationship with his wife and mob partners.","genres":["Crime","Drama"],"director":"p24","cast":[]},
{"id":"m19","title":"Minority Report","year":2002,"rating":7.7,"tagline":"Everybody runs.","overview":"In a future where a special police unit is able to arrest murderers before they commit their crimes, an officer is accused of a future murder.","genres":["Sci-Fi","Action","Thriller"],"director":"p22","cast":[]},
{"id":"m20","title":"A.I. Artificial Intelligence","year":2001,"rating":7.1,"tagline":"His love is real. He is not.","overview":"A highly advanced robotic boy longs to become 'real' so that he can regain the love of his human mother.","genres":["Sci-Fi","Drama","Adventure"],"director":"p22","cast":[]},
]

INFLUENCES = [
("m1","m2"),("m1","m4"),("m1","m9"),("m2","m3"),("m2","m8"),("m2","m13"),
("m3","m6"),("m4","m5"),("m5","m3"),("m6","m7"),("m6","m11"),("m7","m9"),
("m9","m10"),("m13","m14"),("m1","m15"),("m15","m16"),("m16","m9"),("m17","m18"),
("m1","m19"),("m1","m20"),("m5","m19"),("m2","m20"),("m7","m16"),("m3","m13"),("m8","m10")
]

def run(cypher, params=None):
    with driver.session() as session:
        session.run(cypher, params or {}).consume()

def seed():
    print("Clearing existing data...")
    run("MATCH (n) DETACH DELETE n")

    print("Creating constraints...")
    for label, prop in [("Movie","id"),("Person","id"),("Genre","name")]:
        run(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.{prop} IS UNIQUE")

    print("Seeding genres...")
    for name in GENRES:
        run("MERGE (g:Genre {name:$name})", {"name":name})

    print("Seeding people...")
    for p in PEOPLE:
        run("MERGE (p:Person {id:$id}) SET p.name=$name, p.born=$born", p)

    print("Seeding movies...")
    for m in MOVIES:
        run("""
        MERGE (movie:Movie {id:$id})
        SET movie.title=$title, movie.year=$year, movie.rating=$rating,
            movie.tagline=$tagline, movie.overview=$overview
        """, {k:m[k] for k in ["id","title","year","rating","tagline","overview"]})

        run("""
        MATCH (p:Person {id:$pid}), (movie:Movie {id:$mid})
        MERGE (p)-[:DIRECTED]->(movie)
        """, {"pid":m["director"],"mid":m["id"]})

        for c in m.get("cast", []):
            run("""
            MATCH (p:Person {id:$pid}), (movie:Movie {id:$mid})
            MERGE (p)-[r:ACTED_IN]->(movie)
            SET r.role=$role
            """, {"pid":c["id"],"mid":m["id"],"role":c.get("role","")})

        for g in m.get("genres", []):
            run("""
            MATCH (movie:Movie {id:$mid}), (g:Genre {name:$gname})
            MERGE (movie)-[:IN_GENRE]->(g)
            """, {"mid":m["id"],"gname":g})

    print("Seeding influence relationships...")
    for src, tgt in INFLUENCES:
        run("""
        MATCH (a:Movie {id:$src}), (b:Movie {id:$tgt})
        MERGE (a)-[:INFLUENCED]->(b)
        """, {"src":src,"tgt":tgt})

    print("Seed complete.")
    driver.close()

if __name__ == "__main__":
    seed()
