"""
Enhanced Marriage Coaching Sales Call Analyzer
Surgical analysis for marriage coaching sales with empathetic confrontation tracking
"""

import json
import os
import asyncio
from datetime import datetime
import logging
import time
import re
import hashlib
from http.server import BaseHTTPRequestHandler

try:
    from anthropic import AsyncAnthropic, APIError, RateLimitError, APITimeoutError
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_vtt_content(content):
    """
    Parse VTT (WebVTT) format and convert to timestamped text.

    VTT format example:
    WEBVTT

    00:00:01.000 --> 00:00:03.500
    John: Hi, thanks for joining!

    Returns formatted text with timestamps preserved for temporal analysis.
    """
    # Check if this is VTT content (case insensitive, allow whitespace)
    if not content.strip().upper().startswith('WEBVTT'):
        # Not a VTT file, return as-is
        logger.info("Not VTT format - processing as plain text")
        return content, False

    logger.info("Detected VTT format - parsing with timestamp preservation")
    logger.info(f"Original content length: {len(content)} characters")

    # Split by newlines first
    lines = content.split('\n')

    formatted_lines = []
    current_timestamp = None
    current_text_lines = []
    total_duration = None

    # More flexible timestamp pattern (handles various VTT formats)
    timestamp_pattern = r'(\d{1,2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[.,]\d{3})'

    for line in lines:
        line = line.strip()

        # Skip empty lines, WEBVTT header, and numeric cue identifiers
        if not line or line.upper().startswith('WEBVTT') or line.isdigit():
            # If we have accumulated text, save it
            if current_timestamp and current_text_lines:
                text = ' '.join(current_text_lines)
                if text:
                    formatted_lines.append(f"[{current_timestamp}] {text}")
                current_text_lines = []
            continue

        # Check if this is a timestamp line
        timestamp_match = re.match(timestamp_pattern, line)
        if timestamp_match:
            # Save previous segment if exists
            if current_timestamp and current_text_lines:
                text = ' '.join(current_text_lines)
                if text:
                    formatted_lines.append(f"[{current_timestamp}] {text}")

            # Start new segment
            start_time = timestamp_match.group(1).replace(',', '.')
            end_time = timestamp_match.group(2).replace(',', '.')
            current_timestamp = convert_timestamp_to_simple(start_time)
            total_duration = end_time
            current_text_lines = []
        else:
            # This is text content
            if line and not line.startswith('NOTE'):  # Skip VTT NOTE lines
                current_text_lines.append(line)

    # Don't forget the last segment
    if current_timestamp and current_text_lines:
        text = ' '.join(current_text_lines)
        if text:
            formatted_lines.append(f"[{current_timestamp}] {text}")

    formatted_text = '\n'.join(formatted_lines)

    logger.info(f"VTT parsed: {len(formatted_lines)} timestamped segments")
    logger.info(f"Formatted text length: {len(formatted_text)} characters")
    if total_duration:
        logger.info(f"Call duration: {convert_timestamp_to_simple(total_duration)}")

    # If parsing failed, return original content
    if len(formatted_lines) == 0:
        logger.warning("VTT parsing produced no output - returning original content")
        return content, False

    return formatted_text, True

def convert_timestamp_to_simple(timestamp):
    """Convert 00:00:01.000 to 00:01 (MM:SS format)"""
    try:
        parts = timestamp.split(':')
        if len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            # Handle both . and , as decimal separator
            seconds_part = parts[2].replace(',', '.')
            seconds = int(float(seconds_part))

            total_minutes = hours * 60 + minutes
            return f"{total_minutes:02d}:{seconds:02d}"
    except (ValueError, IndexError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp}': {e}")
    return timestamp

class MarriageCoachingAnalyzer:
    """Surgical marriage coaching sales analyzer with framework from proven systems"""

    def __init__(self, api_key, max_retries=3, timeout=120):
        self.client = AsyncAnthropic(api_key=api_key, timeout=timeout)
        # Model configuration - easy to update when models change
        self.model = "claude-sonnet-4-5"  # Upgraded to Claude Sonnet 4.5 (latest)
        self.max_retries = max_retries
        self.timeout = timeout

        # Marriage Reset package definitions
        self.packages = {
            'MRL': {'name': 'Marriage Reset Light', 'price': 2300, 'description': 'Self-paced course'},
            'MRS': {'name': 'Marriage Reset Standard', 'price': None, 'description': 'Course + 2 coaching calls + weekly group'},
            'MRP': {'name': 'Marriage Reset Plus', 'price': None, 'description': 'Course + 5 coaching sessions + weekly group'},
            'MRI': {'name': 'Marriage Reset Intensive', 'price': 11800, 'description': 'Course + 16 coaching sessions + weekly group'}
        }

    async def _call_api_with_retry(self, prompt, max_tokens, operation_name="API call"):
        """
        Make API call with exponential backoff retry logic

        Args:
            prompt: The prompt to send to Claude
            max_tokens: Maximum tokens for response
            operation_name: Name of the operation for logging

        Returns:
            API response text

        Raises:
            Exception: If all retries fail
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                logger.info(f"{operation_name} - Attempt {attempt + 1}/{self.max_retries}")

                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.3,  # Low temperature for consistent, deterministic scoring
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = response.content[0].text.strip()
                logger.info(f"{operation_name} - Success on attempt {attempt + 1}")
                return response_text

            except RateLimitError as e:
                last_error = e
                wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                logger.warning(f"{operation_name} - Rate limit hit on attempt {attempt + 1}. Waiting {wait_time}s before retry...")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{operation_name} - Rate limit exceeded after {self.max_retries} attempts")

            except APITimeoutError as e:
                last_error = e
                logger.warning(f"{operation_name} - Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{operation_name} - Timeout after {self.max_retries} attempts")

            except APIError as e:
                last_error = e
                error_code = getattr(e, 'status_code', 'unknown')
                logger.warning(f"{operation_name} - API error ({error_code}) on attempt {attempt + 1}: {str(e)}")

                # Don't retry on client errors (4xx), only server errors (5xx)
                if error_code and str(error_code).startswith('4'):
                    logger.error(f"{operation_name} - Client error, not retrying")
                    raise

                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{operation_name} - API error persisted after {self.max_retries} attempts")

            except Exception as e:
                last_error = e
                logger.error(f"{operation_name} - Unexpected error on attempt {attempt + 1}: {type(e).__name__}: {str(e)}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{operation_name} - Failed after {self.max_retries} attempts")

        # If we get here, all retries failed
        raise Exception(f"{operation_name} failed after {self.max_retries} attempts: {str(last_error)}")

    async def detect_call_outcome(self, content):
        """
        Detect if call was won/lost and identify which package was discussed/purchased.
        Specific to Marriage Reset methodology with early price positioning.
        """
        prompt = f"""Analyze this marriage coaching sales call to determine the outcome and packages discussed.

TRANSCRIPT:
{content}

PACKAGE INFORMATION:
- MRL (Marriage Reset Light): $2,300 self-paced course
- MRS (Marriage Reset Standard): Course + 2 coaching calls + weekly group
- MRP (Marriage Reset Plus): Course + 5 coaching sessions + weekly group
- MRI (Marriage Reset Intensive): $11,800 - Course + 16 coaching sessions + weekly group

