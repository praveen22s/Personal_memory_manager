"""
Test Neo4j connection before starting the app
"""
import asyncio
import os
from dotenv import load_dotenv
from diary.database import DiaryDatabase

load_dotenv()

async def test_neo4j():
    print("Testing Neo4j connection...")
    print(f"URI: {os.getenv('NEO4J_URI', 'bolt://localhost:7687')}")
    print(f"User: {os.getenv('NEO4J_USER', 'neo4j')}")
    
    try:
        db = DiaryDatabase()
        await db.connect()
        print("[OK] Neo4j connection successful!")
        await db.close()
        return True
    except Exception as e:
        print(f"[ERROR] Neo4j connection failed: {e}")
        print("\nPlease check:")
        print("1. Neo4j Desktop is running")
        print("2. Your database is Active (green)")
        print("3. Password in .env is correct")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_neo4j())
    exit(0 if result else 1)
