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

from flask import Blueprint
from app_utils import *
import logging
from services.v1.audio.duration import get_audio_duration, format_duration
from services.authentication import authenticate

v1_audio_duration_bp = Blueprint("v1_audio_duration", __name__)
logger = logging.getLogger(__name__)


@v1_audio_duration_bp.route("/v1/audio/duration", methods=["POST"])
@authenticate
@validate_payload(
    {
        "type": "object",
        "properties": {
            "audio_url": {"type": "string", "format": "uri"},
            "webhook_url": {"type": "string", "format": "uri"},
            "id": {"type": "string"},
        },
        "required": ["audio_url"],
        "additionalProperties": False,
    }
)
@queue_task_wrapper(bypass_queue=True)  # Making it synchronous since it's a quick operation
def get_duration(job_id, data):
    audio_url = data["audio_url"]
    webhook_url = data.get("webhook_url")
    id = data.get("id")

    logger.info(
        f"Job {job_id}: Received audio-duration request for audio file: {audio_url}"
    )

    try:
        duration_sec, duration_ms = get_audio_duration(audio_url, job_id)
        logger.info(f"Job {job_id}: Audio duration retrieval completed successfully")

        response = {
            "duration": duration_sec,
            "duration_ms": duration_ms,
            "duration_formatted": format_duration(duration_sec)
        }

        return response, "/v1/audio/duration", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error during audio duration retrieval - {str(e)}")
        return str(e), "/v1/audio/duration", 500 