#!/usr/bin/env python3
"""
Simple test to verify YouTube transcript API works with Oxylabs proxy
"""

import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

def test_transcript_extraction():
    """Test basic transcript extraction"""

    print("🧪 Testing YouTube Transcript API with Oxylabs Proxy")
    print("=" * 60)

    # Configure Oxylabs proxy
    OXYLABS_HOST = 'pr.oxylabs.io'
    OXYLABS_PORT = '7777'
    OXYLABS_USERNAME = 'customer-snowflake_3blLD'
    OXYLABS_PASSWORD = 'HyperLight23++'

    proxy_url = f"http://{OXYLABS_USERNAME}:{OXYLABS_PASSWORD}@{OXYLABS_HOST}:{OXYLABS_PORT}"

    print(f"🌐 Proxy: {OXYLABS_HOST}:{OXYLABS_PORT}")
    print(f"👤 Username: {OXYLABS_USERNAME}")
    print()

    try:
        # Create proxy configuration
        proxy_config = GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

        print("🔧 Proxy configuration created")

        # Test video IDs
        test_videos = [
            ("dQw4w9WgXcQ", "Rick Roll (known to have transcripts)"),
            ("jNQXAC9IVRw", "Me at the zoo (first YouTube video)"),
            ("9bZkp7q19f0", "PSY - Gangnam Style"),
        ]

        for video_id, description in test_videos:
            print(f"\n🎬 Testing: {description}")
            print(f"📺 Video ID: {video_id}")

            try:
                # Initialize API with proxy
                ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

                # Fetch transcript
                print("📝 Fetching transcript...")
                transcript_list = ytt_api.fetch(video_id, languages=['en'])

                if transcript_list:
                    # Combine transcript entries
                    full_transcript = " ".join([entry['text'] for entry in transcript_list])

                    print(f"✅ SUCCESS! Transcript extracted")
                    print(f"📊 Length: {len(full_transcript)} characters")
                    print(f"📄 Preview: {full_transcript[:150]}...")

                    return True

                else:
                    print("❌ No transcript found")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                continue

        print("\n❌ All test videos failed")
        return False

    except Exception as e:
        print(f"❌ Setup error: {str(e)}")
        return False

def test_without_proxy():
    """Test without proxy for comparison"""

    print("\n🔄 Testing WITHOUT proxy (for comparison)")
    print("=" * 60)

    try:
        # Test without proxy
        ytt_api = YouTubeTranscriptApi()

        video_id = "dQw4w9WgXcQ"
        print(f"🎬 Testing video: {video_id}")

        transcript_list = ytt_api.fetch(video_id, languages=['en'])

        if transcript_list:
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            print(f"✅ SUCCESS without proxy! Length: {len(full_transcript)} characters")
            return True
        else:
            print("❌ No transcript found")
            return False

    except Exception as e:
        print(f"❌ Error without proxy: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 YouTube Transcript API Test")
    print("🔗 Repository: https://github.com/jdepoix/youtube-transcript-api")
    print()

    # Test with proxy
    proxy_success = test_transcript_extraction()

    # Test without proxy for comparison
    no_proxy_success = test_without_proxy()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"🌐 With Oxylabs Proxy: {'✅ PASS' if proxy_success else '❌ FAIL'}")
    print(f"🔄 Without Proxy: {'✅ PASS' if no_proxy_success else '❌ FAIL'}")
    print()

    if proxy_success:
        print("🎉 SUCCESS! The YouTube transcript API works with Oxylabs proxy!")
        print("✅ Ready to proceed with Railway deployment")
    elif no_proxy_success:
        print("⚠️ API works without proxy but fails with proxy")
        print("🔧 May need to adjust proxy configuration")
    else:
        print("❌ API not working - check network/configuration")

    print("=" * 60)