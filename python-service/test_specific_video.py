#!/usr/bin/env python3
"""
Test specific YouTube video for transcript availability
"""

from youtube_transcript_api import YouTubeTranscriptApi
import requests

def test_specific_video():
    """Test the specific video ID"""

    video_id = "MJDBu5riiR8"
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print("🧪 Testing Specific YouTube Video")
    print("=" * 60)
    print(f"🎬 Video URL: {video_url}")
    print(f"📺 Video ID: {video_id}")
    print()

    try:
        # Method 1: Basic get_transcript
        print("📝 Method 1: Basic get_transcript...")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        if transcript_list:
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            print(f"✅ SUCCESS! Transcript extracted")
            print(f"📊 Entries: {len(transcript_list)}")
            print(f"📊 Total length: {len(full_transcript)} characters")
            print(f"🎯 First entry: {transcript_list[0]}")
            print(f"📄 Preview: {full_transcript[:300]}...")
            return True, full_transcript

    except Exception as e:
        print(f"❌ Method 1 failed: {str(e)}")

    try:
        # Method 2: List available transcripts first
        print("\n📝 Method 2: List available transcripts...")
        transcript_list_obj = YouTubeTranscriptApi.list_transcripts(video_id)

        print("📋 Available transcripts:")
        for transcript in transcript_list_obj:
            print(f"  - {transcript.language} ({transcript.language_code})")

            # Try to fetch this transcript
            try:
                transcript_data = transcript.fetch()
                if transcript_data:
                    full_transcript = " ".join([entry['text'] for entry in transcript_data])
                    print(f"✅ SUCCESS with {transcript.language}!")
                    print(f"📊 Length: {len(full_transcript)} characters")
                    print(f"📄 Preview: {full_transcript[:300]}...")
                    return True, full_transcript
            except Exception as fetch_error:
                print(f"   ❌ Failed to fetch {transcript.language}: {str(fetch_error)}")
                continue

    except Exception as e:
        print(f"❌ Method 2 failed: {str(e)}")

    try:
        # Method 3: Try different language codes
        print("\n📝 Method 3: Trying different language codes...")
        languages_to_try = ['en', 'en-US', 'en-GB', 'auto', 'a.en']

        for lang in languages_to_try:
            try:
                print(f"  Trying language: {lang}")
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

                if transcript_list:
                    full_transcript = " ".join([entry['text'] for entry in transcript_list])
                    print(f"✅ SUCCESS with language {lang}!")
                    print(f"📊 Length: {len(full_transcript)} characters")
                    print(f"📄 Preview: {full_transcript[:300]}...")
                    return True, full_transcript

            except Exception as lang_error:
                print(f"   ❌ Language {lang} failed: {str(lang_error)}")
                continue

    except Exception as e:
        print(f"❌ Method 3 failed: {str(e)}")

    print("\n❌ All methods failed to extract transcript")
    return False, None

def check_video_manually():
    """Check the video page manually for transcript indicators"""

    print("\n🔍 Manual Video Page Check")
    print("=" * 60)

    video_url = "https://www.youtube.com/watch?v=MJDBu5riiR8"

    try:
        response = requests.get(video_url, timeout=30)

        if response.status_code == 200:
            content = response.text.lower()

            # Check for transcript/caption indicators
            indicators = [
                'transcript',
                'caption',
                'subtitle',
                '"captions"',
                'captionTracks',
                'transcriptRenderer',
                'showTranscriptText'
            ]

            found_indicators = []
            for indicator in indicators:
                if indicator in content:
                    found_indicators.append(indicator)

            print(f"📄 Page loaded: {len(response.text)} characters")
            print(f"🎯 Transcript indicators found: {found_indicators}")

            # Look for specific patterns
            if 'captionTracks' in content:
                print("✅ Found 'captionTracks' - video likely has captions")

                # Try to extract caption track info
                import re
                caption_match = re.search(r'"captionTracks":\[(.*?)\]', content)
                if caption_match:
                    print(f"📋 Caption data preview: {caption_match.group(1)[:200]}...")

            if len(found_indicators) > 0:
                print("✅ Video appears to have transcript/caption data available")
                return True
            else:
                print("❌ No transcript indicators found in page")
                return False

        else:
            print(f"❌ Failed to load video page: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error checking video page: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Testing Specific YouTube Video for Transcripts")
    print("🔗 Video: https://www.youtube.com/watch?v=MJDBu5riiR8")
    print()

    # Test transcript extraction
    success, transcript = test_specific_video()

    # Manual page check
    has_indicators = check_video_manually()

    # Summary
    print("\n" + "=" * 60)
    print("📊 RESULTS FOR VIDEO MJDBu5riiR8")
    print("=" * 60)
    print(f"📝 Transcript API: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"🔍 Manual Check: {'✅ HAS INDICATORS' if has_indicators else '❌ NO INDICATORS'}")

    if success:
        print("\n🎉 SUCCESS! This video has extractable transcripts!")
        print("✅ Ready to proceed with this approach")
    elif has_indicators:
        print("\n⚠️ Video has transcript data but API can't extract it")
        print("🔧 May need different extraction method or API configuration")
    else:
        print("\n❌ This video doesn't appear to have transcripts")
        print("🔄 Try a different video that definitely has captions/transcripts")

    print("=" * 60)