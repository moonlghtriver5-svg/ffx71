#!/usr/bin/env python3
"""
Local test script for the YouTube transcript service
"""

import asyncio
import sys
from main import app, get_transcript, TranscriptRequest

async def test_transcript_extraction():
    """Test transcript extraction with a known video"""

    print("🧪 Testing YouTube Transcript Extraction with Oxylabs...")
    print("=" * 60)

    # Test with Rick Roll (known to have transcripts)
    test_video_id = "dQw4w9WgXcQ"

    print(f"🎬 Testing with video ID: {test_video_id}")
    print(f"🌐 Using Oxylabs proxy: pr.oxylabs.io:7777")
    print(f"👤 Username: customer-snowflake_3blLD")
    print()

    try:
        # Create request
        request = TranscriptRequest(video_id=test_video_id)

        # Get transcript
        print("📝 Fetching transcript...")
        result = await get_transcript(request)

        if result.success:
            print("✅ SUCCESS! Transcript extracted successfully!")
            print(f"📊 Transcript length: {len(result.transcript)} characters")
            print(f"🌍 Language: {result.language}")
            print()
            print("📄 Transcript preview (first 300 characters):")
            print("-" * 60)
            print(result.transcript[:300] + "...")
            print("-" * 60)

            return True

        else:
            print(f"❌ FAILED: {result.error}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

async def test_boxing_video():
    """Test with a boxing video"""

    print("\n🥊 Testing with boxing content...")
    print("=" * 60)

    # Boxing video IDs to try
    boxing_videos = [
        "LXZfuC0vi4g",  # Example boxing video
        "9A2UC7_KM4E",  # Another boxing video
    ]

    for video_id in boxing_videos:
        print(f"🥊 Testing boxing video: {video_id}")

        try:
            request = TranscriptRequest(video_id=video_id)
            result = await get_transcript(request)

            if result.success:
                print(f"✅ Boxing video transcript extracted!")
                print(f"📊 Length: {len(result.transcript)} characters")

                # Look for boxing keywords
                boxing_terms = ['fight', 'round', 'knockout', 'boxing', 'punch']
                found_terms = [term for term in boxing_terms if term.lower() in result.transcript.lower()]

                if found_terms:
                    print(f"🥊 Boxing terms found: {', '.join(found_terms)}")

                print(f"📄 Preview: {result.transcript[:200]}...")
                return True

            else:
                print(f"⚠️ Failed to get transcript: {result.error}")
                continue

        except Exception as e:
            print(f"❌ Error with video {video_id}: {str(e)}")
            continue

    print("❌ No boxing video transcripts could be extracted")
    return False

async def main():
    """Run all tests"""

    print("🚀 YouTube Transcript Service Local Test")
    print("🔗 Repository: https://github.com/jdepoix/youtube-transcript-api")
    print("🌐 Using Oxylabs proxy for transcript extraction")
    print()

    # Test 1: Basic transcript extraction
    test1_success = await test_transcript_extraction()

    # Test 2: Boxing video
    test2_success = await test_boxing_video()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Basic transcript test: {'PASS' if test1_success else 'FAIL'}")
    print(f"🥊 Boxing video test: {'PASS' if test2_success else 'FAIL'}")

    if test1_success or test2_success:
        print("\n🎉 Service is working! Ready for Railway deployment.")
        print("\n📋 Next steps:")
        print("1. Deploy Python service to Railway")
        print("2. Update Next.js app to use Railway URL")
        print("3. Test the full pipeline")
    else:
        print("\n⚠️ Service needs debugging before deployment.")
        print("Check proxy configuration and video IDs.")

    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())