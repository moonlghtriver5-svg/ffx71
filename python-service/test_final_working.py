#!/usr/bin/env python3
"""
Final working test for YouTube transcript API v1.2.2 with Oxylabs proxy
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

def test_working_version():
    """Test YouTube transcript extraction with correct API v1.2.2 structure"""

    print("🎯 Final Test: YouTube Transcript API v1.2.2 with Oxylabs Proxy")
    print("=" * 70)

    # Configure Oxylabs proxy
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

        # Initialize YouTubeTranscriptApi with proxy
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        print("✅ YouTubeTranscriptApi initialized with Oxylabs proxy")
        print()

        # Test the specific video first
        test_videos = [
            ("MJDBu5riiR8", "User's specific video"),
            ("dQw4w9WgXcQ", "Rick Roll"),
            ("jNQXAC9IVRw", "Me at the zoo"),
        ]

        for video_id, name in test_videos:
            print(f"🎬 Testing: {name}")
            print(f"📺 Video ID: {video_id}")

            try:
                # Method 1: Direct fetch (correct API)
                print("📝 Method 1: Direct fetch...")
                fetched_transcript = ytt_api.fetch(video_id, languages=['en'])

                # FetchedTranscript has a 'snippets' property
                if hasattr(fetched_transcript, 'snippets') and fetched_transcript.snippets:
                    full_transcript = " ".join([snippet.text for snippet in fetched_transcript.snippets])
                    print(f"✅ SUCCESS! Transcript length: {len(full_transcript)} chars")
                    print(f"📄 Preview: {full_transcript[:300]}...")
                    return True, full_transcript
                elif hasattr(fetched_transcript, '__iter__'):
                    # If it's iterable, try to extract text
                    full_transcript = " ".join([item.get('text', '') if hasattr(item, 'get') else str(item) for item in fetched_transcript])
                    if full_transcript.strip():
                        print(f"✅ SUCCESS! Transcript length: {len(full_transcript)} chars")
                        print(f"📄 Preview: {full_transcript[:300]}...")
                        return True, full_transcript

            except Exception as e:
                print(f"❌ Method 1 failed: {str(e)}")

            try:
                # Method 2: List and fetch manually
                print("📝 Method 2: List transcripts and fetch...")
                transcript_list = ytt_api.list(video_id)

                print("📋 Available transcripts:")
                for transcript in transcript_list:
                    print(f"  - {transcript.language} ({transcript.language_code}) - Generated: {transcript.is_generated}")

                    try:
                        # Find first available transcript
                        transcript_data = transcript.fetch()
                        if hasattr(transcript_data, 'snippets') and transcript_data.snippets:
                            full_transcript = " ".join([snippet.text for snippet in transcript_data.snippets])
                            print(f"✅ SUCCESS with {transcript.language}!")
                            print(f"📊 Length: {len(full_transcript)} characters")
                            print(f"📄 Preview: {full_transcript[:300]}...")
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

if __name__ == "__main__":
    print("🚀 Final Test: YouTube Transcript Extraction")
    print("🔗 Target Video: https://www.youtube.com/watch?v=MJDBu5riiR8")
    print()

    # Run the test
    success, transcript = test_working_version()

    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)

    if success:
        print("🎉 SUCCESS! YouTube transcript extraction is working!")
        print("✅ Oxylabs proxy is working correctly")
        print("✅ YouTube Transcript API v1.2.2 is configured properly")
        print("✅ Ready to deploy to Railway and integrate with Next.js")
        print()
        print(f"📝 Sample transcript preview:")
        print(f"'{transcript[:500]}...'")
    else:
        print("❌ Still having issues with transcript extraction")
        print("🔧 May need to investigate further or try different approach")

    print("=" * 70)