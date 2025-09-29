#!/usr/bin/env python3
"""
Test YouTube transcript API with proper Oxylabs proxy configuration
"""

from youtube_transcript_api import YouTubeTranscriptApi

def test_with_oxylabs_proxy():
    """Test YouTube transcript extraction with Oxylabs proxy"""

    print("🧪 Testing YouTube Transcript API with Oxylabs Proxy")
    print("=" * 60)

    # Configure Oxylabs proxy
    PROXY_HOST = 'pr.oxylabs.io'
    PROXY_PORT = '7777'
    PROXY_USER = 'customer-snowflake_3blLD'
    PROXY_PASS = 'HyperLight23++'

    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    print(f"🌐 Proxy: {PROXY_HOST}:{PROXY_PORT}")
    print(f"👤 Username: {PROXY_USER}")
    print()

    # Test videos that are known to have transcripts
    test_videos = [
        ("dQw4w9WgXcQ", "Rick Roll"),
        ("MJDBu5riiR8", "User's specific video"),
        ("jNQXAC9IVRw", "Me at the zoo"),
    ]

    for video_id, name in test_videos:
        print(f"🎬 Testing: {name}")
        print(f"📺 Video ID: {video_id}")

        try:
            # Method 1: Basic get_transcript with proxy
            print("📝 Method 1: get_transcript with proxy...")
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                proxies=proxies
            )

            if transcript_list:
                full_transcript = " ".join([entry['text'] for entry in transcript_list])
                print(f"✅ SUCCESS! Transcript length: {len(full_transcript)} chars")
                print(f"📄 Preview: {full_transcript[:200]}...")
                return True, full_transcript

        except Exception as e:
            print(f"❌ Method 1 failed: {str(e)}")

        try:
            # Method 2: List transcripts first with proxy
            print("📝 Method 2: list_transcripts with proxy...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(
                video_id,
                proxies=proxies
            )

            print("📋 Available transcripts:")
            for transcript in transcript_list:
                print(f"  - {transcript.language} ({transcript.language_code}) - Generated: {transcript.is_generated}")

                try:
                    transcript_data = transcript.fetch()
                    if transcript_data:
                        full_transcript = " ".join([entry['text'] for entry in transcript_data])
                        print(f"✅ SUCCESS with {transcript.language}!")
                        print(f"📊 Length: {len(full_transcript)} characters")
                        print(f"📄 Preview: {full_transcript[:200]}...")
                        return True, full_transcript

                except Exception as fetch_error:
                    print(f"   ❌ Failed to fetch {transcript.language}: {str(fetch_error)}")
                    continue

        except Exception as e:
            print(f"❌ Method 2 failed: {str(e)}")

        print()

    return False, None

if __name__ == "__main__":
    print("🎯 Testing YouTube Transcript API with Oxylabs Proxy")
    print("🔗 Target Video: https://www.youtube.com/watch?v=MJDBu5riiR8")
    print()

    success, transcript = test_with_oxylabs_proxy()

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)

    if success:
        print("🎉 SUCCESS! YouTube transcript extraction works with Oxylabs proxy!")
        print("✅ Ready to proceed with Railway deployment")
        print(f"📝 Sample transcript: {transcript[:300]}..." if transcript else "")
    else:
        print("❌ Failed to extract transcripts even with proxy")
        print("🔧 May need alternative transcript extraction method")

    print("=" * 60)