IMPORTANT: Look for explicit purchase signals like:
- "I want to get started"
- "Let's do it" / "I'm in"
- "How do I sign up" / "What's the next step"
- "I'll do the [package name]"
- Discussion of payment plans, credit cards, signing up
- Scheduling first coaching call
- Rep saying "welcome to the program" or similar

CALL WON = Clear commitment to purchase (even if paying later)
CALL LOST = No commitment, "I need to think about it", "talk to my wife", objections not overcome

Return ONLY this JSON:
{{
  "call_outcome": "won" or "lost" or "undetermined",
  "confidence": 0.85,
  "packages_positioned": ["MRL", "MRI"],
  "package_purchased": "MRI" or null,
  "purchase_timestamp": "[35:20]" or null,
  "closing_moment_analysis": {{
    "decision_point_timestamp": "[35:20]",
    "prospect_buying_signals": ["Said 'I need this'", "Asked about payment"],
    "rep_closing_approach": "Assumptive close after addressing wife objection",
    "objections_raised": ["Need to talk to wife", "Concerned about cost"],
    "objections_handled": true,
    "final_commitment_language": "Prospect said 'let's do the intensive'"
  }},
  "why_won_or_lost": "Clear analysis of what led to outcome",
  "key_closing_moments": [
    "[33:15] Prospect showed strong buying signal - 'this makes so much sense'",
    "[35:20] Rep handled wife objection perfectly",
    "[36:45] Prospect committed to MRI package"
  ]
}}

