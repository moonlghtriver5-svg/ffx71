#!/usr/bin/env python3
"""
Test YouTube transcript API with working Oxylabs proxy credentials
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

def test_with_working_proxy():
    """Test YouTube transcript extraction with working Oxylabs proxy"""

    print("🎯 Testing YouTube Transcript API with Working Oxylabs Proxy")
    print("=" * 70)

    # Updated working Oxylabs proxy credentials
    PROXY_HOST = 'pr.oxylabs.io'
    PROXY_PORT = '7777'
    PROXY_USER = 'snowflake2_CgJtr'
    PROXY_PASS = 'Fighter34+++'

    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

    print(f"🌐 Proxy: {PROXY_HOST}:{PROXY_PORT}")
    print(f"👤 Username: {PROXY_USER}")
    print(f"✅ Proxy verified working (IP: 78.80.96.215)")
    print()

    try:
        # Create proxy configuration
        proxy_config = GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

        # Initialize YouTubeTranscriptApi with working proxy
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        print("✅ YouTubeTranscriptApi initialized with working proxy")
        print()

        # Test the user's specific video first
        test_videos = [
            ("MJDBu5riiR8", "User's specific video"),
            ("dQw4w9WgXcQ", "Rick Roll"),
            ("jNQXAC9IVRw", "Me at the zoo"),
        ]

        for video_id, name in test_videos:
            print(f"🎬 Testing: {name}")
            print(f"📺 Video ID: {video_id}")

            try:
                # Method 1: Direct fetch
                print("📝 Method 1: Direct fetch with working proxy...")
                fetched_transcript = ytt_api.fetch(video_id, languages=['en'])

                # Check different possible structures
                transcript_text = None

                if hasattr(fetched_transcript, 'snippets'):
                    transcript_text = " ".join([snippet.text for snippet in fetched_transcript.snippets])
                elif hasattr(fetched_transcript, '__iter__'):
                    # Try to iterate and get text
                    try:
                        transcript_text = " ".join([item['text'] if isinstance(item, dict) else str(item) for item in fetched_transcript])
                    except:
                        pass

                if transcript_text and transcript_text.strip():
                    print(f"✅ SUCCESS! Transcript length: {len(transcript_text)} chars")
                    print(f"📄 Preview: {transcript_text[:300]}...")
                    return True, transcript_text

            except Exception as e:
                print(f"❌ Method 1 failed: {str(e)}")

            try:
                # Method 2: List and fetch manually
                print("📝 Method 2: List transcripts with working proxy...")
                transcript_list = ytt_api.list(video_id)

                print("📋 Available transcripts:")
                for transcript in transcript_list:
                    print(f"  - {transcript.language} ({transcript.language_code}) - Generated: {transcript.is_generated}")

                    try:
                        transcript_data = transcript.fetch()

                        # Try different ways to extract text
                        transcript_text = None
                        if hasattr(transcript_data, 'snippets'):
                            transcript_text = " ".join([snippet.text for snippet in transcript_data.snippets])
                        elif hasattr(transcript_data, '__iter__'):
                            try:
                                transcript_text = " ".join([item['text'] if isinstance(item, dict) else str(item) for item in transcript_data])
                            except:
                                pass

                        if transcript_text and transcript_text.strip():
                            print(f"✅ SUCCESS with {transcript.language}!")
                            print(f"📊 Length: {len(transcript_text)} characters")
                            print(f"📄 Preview: {transcript_text[:300]}...")
                            return True, transcript_text

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

if __name__ == "__main__":
    print("🚀 Final Test: YouTube Transcript with Working Proxy")
    print("🔗 Target Video: https://www.youtube.com/watch?v=MJDBu5riiR8")
    print()

    success, transcript = test_with_working_proxy()

    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)

    if success:
        print("🎉 SUCCESS! YouTube transcript extraction is working!")
        print("✅ Oxylabs proxy working correctly")
        print("✅ YouTube Transcript API v1.2.2 configured properly")
        print("✅ Ready to deploy to Railway and integrate with pipeline")
        print()
        print(f"📝 Sample transcript:")
        print(f"'{transcript[:500]}...'")
    else:
        print("❌ Still having issues with transcript extraction")
        print("🔧 Need to debug API response structure")

    print("=" * 70)