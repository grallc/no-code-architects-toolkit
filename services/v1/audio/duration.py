# Copyright (c) 2025 Stephen G. Pope
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.



import os
import ffmpeg
from services.file_management import download_file
from config import LOCAL_STORAGE_PATH

def get_audio_duration(audio_url, job_id):
    """Get the duration of an audio file in seconds."""
    try:
        # Download the audio file
        input_filename = download_file(audio_url, os.path.join(LOCAL_STORAGE_PATH, f"{job_id}_input"))
        
        # Get duration using ffprobe (part of ffmpeg)
        probe = ffmpeg.probe(input_filename)
        duration = float(probe['format']['duration'])
        
        # Clean up the downloaded file
        os.remove(input_filename)
        
        print(f"Audio duration successfully retrieved: {duration} seconds")
        
        # Also return milliseconds
        duration_ms = int(duration * 1000)
        
        return duration, duration_ms
    except Exception as e:
        print(f"Audio duration retrieval failed: {str(e)}")
        raise

def format_duration(seconds):
    """Format the duration in seconds to HH:MM:SS format."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" 