Be PRECISE - only mark as "won" if there's clear commitment. "I'll think about it" = lost."""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=1500,
                operation_name="Call Outcome Detection"
            )

            # Clean and extract JSON
            response_text = response_text.replace('```json', '').replace('```', '').strip()

            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            # Add package details
            if result.get('package_purchased'):
                package_code = result['package_purchased']
                if package_code in self.packages:
                    result['package_details'] = self.packages[package_code]

            logger.info(f"Call outcome: {result.get('call_outcome')} - Package: {result.get('package_purchased')}")
            return result

        except Exception as e:
            logger.error(f"Call outcome detection error: {str(e)}")
            # Return safe fallback
            return {
                'call_outcome': 'undetermined',
                'confidence': 0.0,
                'packages_positioned': [],
                'package_purchased': None,
                'purchase_timestamp': None,
                'why_won_or_lost': 'Analysis failed - could not determine outcome',
                'key_closing_moments': []
            }

    async def detect_discovery_quality(self, content):
        """
        Phase 2: Discovery Quality Tracking
        Detects "switching gears" transition and tracks the 4 key questions.
        """
        prompt = f"""Analyze this marriage coaching sales call to evaluate discovery quality.

TRANSCRIPT:
{content}

MARRIAGE RESET DISCOVERY FRAMEWORK:

1. **TRANSITION DETECTION**: Look for the "switching gears" keyword or similar transition phrases like:
   - "Let me switch gears"
   - "I want to shift gears"
   - "Let's transition to"
   - "Now I want to move into"

2. **THE 4 KEY QUESTIONS**: After switching gears, rep should ask these 4 questions:
   a) "Do you feel like you're a priority to your husband?"
   b) "Do you feel like your husband understands what you need?"
   c) "Can you trust him?"
   d) "Do you feel emotionally secure in the marriage?"

3. **CONFLICT HANDLING**: Later, rep should ask:
   - "How do you handle conflict?"
   - "What happens when you disagree?"

IMPORTANT: Provide EXACT timestamps for all findings. Mark questions as asked ONLY if clearly present.

Return ONLY this JSON:
{{
  "switching_gears_detected": {{
    "found": true,
    "timestamp": "[12:45]",
    "exact_phrase": "Let me switch gears here",
    "transition_quality": "smooth|abrupt|missing",
    "context": "Rep transitioned after building rapport"
  }},
  "four_key_questions": {{
    "priority_question": {{
      "asked": true,
      "timestamp": "[13:20]",
      "prospect_response_summary": "Said she doesn't feel like a priority",
      "rep_follow_up": "Rep dug deeper into specific examples",
      "emotional_intensity": 8
    }},
    "understanding_question": {{
      "asked": true,
      "timestamp": "[15:45]",
      "prospect_response_summary": "Feels husband doesn't understand her needs",
      "rep_follow_up": "Rep asked for clarification",
      "emotional_intensity": 7
    }},
    "trust_question": {{
      "asked": false,
      "timestamp": null,
      "missed_opportunity": "[16:30] Prospect mentioned broken promises - perfect moment to ask about trust",
      "impact_of_missing": "Missed critical trust issue that affects close probability"
    }},
    "emotional_security_question": {{
      "asked": true,
      "timestamp": "[18:10]",
      "prospect_response_summary": "Feels anxious and uncertain",
      "rep_follow_up": "Rep validated feelings",
      "emotional_intensity": 9
    }}
  }},
  "conflict_handling": {{
    "asked": true,
    "timestamp": "[20:15]",
    "prospect_response_summary": "They avoid conflict, which makes things worse",
    "conflict_pattern_identified": "Avoidance pattern leading to resentment",
    "rep_coaching_response": "Rep explained how avoidance compounds problems"
  }},
  "discovery_quality_summary": {{
    "questions_asked_count": 3,
    "questions_missed_count": 1,
    "completion_percentage": 75,
    "discovery_depth_score": 7,
    "key_insights_uncovered": [
      "Prospect feels deprioritized",
      "Communication breakdown present",
      "High emotional intensity around security"
    ],
    "missed_opportunities": [
      "Trust question not asked despite broken promises mention",
      "Could have probed deeper on priority issue"
    ],
    "coaching_prescription": "Practice all 4 questions until they become second nature. Trust question critical for close."
  }}
}}

Be PRECISE with timestamps. Only mark as asked if the question is clearly present."""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=2000,
                operation_name="Discovery Quality Detection"
            )

            # Clean and extract JSON
            response_text = response_text.replace('```json', '').replace('```', '').strip()

            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            logger.info(f"Discovery quality: {result.get('discovery_quality_summary', {}).get('questions_asked_count', 0)}/4 key questions asked")
            return result

        except Exception as e:
            logger.error(f"Discovery quality detection error: {str(e)}")
            # Return safe fallback
            return {
                'switching_gears_detected': {
                    'found': False,
                    'transition_quality': 'undetermined'
                },
                'four_key_questions': {
                    'priority_question': {'asked': False},
                    'understanding_question': {'asked': False},
                    'trust_question': {'asked': False},
                    'emotional_security_question': {'asked': False}
                },
                'conflict_handling': {'asked': False},
                'discovery_quality_summary': {
                    'questions_asked_count': 0,
                    'questions_missed_count': 4,
                    'completion_percentage': 0,
                    'discovery_depth_score': 1,
                    'key_insights_uncovered': [],
                    'missed_opportunities': ['Analysis failed - could not determine discovery quality'],
                    'coaching_prescription': 'Review recording manually'
                }
            }

    async def analyze_marriage_coaching_call(self, content, filename="transcript.txt", client_name=None, closer_name=None, zoom_meeting_id=None, call_date=None):
        """Complete marriage coaching sales analysis with VTT support"""

        try:
            # Parse VTT format if detected
            content, is_vtt = parse_vtt_content(content)

            logger.info(f"Content length after VTT parsing: {len(content)} characters")

            # Generate content hash for consistency tracking
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            logger.info(f"Content hash: {content_hash} - Use this to identify duplicate analyses")

            # Increased limit to handle full sales calls (45-60 min calls = ~50k chars)
            # Claude can handle up to ~200k tokens (~800k characters)
            if len(content) > 100000:
                logger.warning(f"Content very long ({len(content)} chars), truncating to 100k")
                content = content[:100000] + "\n\n... [Content truncated for analysis - call exceeded 100k characters]"

            # Detect call outcome and packages first
            call_outcome = await self.detect_call_outcome(content)

            # Phase 2: Detect discovery quality
            discovery_quality = await self.detect_discovery_quality(content)

            # Run comprehensive analysis (pass discovery quality to enhance framework scoring)
            sales_framework_analysis = await self.analyze_sales_framework(content, discovery_quality)
            psychological_analysis = await self.analyze_psychological_profile(content)
            marriage_specific_analysis = await self.analyze_marriage_coaching_specifics(content)
            emotional_journey = await self.analyze_emotional_journey(content)
            archetype_classification = await self.classify_marriage_archetype(content)
            talk_track_improvements = await self.analyze_talk_track_improvements(content, sales_framework_analysis, marriage_specific_analysis)

            # Calculate success probability
            success_probability = self.calculate_marriage_success_probability(
                sales_framework_analysis, marriage_specific_analysis, archetype_classification
            )

            # Determine coaching urgency (75% threshold)
            coaching_assessment = self.determine_coaching_urgency(success_probability)

            # Extract participant names if not provided
            if not client_name or not closer_name:
                extracted_names = self.extract_participant_names(content)
                client_name = client_name or extracted_names.get('client_name')
                closer_name = closer_name or extracted_names.get('closer_name')

            return {
                'transcript_id': filename,
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'success',
                'word_count': len(content.split()),

                # Call metadata
                'call_metadata': {
                    'client_name': client_name,
                    'closer_name': closer_name,
                    'zoom_meeting_id': zoom_meeting_id,
                    'call_date': call_date or datetime.now().strftime('%Y-%m-%d'),
                    'analysis_timestamp': datetime.now().isoformat()
                },

                # Call outcome (Phase 1 feature)
                'call_outcome': call_outcome,

                # Discovery quality (Phase 2 feature)
                'discovery_quality': discovery_quality,

                # Core analyses
                'sales_framework_analysis': sales_framework_analysis,
                'psychological_profile': psychological_analysis,
                'marriage_coaching_analysis': marriage_specific_analysis,
                'emotional_journey': emotional_journey,
                'archetype_analysis': archetype_classification,
                'talk_track_improvements': talk_track_improvements,

                # Calculated metrics
                'success_probability': success_probability,
                'coaching_assessment': coaching_assessment
            }

        except Exception as e:
            logger.error(f"Marriage coaching analysis failed: {str(e)}")
            return {
                'transcript_id': filename,
                'status': 'error',
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }

    async def analyze_sales_framework(self, content, discovery_quality=None):
        """Apply the proven 7-category sales framework with temporal analysis"""

        # Build discovery quality context for enhanced scoring
        discovery_context = ""
        if discovery_quality:
            summary = discovery_quality.get('discovery_quality_summary', {})
            questions_asked = summary.get('questions_asked_count', 0)
            discovery_context = f"""

DISCOVERY QUALITY DATA (Phase 2):
- Switching gears transition: {discovery_quality.get('switching_gears_detected', {}).get('found', False)}
- Key questions asked: {questions_asked}/4
- Discovery completion: {summary.get('completion_percentage', 0)}%
- Discovery depth score from Phase 2: {summary.get('discovery_depth_score', 5)}/10

Use this data to inform your discovery_depth category score. If Phase 2 shows strong discovery (3-4 questions asked), score should be 7-10. If weak (0-1 questions), score should be 1-4."""

        prompt = f"""Analyze this marriage coaching sales call and rate performance in 7 categories using the STRICT SCORING RUBRIC below.

IMPORTANT: Transcript may include timestamps in [MM:SS] format. Use timestamps to provide PRECISE coaching feedback with exact moments to review.

SCORING RUBRIC (use these exact criteria for consistency):
- 9-10: Exceptional - Demonstrates mastery, multiple strong examples
- 7-8: Good - Solid performance, few minor improvements needed
- 5-6: Average - Adequate but significant room for improvement
- 3-4: Below Average - Major gaps, needs immediate coaching
- 1-2: Poor - Critical failures, requires urgent intervention
{discovery_context}

TRANSCRIPT:
{content}

Rate each category 1-10 using the rubric above. Be CONSISTENT - same quality should get same score.

CRITICAL: For "relationship_dynamics_education" - ONLY flag MISSED opportunities when:
1. Prospect's story REVEALS a dynamic (e.g., describes shutting down when husband yells)
2. Rep did NOT teach the principle in that moment
3. Teaching would have been contextually appropriate (not over-educating)

Core principles to watch for:
- Emotion-first processing: Wife feels what husband says before processing the words
- Emotional priming: Tone/demeanor sets receptivity for what follows (door-slamming vs. whistling example)
- Defensive triggers: How emotional state colors interpretation of words
- Communication patterns: How small interactions compound over time

High score (8-10): Rep identifies dynamics in prospect's story and teaches principles at perfect moments
Low score (1-4): Rep misses multiple clear teaching opportunities when prospect reveals dynamics

{{
  "framework_scores": {{
    "call_control": {{
      "score": 7,
      "analysis": "Rep maintained good conversation flow",
      "coaching_fix": "Ask more guiding questions",
      "key_moments": ["[12:30] Lost control when prospect went off-topic", "[25:15] Good redirect back to solution"]
    }},
    "discovery_depth": {{
      "score": 5,
      "analysis": "Surface-level problem identification",
      "coaching_fix": "Dig deeper into marriage pain points",
      "key_moments": ["[08:45] Missed opportunity to explore emotional impact", "[15:20] Good probing question"]
    }},
    "empathetic_confrontation": {{
      "score": 6,
      "analysis": "Showed empathy but missed confrontation opportunities",
      "coaching_fix": "Balance understanding with accountability",
      "key_moments": ["[18:30] Too much empathy, avoided confrontation", "[22:10] Missed chance to show prospect his role"]
    }},
    "objection_handling": {{
      "score": 4,
      "analysis": "Struggled with price objections",
      "coaching_fix": "Use investment reframes not cost justification",
      "key_moments": ["[28:45] Price objection handled poorly - justified instead of reframed"]
    }},
    "value_positioning": {{
      "score": 3,
      "analysis": "Weak marriage value positioning",
      "coaching_fix": "Position marriage as most important investment",
      "key_moments": ["[20:15] Weak value statement - sounded like expense not investment"]
    }},
    "closing_strength": {{
      "score": 2,
      "analysis": "No clear commitment requests",
      "coaching_fix": "Use assumptive close techniques",
      "key_moments": ["[32:40] CRITICAL MISS - Client showed buying signal but rep didn't close"]
    }},
    "relationship_dynamics_education": {{
      "score": 4,
      "analysis": "Rep missed opportunities to teach core relationship principles when prospect's story revealed them",
      "coaching_fix": "Identify when prospect describes dynamics, then teach the principle briefly without over-educating",
      "key_moments": ["[15:45] MISSED - Prospect said 'he yelled and I shut down' - perfect moment to explain emotion-first processing", "[22:10] MISSED - Prospect described communication breakdown - could have taught how tone sets receptivity"],
      "missed_teaching_opportunities": [
        {{"principle": "Emotion-first processing (wife feels before she hears)", "context": "Prospect described defensive reaction to husband's tone", "timestamp": "[15:45]"}},
        {{"principle": "Emotional priming (tone sets receptivity)", "context": "Prospect said arguments escalate from how conversation starts", "timestamp": "[22:10]"}}
      ]
    }}
  }},
  "total_score": 31,
  "overall_grade": "C"
}}

Respond with ONLY valid JSON matching this format."""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=3500,
                operation_name="Sales Framework Analysis"
            )

            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Sales framework analysis error after retries: {str(e)}")
            return self.get_fallback_sales_framework()

    async def analyze_psychological_profile(self, content):
        """Big Five personality analysis for marriage coaching prospects"""

        prompt = f"""Analyze this prospect's personality from the marriage coaching call.

TRANSCRIPT:
{content}

Rate their Big Five personality traits (1-100):

{{
  "big_five_personality": {{
    "openness": {{
      "score": 75,
      "confidence": 80,
      "implications": "Open to new approaches for marriage improvement"
    }},
    "conscientiousness": {{
      "score": 60,
      "confidence": 85,
      "implications": "Moderate follow-through likelihood"
    }},
    "extraversion": {{
      "score": 45,
      "confidence": 75,
      "implications": "Introverted communication style"
    }},
    "agreeableness": {{
      "score": 70,
      "confidence": 85,
      "implications": "Cooperative but conflict-avoidant"
    }},
    "neuroticism": {{
      "score": 65,
      "confidence": 80,
      "implications": "Moderate stress about marriage situation"
    }}
  }},
  "decision_making_style": {{
    "primary_style": "emotional",
    "confidence": 85
  }},
  "emotional_state": {{
    "primary_emotion": "anxious",
    "intensity": 7,
    "stability": 5
  }}
}}

Respond with ONLY valid JSON matching this format."""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=2000,
                operation_name="Psychological Profile Analysis"
            )

            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Psychological analysis error after retries: {str(e)}")
            return self.get_fallback_psychological_analysis()

    async def analyze_marriage_coaching_specifics(self, content):
        """Marriage coaching specific analysis"""

        prompt = f"""
        Analyze this marriage coaching sales call for marriage-specific elements and coaching effectiveness.

        IMPORTANT: Transcript may include timestamps in [MM:SS] format. Include timestamps in ALL coaching feedback for precise review moments.

        TRANSCRIPT:
        {content}

        Focus on marriage coaching specifics:

        {{
          "marriage_coaching_elements": {{
            "listening_with_intent": {{
              "information_gathering_score": 1-10,
              "information_callback_score": 1-10,
              "examples_of_good_listening": ["quotes where rep used earlier info later"],
              "missed_callback_opportunities": ["info given early that wasn't used later"],
              "coaching_prescription": "How to improve listening and callback usage"
            }},
            "empathy_vs_confrontation_balance": {{
              "empathy_score": 1-10,
              "confrontation_score": 1-10,
              "balance_effectiveness": 1-10,
              "empathy_examples": ["quotes showing good empathy"],
              "confrontation_examples": ["quotes showing prospect his role in problems"],
              "missed_confrontation_opportunities": ["moments to show prospect his shortcomings"],
              "coaching_improvement": "Better balance techniques"
            }},
            "value_vs_price_analysis": {{
              "marriage_value_positioning": {{
                "score": 1-10,
                "effective_positioning": ["quotes positioning marriage as valuable"],
                "missed_positioning": ["opportunities to reinforce marriage value"],
                "tesla_analogy_usage": {{ "used": true/false, "effectiveness": 1-10, "context": "how it was used" }},
                "beg_borrow_steal_positioning": {{ "used": true/false, "effectiveness": 1-10, "improvement": "how to use this better" }}
              }},
              "investment_vs_expense_framing": {{
                "score": 1-10,
                "effective_framing": ["quotes framing as investment"],
                "expense_framing_mistakes": ["quotes that made it sound like expense"],
                "coaching_improvement": "Better investment framing scripts"
              }}
            }},
            "marriage_analogies_effectiveness": {{
              "analogies_used": {{
                "garden_analogy": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "relationship needs tending like a garden",
                  "prospect_response": "how prospect reacted to this analogy",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "how to use this analogy better"
                }},
                "bucket_emotional_flexseal": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "emotional holes need repair like bucket with flexseal",
                  "prospect_response": "emotional connection created",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "better application of this analogy"
                }},
                "sediment_analogy": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "relationship problems build up like sediment",
                  "prospect_response": "understanding of problem accumulation",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "more effective sediment positioning"
                }},
                "tipping_scale": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "marriage problems vs solutions on tipping scale",
                  "prospect_response": "urgency created about tipping point",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "better scale positioning"
                }},
                "couch_analogy": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "comfort zone keeping prospect from action",
                  "prospect_response": "recognition of comfort zone trap",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "more effective comfort zone challenge"
                }},
                "razor_analogy": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "sharp precision needed in marriage repair",
                  "prospect_response": "understanding need for precision",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "sharper analogy delivery"
                }},
                "road_trip": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "marriage journey like planned road trip",
                  "prospect_response": "connection to journey concept",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "better journey positioning"
                }},
                "reading_smoke": {{
                  "used": true/false,
                  "effectiveness": 1-10,
                  "context": "marriage warning signs like reading smoke",
                  "prospect_response": "recognition of warning signs",
                  "timing_in_call": "opening|discovery|presentation|closing",
                  "improvement_note": "more effective warning positioning"
                }}
              }},
              "analogy_strategy_analysis": {{
                "total_analogies_used": "count of analogies used",
                "most_effective_analogy": "which analogy resonated most",
                "analogy_timing_effectiveness": "early|mid|late - when analogies worked best",
                "prospect_analogy_preference": "which type of analogies this prospect responds to",
                "overuse_warning": "if too many analogies confused the prospect"
              }},
              "analogy_recommendations": {{
                "best_analogy_for_this_prospect": "which specific analogy would work best and why based on their situation",
                "optimal_analogy_timing": "when in conversation to introduce analogies for maximum impact",
                "missed_analogy_opportunities": ["specific moments where analogies could have created breakthrough"],
                "next_call_analogy_strategy": "which analogies to use in follow-up based on analysis"
              }}
            }}
          }},
          "marriage_situation_assessment": {{
            "relationship_status": "same_house_same_bed|same_house_separate_rooms|separated|unclear",
            "urgency_level": 1-10,
            "emotional_state": "desperate|hopeful|angry|resigned|confused",
            "wife_involvement": "supportive|neutral|resistant|unknown",
            "timeline_pressure": "immediate|weeks|months|no_pressure",
            "financial_capability": {{ "assessed": true/false, "ability": "high|medium|low|unknown", "objections": ["financial concerns raised"] }}
          }},
          "coaching_triggers": {{
            "critical_intervention_needed": {{
              "high_probability_miss": {{
                "triggered": true/false,
                "severity": "low|medium|high|critical",
                "specific_reasons": ["prospect showed high interest but rep didn't close", "buying signals missed", "emotional peak not leveraged"],
                "missed_closing_opportunities": ["specific moments where rep should have asked for commitment"],
                "immediate_coaching_action": "what sales manager needs to address RIGHT NOW"
              }},
              "empathy_confrontation_imbalance": {{
                "triggered": true/false,
                "imbalance_type": "too_much_empathy|too_much_confrontation|no_confrontation",
                "severity": "low|medium|high|critical",
                "specific_examples": ["quotes showing the imbalance"],
                "impact_on_sale": "how this imbalance hurt the sales process",
                "coaching_correction": "specific script/technique to fix this immediately"
              }},
              "value_positioning_catastrophe": {{
                "triggered": true/false,
                "severity": "low|medium|high|critical",
                "positioning_failures": ["made coaching sound like expense", "didn't show marriage value", "weak ROI positioning"],
                "prospect_price_objections": ["specific price concerns that weren't handled"],
                "emergency_value_scripts": ["scripts rep needs to learn before next call"]
              }},
              "listening_and_discovery_failure": {{
                "triggered": true/false,
                "severity": "low|medium|high|critical",
                "information_missed": ["critical info prospect gave that wasn't used"],
                "callback_failures": ["early info that should have been referenced later"],
                "discovery_gaps": ["essential marriage situation info not gathered"],
                "coaching_intervention": "immediate discovery training needed"
              }},
              "emotional_mismanagement": {{
                "triggered": true/false,
                "severity": "low|medium|high|critical",
                "emotional_mistakes": ["misread emotional state", "responded poorly to emotion", "created negative emotion"],
                "missed_emotional_leverage": ["emotional peaks not used for closing"],
                "emotional_coaching_needed": "specific emotional intelligence training required"
              }},
              "analogy_and_story_failure": {{
                "triggered": true/false,
                "severity": "low|medium|high|critical",
                "missed_story_opportunities": ["moments where analogies could have created breakthrough"],
                "poor_analogy_execution": ["analogies used poorly or at wrong time"],
                "story_coaching_priority": "which analogies rep needs to master first"
              }}
            }},
            "coaching_urgency_assessment": {{
              "immediate_coaching_required": true/false,
              "coaching_priority_level": "low|medium|high|emergency",
              "total_critical_triggers": "count of critical issues",
              "rep_competency_concern": "is this rep capable of closing marriage coaching sales",
              "recommended_coaching_timeline": "immediate|within_24hrs|this_week|ongoing"
            }},
            "manager_intervention_recommendations": {{
              "should_manager_jump_on_next_call": true/false,
              "rep_needs_shadowing": true/false,
              "script_drilling_required": ["specific scripts rep must practice"],
              "role_play_scenarios": ["situations rep needs to practice before next call"],
              "performance_improvement_plan_trigger": true/false
            }}
          }}
        }}

        Be savage and specific about marriage coaching techniques. This analysis determines if this rep can save marriages.

        Respond with ONLY the JSON object.
        """

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=3500,
                operation_name="Marriage Coaching Specifics Analysis"
            )

            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Marriage coaching analysis error after retries: {str(e)}")
            return self.get_fallback_marriage_analysis()

    async def analyze_emotional_journey(self, content):
        """Track emotional journey throughout the call using Claude Sonnet 4.5"""

        # Use shorter content for reliable analysis
        content_preview = content[:3000] if len(content) > 3000 else content
        logger.info(f"AI emotional journey analysis for content length: {len(content_preview)}")

        prompt = f"""You are an expert marriage coaching psychologist. Map the prospect's emotional journey through this sales call.

IMPORTANT: Transcript may include timestamps in [MM:SS] format. Use timestamps to track WHEN emotional shifts occur.

TRANSCRIPT:
{content_preview}

Track their emotional progression through 4 phases with PRECISE timestamps:

Return ONLY this JSON:
{{
  "emotional_journey_phases": [
    {{
      "phase": "opening",
      "timestamp": "[02:15]",
      "emotional_state": "curious",
      "intensity": 6,
      "trigger_moment": "[02:15] Learning about the process",
      "coaching_note": "Rep could have used curiosity to build more engagement - ask more questions"
    }},
    {{
      "phase": "discovery",
      "timestamp": "[08:30]",
      "emotional_state": "vulnerable",
      "intensity": 8,
      "trigger_moment": "[08:30] Shared deep marriage pain",
      "coaching_note": "Peak emotional moment - rep should have acknowledged and used for urgency"
    }}
  ],
  "emotional_patterns": {{
    "dominant_emotion": "hopeful",
    "emotional_shifts": [
      "[12:45] Became more engaged when solution presented",
      "[22:10] Showed resistance after price mention"
    ],
    "missed_emotional_opportunities": [
      "[15:20] Client expressed fear but rep didn't address it",
      "[28:40] High emotional state - rep should have closed here"
    ]
  }}
}}

Focus on marriage crisis emotions: desperation, hope, fear, skepticism, relief. Include timestamps for ALL key moments."""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=1200,
                operation_name="Emotional Journey Analysis"
            )

            logger.info(f"AI emotional journey response: {response_text}")

            # Clean and extract JSON
            response_text = response_text.replace('```json', '').replace('```', '').strip()

            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            # Validate structure
            if not result.get('emotional_journey_phases'):
                raise ValueError("Missing emotional_journey_phases")

            logger.info(f"AI emotional journey analysis successful with {len(result['emotional_journey_phases'])} phases")
            return result

        except Exception as e:
            logger.error(f"AI emotional journey analysis failed: {str(e)}")
            # Fallback to keyword approach if AI fails
            logger.info("Falling back to keyword-based emotional journey")
            return await self._fallback_keyword_emotional_journey(content)

    async def _fallback_keyword_emotional_journey(self, content):
        """Fallback keyword-based emotional journey if AI fails"""
        logger.info("Using keyword-based fallback emotional journey")

        content_lower = content.lower()

        # Simple emotion detection
        if any(word in content_lower for word in ['desperate', 'crisis', 'urgent', 'falling apart']):
            dominant_emotion = "desperate"
            phases = [
                {"phase": "opening", "emotional_state": "panicked", "intensity": 9, "trigger_moment": "Crisis expressed", "coaching_note": "Acknowledge crisis, build hope"},
                {"phase": "discovery", "emotional_state": "vulnerable", "intensity": 8, "trigger_moment": "Shared struggles", "coaching_note": "Create safe space"},
                {"phase": "presentation", "emotional_state": "hopeful", "intensity": 7, "trigger_moment": "Heard solutions", "coaching_note": "Build on hope"},
                {"phase": "closing", "emotional_state": "motivated", "intensity": 8, "trigger_moment": "Ready for action", "coaching_note": "Create urgency"}
            ]
        elif any(word in content_lower for word in ['hopeful', 'excited', 'optimistic']):
            dominant_emotion = "hopeful"
            phases = [
                {"phase": "opening", "emotional_state": "optimistic", "intensity": 7, "trigger_moment": "Positive about change", "coaching_note": "Channel optimism"},
                {"phase": "discovery", "emotional_state": "engaged", "intensity": 8, "trigger_moment": "Active participation", "coaching_note": "Uncover motivations"},
                {"phase": "presentation", "emotional_state": "excited", "intensity": 8, "trigger_moment": "Seeing potential", "coaching_note": "Paint transformation picture"},
                {"phase": "closing", "emotional_state": "motivated", "intensity": 9, "trigger_moment": "Ready to begin", "coaching_note": "Close confidently"}
            ]
        else:
            dominant_emotion = "mixed"
            phases = [
                {"phase": "opening", "emotional_state": "curious", "intensity": 6, "trigger_moment": "Learning process", "coaching_note": "Build engagement"},
                {"phase": "discovery", "emotional_state": "concerned", "intensity": 7, "trigger_moment": "Discussing challenges", "coaching_note": "Address concerns"},
                {"phase": "presentation", "emotional_state": "interested", "intensity": 7, "trigger_moment": "Considering options", "coaching_note": "Clear value proposition"},
                {"phase": "closing", "emotional_state": "thoughtful", "intensity": 6, "trigger_moment": "Weighing decision", "coaching_note": "Help decision process"}
            ]

        return {
            "emotional_journey_phases": phases,
            "emotional_patterns": {
                "dominant_emotion": dominant_emotion,
                "emotional_shifts": ["Initial to engaged", "Engaged to decision-ready"],
                "missed_emotional_opportunities": ["Keyword-based fallback analysis"]
            }
        }

    async def classify_marriage_archetype(self, content):
        """Classify into marriage coaching specific archetypes using Claude Sonnet 4.5"""

        # Use shorter content for reliable analysis
        content_preview = content[:3000] if len(content) > 3000 else content
        logger.info(f"AI archetype analysis for content length: {len(content_preview)}")

        prompt = f"""You are an expert marriage coaching sales psychologist. Analyze this transcript and classify the prospect's psychological archetype.

TRANSCRIPT:
{content_preview}

MARRIAGE COACHING ARCHETYPES:
1. DESPERATE SAVER - High urgency, crisis-driven, time pressure language
2. ANALYTICAL RESEARCHER - Wants data, statistics, success rates, proof
3. HOPEFUL BUILDER - Optimistic, growth-focused, investment-oriented
4. SKEPTICAL EVALUATOR - Cautious, mentions scams/trust issues
5. CONSENSUS SEEKER - Needs spouse approval, collaborative language

Return ONLY this JSON:
{{
  "primary_archetype": "DESPERATE SAVER",
  "confidence_score": 0.85,
  "supporting_quotes": ["quote from transcript", "another quote"],
  "behavioral_indicators": ["behavior pattern 1", "behavior pattern 2"]
}}"""

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=800,
                operation_name="Archetype Classification"
            )

            logger.info(f"AI archetype response: {response_text}")

            # Clean and extract JSON
            response_text = response_text.replace('```json', '').replace('```', '').strip()

            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            # Add missing fields for frontend compatibility
            result.setdefault('secondary_archetype', 'Hopeful Builder')
            result.setdefault('confidence_score', 0.75)
            result.setdefault('archetype_evidence', {
                "supporting_quotes": result.get('supporting_quotes', []),
                "behavioral_indicators": result.get('behavioral_indicators', [])
            })

            logger.info(f"AI archetype classification successful: {result.get('primary_archetype')}")
            return result

        except Exception as e:
            logger.error(f"AI archetype analysis failed: {str(e)}")
            # Fallback to keyword approach if AI fails
            logger.info("Falling back to keyword-based classification")
            return await self._fallback_keyword_archetype(content)

    async def _fallback_keyword_archetype(self, content):
        """Fallback keyword-based archetype classification if AI fails"""
        logger.info("Using keyword-based fallback archetype classification")

        content_lower = content.lower()
        archetype_scores = {
            'DESPERATE SAVER': 0,
            'ANALYTICAL RESEARCHER': 0,
            'SKEPTICAL EVALUATOR': 0,
            'CONSENSUS SEEKER': 0,
            'HOPEFUL BUILDER': 0
        }

        # Simplified keyword matching
        if any(word in content_lower for word in ['urgent', 'crisis', 'desperate', 'emergency', 'last chance']):
            archetype_scores['DESPERATE SAVER'] += 3
        if any(word in content_lower for word in ['statistics', 'success rate', 'data', 'proof', 'evidence']):
            archetype_scores['ANALYTICAL RESEARCHER'] += 3
        if any(word in content_lower for word in ['scam', 'too good', 'burned before', 'suspicious']):
            archetype_scores['SKEPTICAL EVALUATOR'] += 3
        if any(word in content_lower for word in ['my spouse', 'my partner', 'we need to discuss']):
            archetype_scores['CONSENSUS SEEKER'] += 3
        if any(word in content_lower for word in ['excited', 'hopeful', 'looking forward', 'improve']):
            archetype_scores['HOPEFUL BUILDER'] += 3

        # Select highest scoring archetype
        max_score = max(archetype_scores.values())
        archetype = 'HOPEFUL BUILDER' if max_score == 0 else max(archetype_scores, key=archetype_scores.get)

        return {
            "primary_archetype": archetype,
            "confidence_score": 0.70,
            "secondary_archetype": "Hopeful Builder",
            "archetype_evidence": {
                "supporting_quotes": ["Keyword-based fallback analysis"],
                "behavioral_indicators": ["Pattern matching classification"]
            }
        }

    def determine_coaching_urgency(self, success_probability):
        """
        Determine if immediate coaching is needed based on 75% threshold
        Only flag high-probability misses (>=75%) for urgent coaching
        """
        if success_probability >= 0.75:
            return {
                'immediate_coaching_needed': True,
                'urgency_reason': 'High-probability prospect (75%+) requires immediate coaching attention',
                'coaching_priority': 'URGENT',
                'recommended_actions': [
                    'Review call recording immediately',
                    'Identify specific missed closing opportunities',
                    'Schedule coaching session within 24 hours',
                    'Prepare follow-up strategy for prospect'
                ]
            }
        elif success_probability >= 0.60:
            return {
                'immediate_coaching_needed': False,
                'urgency_reason': 'Moderate probability prospect - standard coaching queue',
                'coaching_priority': 'STANDARD',
                'recommended_actions': [
                    'Include in weekly coaching review',
                    'Analyze for skill development opportunities',
                    'Note patterns for group coaching sessions'
                ]
            }
        else:
            return {
                'immediate_coaching_needed': False,
                'urgency_reason': 'Low probability prospect - focus on lead quality',
                'coaching_priority': 'LOW',
                'recommended_actions': [
                    'Review lead qualification process',
                    'Assess if prospect was properly qualified',
                    'Focus coaching on discovery and qualification skills'
                ]
            }

    def extract_participant_names(self, content):
        """
        Extract participant names from transcript using pattern matching
        Enhanced name detection for Phase 3
        """
        import re

        names = {'client_name': None, 'closer_name': None}
        content_lower = content.lower()

        # Common introduction patterns
        intro_patterns = [
            r"hi,?\s+i'?m\s+([a-z]+)",
            r"my name is\s+([a-z]+)",
            r"this is\s+([a-z]+)",
            r"i'm\s+([a-z]+)",
            r"speaking with\s+([a-z]+)"
        ]

        found_names = []
        for pattern in intro_patterns:
            matches = re.findall(pattern, content_lower)
            found_names.extend(matches)

        # Remove common words that aren't names
        common_words = {'calling', 'here', 'good', 'great', 'fine', 'okay', 'sure', 'yes', 'no'}
        potential_names = [name.title() for name in found_names if name not in common_words and len(name) > 2]

        # Assign names - first unique name is likely client, second is closer
        unique_names = list(dict.fromkeys(potential_names))  # Remove duplicates while preserving order

        if len(unique_names) >= 1:
            names['client_name'] = unique_names[0]
        if len(unique_names) >= 2:
            names['closer_name'] = unique_names[1]

        logger.info(f"Extracted names: {names}")
        return names

    async def analyze_talk_track_improvements(self, content, sales_framework, marriage_analysis):
        """Generate specific talk track improvements for marriage coaching sales"""

        prompt = f"""
        Analyze this marriage coaching sales call and provide specific talk track improvements and script recommendations.

        TRANSCRIPT:
        {content}

        SALES FRAMEWORK SCORES:
        {json.dumps(sales_framework.get('framework_scores', {}), indent=2)}

        MARRIAGE COACHING ANALYSIS:
        {json.dumps(marriage_analysis.get('marriage_coaching_elements', {}), indent=2)}

        Provide surgical talk track improvements:

        {{
          "talk_track_analysis": {{
            "opening_improvements": {{
              "current_opening_effectiveness": 1-10,
              "what_worked": ["effective opening elements with quotes"],
              "what_failed": ["weak opening elements with quotes"],
              "improved_opening_script": "specific script improvement for marriage coaching",
              "hook_recommendations": ["powerful hooks for marriage coaching prospects"],
              "rapport_building_improvements": "specific rapport techniques for marriage situations"
            }},
            "discovery_talk_track": {{
              "current_discovery_effectiveness": 1-10,
              "strong_questions_asked": ["good discovery questions with prospect responses"],
              "weak_questions_asked": ["poor questions that didn't uncover key info"],
              "missing_critical_questions": ["essential marriage coaching discovery questions not asked"],
              "improved_discovery_sequence": [
                "Question 1: [specific improved question]",
                "Question 2: [follow-up question based on response]",
                "Question 3: [deeper discovery question]",
                "And 7 more sequential questions for marriage coaching discovery..."
              ],
              "emotional_discovery_improvements": "how to uncover emotional state more effectively"
            }},
            "presentation_improvements": {{
              "current_presentation_effectiveness": 1-10,
              "presentation_strengths": ["what rep presented well with quotes"],
              "presentation_weaknesses": ["what rep presented poorly with quotes"],
              "marriage_value_presentation_script": "improved script for positioning marriage coaching value",
              "analogy_integration": "how to weave analogies into presentation more effectively",
              "emotional_connection_improvements": "scripts to create deeper emotional connection"
            }},
            "objection_handling_scripts": {{
              "price_objection_improvements": {{
                "common_price_objections": ["actual objections from transcript"],
                "current_responses_effectiveness": [{{ "objection": "quote", "response": "rep response", "effectiveness": 1-10 }}],
                "improved_price_scripts": [{{ "objection": "price concern", "improved_response": "better script response" }}],
                "investment_reframe_scripts": ["scripts to reframe cost as investment in marriage"]
              }},
              "time_objection_improvements": {{
                "time_concerns_raised": ["actual time objections from transcript"],
                "urgency_creation_scripts": ["scripts to create urgency about marriage timeline"],
                "time_value_positioning": "positioning marriage coaching as time-sensitive investment"
              }},
              "spouse_objection_handling": {{
                "wife_resistance_concerns": ["concerns about spouse buy-in from transcript"],
                "spouse_involvement_scripts": ["scripts for handling spouse resistance"],
                "consensus_building_techniques": "talk track for getting spouse on board"
              }}
            }},
            "closing_improvements": {{
              "current_closing_effectiveness": 1-10,
              "closing_attempts_analysis": [{{ "attempt": "quote of closing attempt", "effectiveness": 1-10, "improvement": "how to close better" }}],
              "improved_closing_sequences": [
                "Soft Close: [specific script for soft close attempt]",
                "Medium Close: [script for medium pressure close]",
                "Hard Close: [script for direct close attempt]"
              ],
              "urgency_creation_scripts": ["scripts to create urgency about marriage situation"],
              "emotional_leverage_closing": "how to use emotions discovered for closing"
            }},
            "follow_up_talk_track": {{
              "immediate_follow_up_script": "script for following up within 24 hours",
              "objection_follow_up_scripts": [{{ "objection_type": "price|time|spouse", "follow_up_script": "specific follow-up for this objection" }}],
              "value_reinforcement_follow_up": "scripts to reinforce marriage value in follow-up",
              "urgency_follow_up_techniques": "creating urgency in follow-up conversations"
            }}
          }},
          "script_drilling_priorities": {{
            "top_3_scripts_to_master": [
              "Script 1: [specific script with rationale]",
              "Script 2: [specific script with rationale]",
              "Script 3: [specific script with rationale]"
            ],
            "role_play_scenarios": [
              "Scenario 1: [specific marriage situation to practice]",
              "Scenario 2: [specific objection to practice]",
              "Scenario 3: [specific closing situation to practice]"
            ],
            "daily_practice_recommendations": "what rep should practice daily to improve talk track"
          }},
          "marriage_coaching_specialization": {{
            "marriage_specific_language": {{
              "words_to_use_more": ["marriage", "relationship", "connection", "intimacy", "partnership"],
              "words_to_avoid": ["coaching", "training", "program" - instead use "solution", "transformation", "breakthrough"],
              "emotional_language_improvements": "more emotionally resonant language for marriage coaching"
            }},
            "marriage_situation_adaptations": {{
              "separated_couples_talk_track": "specific scripts for separated couples",
              "same_house_different_rooms_script": "scripts for couples living together but distant",
              "high_conflict_couples_approach": "talk track for couples in high conflict",
              "low_intimacy_couples_positioning": "how to position coaching for intimacy issues"
            }}
          }}
        }}

        Focus on actionable, specific scripts that will improve marriage coaching sales performance immediately.

        Respond with ONLY the JSON object.
        """

        try:
            response_text = await self._call_api_with_retry(
                prompt=prompt,
                max_tokens=4000,
                operation_name="Talk Track Improvements Analysis"
            )

            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Talk track analysis error after retries: {str(e)}")
            return self.get_fallback_talk_track()

    def calculate_marriage_success_probability(self, sales_framework, marriage_analysis, archetype):
        """
        Calculate close probability based on evidence-based marriage coaching conversion factors.

        Research-backed weighting from relationship coaching industry benchmarks:
        - Consultation call conversion rates: 25-70% (professional services average 20%)
        - Phone vs. online conversion: 10-20x higher close rate
        - Prochaska-DiClemente stages of change model for behavioral readiness
        - Relationship investment theory (Rusbult) for commitment psychology
        """

        try:
            # Sales Framework Performance (35% weight)
            # Based on professional services industry benchmarks showing high consultation conversion rates
            framework_score = sales_framework.get('framework_scores', {})
            total_framework_score = 0

            for category in ['call_control', 'discovery_depth', 'empathetic_confrontation',
                           'objection_handling', 'value_positioning', 'closing_strength']:
                total_framework_score += framework_score.get(category, {}).get('score', 5)

            sales_performance = total_framework_score / 60  # Normalize to 0-1

            # Behavioral Readiness to Change (40% weight)
            # Prochaska-DiClemente research: 40% precontemplation, 40% contemplation, 20% preparation
            # Marriage crisis creates accelerated readiness compared to general population
            marriage_factors = marriage_analysis.get('marriage_situation_assessment', {})
            urgency_level = marriage_factors.get('urgency_level', 5) / 10

            # Stage of Change Assessment (Transtheoretical Model)
            change_stage_score = 0.6  # Default (contemplation stage)
            emotional_state = marriage_factors.get('emotional_state', 'neutral')

            if emotional_state == 'desperate':
                change_stage_score = 0.85  # Action stage - crisis creates immediate readiness
            elif emotional_state == 'hopeful':
                change_stage_score = 0.75  # Preparation stage - motivated and planning
            elif emotional_state == 'angry':
                change_stage_score = 0.45  # Precontemplation - resistance to change
            elif emotional_state == 'analytical':
                change_stage_score = 0.65  # Late contemplation - weighing options

            behavioral_readiness = (urgency_level * 0.6) + (change_stage_score * 0.4)

            # Relationship Investment Theory (15% weight)
            # Rusbult's model: satisfaction, alternatives, investment size predict commitment
            archetype_name = archetype.get('primary_archetype', 'Mixed Profile')
            investment_psychology = 0.6  # Default

            if archetype_name == 'DESPERATE SAVER':
                investment_psychology = 0.9  # High investment, few alternatives, low satisfaction
            elif archetype_name == 'HOPEFUL BUILDER':
                investment_psychology = 0.8  # High satisfaction, high investment
            elif archetype_name == 'ANALYTICAL RESEARCHER':
                investment_psychology = 0.5  # Methodical decision-making, comparing alternatives
            elif archetype_name == 'SKEPTICAL EVALUATOR':
                investment_psychology = 0.3  # Low trust, considering alternatives
            elif archetype_name == 'CONSENSUS SEEKER':
                investment_psychology = 0.4  # Dependent on partner buy-in, divided investment

            # Trust and Rapport Building (10% weight)
            # Critical for relationship coaching where vulnerability is required
            archetype_confidence = archetype.get('confidence_score', 0.5)
            trust_factor = archetype_confidence  # Higher archetype accuracy = better rapport match

            # Evidence-based weighted calculation for marriage coaching
            # Research shows consultation calls convert 25-70%, weighted for behavioral psychology
            success_probability = (
                sales_performance * 0.35 +          # Sales execution capability
                behavioral_readiness * 0.40 +       # Prochaska-DiClemente readiness to change
                investment_psychology * 0.15 +      # Rusbult relationship investment theory
                trust_factor * 0.10                 # Archetypal rapport and trust building
            )

            # Industry benchmarks: 25-70% consultation conversion, cap at realistic ranges
            return min(max(success_probability, 0.15), 0.85)

        except Exception as e:
            logger.error(f"Success probability calculation error: {str(e)}")
            return 0.4  # Industry average for professional services consultation calls

    # Fallback methods
    def get_fallback_sales_framework(self):
        return {
            "framework_scores": {
                "call_control": {"score": 5, "analysis": "analysis unavailable"},
                "discovery_depth": {"score": 5, "analysis": "analysis unavailable"},
                "empathetic_confrontation": {"score": 5, "analysis": "analysis unavailable"},
                "objection_handling": {"score": 5, "analysis": "analysis unavailable"},
                "value_positioning": {"score": 5, "analysis": "analysis unavailable"},
                "closing_strength": {"score": 5, "analysis": "analysis unavailable"}
            },
            "total_score": 30,
            "overall_grade": "C"
        }

    def get_fallback_marriage_analysis(self):
        return {
            "marriage_coaching_elements": {
                "listening_with_intent": {"information_gathering_score": 5, "information_callback_score": 5},
                "empathy_vs_confrontation_balance": {"empathy_score": 5, "confrontation_score": 5},
                "value_vs_price_analysis": {"marriage_value_positioning": {"score": 5}},
                "marriage_analogies_effectiveness": {"analogies_used": {}}
            },
            "marriage_situation_assessment": {
                "relationship_status": "unclear",
                "urgency_level": 5,
                "emotional_state": "confused"
            }
        }

    def get_fallback_emotional_journey(self):
        return {
            "emotional_journey_phases": [],
            "emotional_patterns": {"dominant_emotion": "neutral"},
            "emotional_coaching_strategy": {"next_call_emotional_approach": "empathetic discovery"}
        }

    def get_fallback_archetype(self):
        return {
            "primary_archetype": "Mixed Profile",
            "confidence_score": 0.5,
            "secondary_archetype": "Hopeful Builder",
            "archetype_evidence": {"supporting_quotes": [], "behavioral_indicators": []},
            "pre_call_validation": {"recommended_questions": [], "archetype_accuracy_prediction": 5}
        }

    def get_fallback_psychological_analysis(self):
        return {
            "big_five_personality": {
                "openness": {"score": 50, "confidence": 50, "implications": "analysis unavailable"},
                "conscientiousness": {"score": 50, "confidence": 50, "implications": "analysis unavailable"},
                "extraversion": {"score": 50, "confidence": 50, "implications": "analysis unavailable"},
                "agreeableness": {"score": 50, "confidence": 50, "implications": "analysis unavailable"},
                "neuroticism": {"score": 50, "confidence": 50, "implications": "analysis unavailable"}
            },
            "decision_making_style": {"primary_style": "mixed", "confidence": 50},
            "emotional_state": {"primary_emotion": "neutral", "intensity": 5, "stability": 5},
            "communication_preferences": {"directness": 5, "detail_level": "medium", "pace": "moderate"}
        }

    def get_fallback_talk_track(self):
        return {
            "talk_track_analysis": {
                "opening_improvements": {
                    "current_opening_effectiveness": 5,
                    "what_worked": ["analysis unavailable"],
                    "what_failed": ["analysis unavailable"],
                    "improved_opening_script": "analysis unavailable",
                    "hook_recommendations": ["analysis unavailable"]
                },
                "discovery_talk_track": {
                    "current_discovery_effectiveness": 5,
                    "strong_questions_asked": ["analysis unavailable"],
                    "missing_critical_questions": ["analysis unavailable"]
                },
                "objection_handling_scripts": {
                    "price_objection_improvements": {"common_price_objections": ["analysis unavailable"]},
                    "time_objection_improvements": {"time_concerns_raised": ["analysis unavailable"]},
                    "spouse_objection_handling": {"wife_resistance_concerns": ["analysis unavailable"]}
                }
            },
            "script_drilling_priorities": {
                "top_3_scripts_to_master": ["analysis unavailable", "analysis unavailable", "analysis unavailable"],
                "daily_practice_recommendations": "analysis unavailable"
            }
        }

# Vercel handler
class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                self.send_error_response(500, {
                    'error': 'API key not configured',
                    'message': 'Please set ANTHROPIC_API_KEY environment variable in Vercel'
                })
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                body = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response(400, {'error': 'Invalid JSON in request body'})
                return

            if 'content' not in body:
                self.send_error_response(400, {'error': 'Missing required field: content'})
                return

            content = body['content']
            filename = body.get('filename', 'transcript.txt')

            if not content or len(content.strip()) < 100:
                self.send_error_response(400, {
                    'error': 'Content too short. Please provide at least 100 characters of transcript content.'
                })
                return

            # Initialize analyzer with retry configuration
            analyzer = MarriageCoachingAnalyzer(
                api_key=api_key,
                max_retries=3,  # Retry up to 3 times
                timeout=120  # 2 minute timeout per request
            )
            result = asyncio.run(analyzer.analyze_marriage_coaching_call(content, filename))

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            logger.error(f"Marriage coaching analysis error: {str(e)}")
            self.send_error_response(500, {
                'error': 'Internal server error',
                'message': str(e)
            })

    def send_error_response(self, status_code, error_data):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(error_data).encode('utf-8'))