from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
import uvicorn
import uuid
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = FastAPI(title="Boxing Transcript API with Database", version="2.0.0")

class TranscriptRequest(BaseModel):
    video_id: str
    languages: Optional[List[str]] = ['en']
    title: Optional[str] = None
    channel: Optional[str] = None
    url: Optional[str] = None

class TranscriptResponse(BaseModel):
    video_id: str
    transcript: str
    language: str
    success: bool
    stored_in_db: bool = False
    db_record_id: Optional[str] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    proxy_configured: bool
    database_connected: bool
    service: str

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_BUpE0JYr5geo@ep-morning-hall-ad96rqg8-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')

# Configure Oxylabs proxy with working credentials
OXYLABS_HOST = os.getenv('OXYLABS_PROXY_HOST', 'pr.oxylabs.io')
OXYLABS_PORT = os.getenv('OXYLABS_PROXY_PORT', '7777')
OXYLABS_USERNAME = os.getenv('OXYLABS_PROXY_USERNAME', 'snowflake2_CgJtr')
OXYLABS_PASSWORD = os.getenv('OXYLABS_PROXY_PASSWORD', 'Fighter34+++')

# Create proxy configuration for Oxylabs
proxy_url = f"http://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@{OXYLABS_HOST}:{OXYLABS_PORT}"

proxy_config = GenericProxyConfig(
    http_url=proxy_url,
    https_url=proxy_url
)

def get_db_connection():
    """Get database connection to Neon PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return None

def test_db_connection():
    """Test database connection"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return True
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
    return False

def store_video_transcript(video_id: str, transcript: str, title: str = None, channel: str = None, url: str = None):
    """Store video transcript in Neon database"""
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()

        # Check if video already exists
        cursor.execute("SELECT id FROM videos WHERE youtube_id = %s", (video_id,))
        existing = cursor.fetchone()

        if existing:
            # Update existing record with transcript
            cursor.execute("""
                UPDATE videos
                SET transcript = %s, is_processed = true, updated_at = NOW()
                WHERE youtube_id = %s
                RETURNING id
            """, (transcript, video_id))
            record_id = cursor.fetchone()['id']
            print(f"✅ Updated existing video record: {record_id}")
        else:
            # Insert new video record
            record_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO videos (
                    id, youtube_id, title, url, channel, transcript,
                    published_at, source, is_processed, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (
                record_id,
                video_id,
                title or f"Video {video_id}",
                url or f"https://www.youtube.com/watch?v={video_id}",
                channel or "Unknown",
                transcript,
                datetime.now(),
                "transcript-api",
                True
            ))
            print(f"✅ Created new video record: {record_id}")

        conn.commit()
        cursor.close()
        conn.close()
        return record_id

    except Exception as e:
        print(f"❌ Failed to store in database: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        return None

@app.get("/", response_model=HealthResponse)
async def health_check():
    db_connected = test_db_connection()
    return HealthResponse(
        status="healthy",
        proxy_configured=bool(OXYLABS_USERNAME and OXYLABS_PASSWORD),
        database_connected=db_connected,
        service="Boxing Transcript API with Database"
    )

@app.post("/transcript", response_model=TranscriptResponse)
async def get_transcript(request: TranscriptRequest):
    """
    Extract transcript from YouTube video and store in Neon database
    """
    try:
        print(f"🎬 Fetching transcript for video: {request.video_id}")
        print(f"🌐 Using Oxylabs proxy: {OXYLABS_HOST}:{OXYLABS_PORT}")

        # Initialize YouTube Transcript API with proxy
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

        # Fetch transcript using working API structure
        fetched_transcript = ytt_api.fetch(request.video_id, languages=request.languages)

        # Extract text from transcript object
        full_transcript = ""
        language = "en"

        if hasattr(fetched_transcript, 'snippets'):
            full_transcript = " ".join([snippet.text for snippet in fetched_transcript.snippets])
            language = getattr(fetched_transcript, 'language_code', 'en')
        elif hasattr(fetched_transcript, '__iter__'):
            # Fallback for different API structures
            try:
                full_transcript = " ".join([item['text'] if isinstance(item, dict) else str(item) for item in fetched_transcript])
            except:
                full_transcript = str(fetched_transcript)

        print(f"✅ Successfully fetched transcript ({len(full_transcript)} chars)")

        # Store in Neon database
        print(f"💾 Storing transcript in Neon database...")
        db_record_id = store_video_transcript(
            video_id=request.video_id,
            transcript=full_transcript,
            title=request.title,
            channel=request.channel,
            url=request.url
        )

        stored_in_db = db_record_id is not None
        if stored_in_db:
            print(f"✅ Transcript stored in database with ID: {db_record_id}")
        else:
            print(f"⚠️ Transcript extracted but not stored in database")

        return TranscriptResponse(
            video_id=request.video_id,
            transcript=full_transcript,
            language=language,
            success=True,
            stored_in_db=stored_in_db,
            db_record_id=str(db_record_id) if db_record_id else None
        )

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to fetch transcript: {error_msg}")

        return TranscriptResponse(
            video_id=request.video_id,
            transcript="",
            language="",
            success=False,
            stored_in_db=False,
            error=error_msg
        )

@app.post("/transcript/batch")
async def get_batch_transcripts(video_ids: List[str]):
    """
    Get transcripts for multiple videos and store them all in database
    """
    results = []

    for video_id in video_ids:
        try:
            request = TranscriptRequest(video_id=video_id)
            result = await get_transcript(request)
            results.append(result)

        except Exception as e:
            results.append(TranscriptResponse(
                video_id=video_id,
                transcript="",
                language="",
                success=False,
                stored_in_db=False,
                error=str(e)
            ))

    successful_stores = sum(1 for r in results if r.stored_in_db)

    return {
        "results": results,
        "total": len(results),
        "successful_extractions": sum(1 for r in results if r.success),
        "stored_in_database": successful_stores
    }

@app.get("/test")
async def test_transcript():
    """
    Test endpoint with user's verified working video
    """
    test_video_id = "MJDBu5riiR8"  # User's specific video - confirmed working

    request = TranscriptRequest(
        video_id=test_video_id,
        title="Boxing Interview - User Test Video",
        channel="Boxing Channel",
        url=f"https://www.youtube.com/watch?v={test_video_id}"
    )
    result = await get_transcript(request)

    return {
        "test_video_id": test_video_id,
        "result": result,
        "proxy_info": {
            "host": OXYLABS_HOST,
            "port": OXYLABS_PORT,
            "username": OXYLABS_USERNAME[:10] + "..." if OXYLABS_USERNAME else None
        },
        "database_info": {
            "connected": test_db_connection(),
            "transcript_stored": result.stored_in_db,
            "record_id": result.db_record_id
        }
    }

@app.get("/videos")
async def get_videos():
    """
    Get all videos from database
    """
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, youtube_id, title, channel, source, is_processed,
                   LENGTH(transcript) as transcript_length, created_at
            FROM videos
            ORDER BY created_at DESC
            LIMIT 50
        """)

        videos = cursor.fetchall()
        cursor.close()
        conn.close()

        return {"videos": videos, "total": len(videos)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/videos/{video_id}")
async def get_video(video_id: str):
    """
    Get specific video from database
    """
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM videos WHERE youtube_id = %s OR id = %s
        """, (video_id, video_id))

        video = cursor.fetchone()
        cursor.close()
        conn.close()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        return {"video": video}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)