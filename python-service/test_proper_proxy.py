#!/usr/bin/env python3
"""
Test YouTube transcript API with proper proxy configuration using updated API
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

def test_with_proper_proxy():
    """Test YouTube transcript extraction with proper Oxylabs proxy configuration"""

    print("🧪 Testing YouTube Transcript API (Updated v1.2.2) with Oxylabs Proxy")
    print("=" * 70)

    # Configure Oxylabs proxy using GenericProxyConfig
    PROXY_HOST = 'pr.oxylabs.io'
    PROXY_PORT = '7777'
    PROXY_USER = 'customer-snowflake_3blLD'
    PROXY_PASS = 'HyperLight23++'

    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

    print(f"🌐 Proxy: {PROXY_HOST}:{PROXY_PORT}")
    print(f"👤 Username: {PROXY_USER}")
    print()

    try:
        # Create proxy configuration
        proxy_config = GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

        print("✅ GenericProxyConfig created successfully")

        # Initialize YouTubeTranscriptApi with proxy
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        print("✅ YouTubeTranscriptApi initialized with proxy")
        print()

        # Test videos
        test_videos = [
            ("MJDBu5riiR8", "User's specific video"),
            ("dQw4w9WgXcQ", "Rick Roll"),
            ("jNQXAC9IVRw", "Me at the zoo"),
        ]

        for video_id, name in test_videos:
            print(f"🎬 Testing: {name}")
            print(f"📺 Video ID: {video_id}")

            try:
                # Method 1: Direct fetch with new API
                print("📝 Method 1: Direct fetch with proxy...")
                transcript_list = ytt_api.fetch(video_id, languages=['en'])

                if transcript_list:
                    full_transcript = " ".join([entry['text'] for entry in transcript_list])
                    print(f"✅ SUCCESS! Transcript length: {len(full_transcript)} chars")
                    print(f"📄 Preview: {full_transcript[:200]}...")
                    return True, full_transcript

            except Exception as e:
                print(f"❌ Method 1 failed: {str(e)}")

            try:
                # Method 2: List transcripts and fetch
                print("📝 Method 2: List and fetch with proxy...")
                transcript_list = ytt_api.list_transcripts(video_id)

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

    except Exception as setup_error:
        print(f"❌ Setup error: {str(setup_error)}")
        return False, None

    return False, None

def test_without_proxy_comparison():
    """Test without proxy to see the difference"""
    print("🔄 Testing WITHOUT proxy for comparison...")
    print("-" * 70)

    try:
        ytt_api = YouTubeTranscriptApi()
        video_id = "MJDBu5riiR8"

        transcript_list = ytt_api.fetch(video_id, languages=['en'])

        if transcript_list:
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            print(f"✅ SUCCESS without proxy! Length: {len(full_transcript)} chars")
            return True
        else:
            print("❌ No transcript without proxy")
            return False

    except Exception as e:
        print(f"❌ Error without proxy: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Testing YouTube Transcript API v1.2.2 with Oxylabs Proxy")
    print("🔗 Target Video: https://www.youtube.com/watch?v=MJDBu5riiR8")
    print()

    # Test with proxy
    success, transcript = test_with_proper_proxy()

    # Test without proxy for comparison
    no_proxy_success = test_without_proxy_comparison()

    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    print(f"🌐 With Oxylabs Proxy: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"🔄 Without Proxy: {'✅ PASS' if no_proxy_success else '❌ FAIL'}")
    print()

    if success:
        print("🎉 SUCCESS! YouTube transcript extraction works with Oxylabs proxy!")
        print("✅ Ready to proceed with Railway deployment")
        print(f"📝 Sample transcript preview: {transcript[:300]}..." if transcript else "")
    elif no_proxy_success:
        print("⚠️ Works without proxy but fails with proxy - check proxy config")
    else:
        print("❌ Both configurations failed")
        print("🔧 YouTube may be blocking requests or API has changed")

    print("=" * 70)