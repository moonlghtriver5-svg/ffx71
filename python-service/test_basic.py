#!/usr/bin/env python3
"""
Basic test to verify YouTube transcript API works
"""

import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def test_basic_transcript():
    """Test basic transcript extraction without proxy first"""

    print("🧪 Testing YouTube Transcript API (Basic)")
    print("=" * 60)

    test_videos = [
        ("dQw4w9WgXcQ", "Rick Roll"),
        ("jNQXAC9IVRw", "Me at the zoo"),
        ("9bZkp7q19f0", "Gangnam Style"),
    ]

    for video_id, name in test_videos:
        print(f"\n🎬 Testing: {name}")
        print(f"📺 Video ID: {video_id}")

        try:
            # Basic transcript fetch
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

            if transcript_list:
                # Combine transcript
                full_transcript = " ".join([entry['text'] for entry in transcript_list])

                print(f"✅ SUCCESS! Transcript length: {len(full_transcript)} chars")
                print(f"📄 Preview: {full_transcript[:100]}...")

                return True, full_transcript[:200]

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

    print("\n❌ All videos failed")
    return False, None

def test_with_requests_proxy():
    """Test if we can make basic requests through Oxylabs proxy"""

    print("\n🌐 Testing Oxylabs Proxy Connection")
    print("=" * 60)

    # Oxylabs configuration
    PROXY_HOST = 'pr.oxylabs.io'
    PROXY_PORT = '7777'
    PROXY_USER = 'customer-snowflake_3blLD'
    PROXY_PASS = 'HyperLight23++'

    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    print(f"🔧 Proxy: {PROXY_HOST}:{PROXY_PORT}")
    print(f"👤 User: {PROXY_USER}")

    try:
        # Test basic HTTP request through proxy
        print("📡 Testing HTTP request through proxy...")
        response = requests.get('https://httpbin.org/ip',
                               proxies=proxies,
                               timeout=30)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Proxy works! IP: {data.get('origin', 'unknown')}")
            return True
        else:
            print(f"❌ Proxy failed: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Proxy error: {str(e)}")
        return False

def test_youtube_with_session():
    """Test YouTube transcript with requests session using proxy"""

    print("\n🎥 Testing YouTube with Proxy Session")
    print("=" * 60)

    # Configure proxy
    PROXY_HOST = 'pr.oxylabs.io'
    PROXY_PORT = '7777'
    PROXY_USER = 'customer-snowflake_3blLD'
    PROXY_PASS = 'HyperLight23++'

    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        # Create session with proxy
        session = requests.Session()
        session.proxies.update(proxies)

        # Try to access YouTube directly
        print("📺 Accessing YouTube through proxy...")
        response = session.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                              timeout=30)

        if response.status_code == 200:
            print(f"✅ YouTube access successful! Page size: {len(response.text)} chars")

            # Look for transcript indicators
            if 'transcript' in response.text.lower() or 'caption' in response.text.lower():
                print("🎯 Found transcript/caption references in page")
                return True
            else:
                print("⚠️ No transcript references found, but page loaded")
                return True
        else:
            print(f"❌ YouTube access failed: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ YouTube proxy test error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 YouTube Transcript API Test Suite")
    print("🔗 Repository: https://github.com/jdepoix/youtube-transcript-api")
    print()

    # Test 1: Basic transcript (no proxy)
    basic_success, sample_transcript = test_basic_transcript()

    # Test 2: Proxy connection
    proxy_success = test_with_requests_proxy()

    # Test 3: YouTube with proxy
    youtube_proxy_success = test_youtube_with_session()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"📝 Basic Transcript API: {'✅ WORKS' if basic_success else '❌ FAILS'}")
    print(f"🌐 Oxylabs Proxy: {'✅ WORKS' if proxy_success else '❌ FAILS'}")
    print(f"🎥 YouTube via Proxy: {'✅ WORKS' if youtube_proxy_success else '❌ FAILS'}")
    print()

    if basic_success and proxy_success:
        print("🎉 GOOD NEWS: Basic transcript API works and proxy is functional!")
        print("📋 Next steps:")
        print("1. The youtube-transcript-api package works")
        print("2. The Oxylabs proxy is working")
        print("3. We may need to configure the API to use the proxy differently")
        print("4. Deploy to Railway and test in production environment")

        if sample_transcript:
            print(f"\n📄 Sample transcript preview:")
            print(f"'{sample_transcript}...'")

    elif basic_success:
        print("⚠️ Transcript API works but proxy has issues")
        print("🔧 Consider deploying without proxy first, then debug proxy setup")
    else:
        print("❌ Basic transcript API is not working")
        print("🔍 Need to investigate the youtube-transcript-api package")

    print("=" * 60)