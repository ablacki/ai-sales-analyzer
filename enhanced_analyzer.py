#!/usr/bin/env python3
"""
Enhanced Sales Call Analyzer with Advanced Psychological Profiling
Analyzes marriage coaching sales transcripts for deep psychological insights and coaching recommendations.
"""

import asyncio
import json
import pandas as pd
from anthropic import AsyncAnthropic
import os
from datetime import datetime
import logging
import sqlite3
from typing import Dict, List, Optional, Any

class EnhancedSalesAnalyzer:
    """Advanced AI-powered sales call analyzer with psychological profiling"""

    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.setup_logging()
        self.setup_database()

    def setup_logging(self):
        """Configure comprehensive logging system"""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/enhanced_analysis.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_database(self):
        """Initialize enhanced database schema"""
        os.makedirs('data', exist_ok=True)
        self.db_path = 'data/enhanced_sales_analysis.db'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Enhanced clients table with psychological profiles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT UNIQUE NOT NULL,
                    analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

                    -- Basic Info
                    client_name TEXT,
                    call_duration_minutes INTEGER,
                    word_count INTEGER,

                    -- Psychological Profile (JSON fields)
                    big_five_personality TEXT,
                    emotional_intelligence TEXT,
                    decision_making_style TEXT,
                    communication_preferences TEXT,

                    -- Archetype Classification
                    primary_archetype TEXT,
                    archetype_confidence REAL,
                    secondary_archetype TEXT,

                    -- Sales Performance
                    overall_sales_score INTEGER,
                    rapport_score INTEGER,
                    discovery_score INTEGER,
                    presentation_score INTEGER,
                    objection_handling_score INTEGER,
                    closing_score INTEGER,

                    -- Coaching Insights
                    coaching_recommendations TEXT,
                    improvement_priorities TEXT,
                    follow_up_strategy TEXT,
                    success_probability REAL,

                    -- Full Analysis Data
                    complete_analysis TEXT
                )
            ''')

            # Analysis sessions tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start DATETIME DEFAULT CURRENT_TIMESTAMP,
                    transcripts_processed INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    error_count INTEGER DEFAULT 0,
                    session_notes TEXT
                )
            ''')

            conn.commit()
            self.logger.info("✓ Database schema initialized")

    async def analyze_transcript(self, transcript_path: str, content: str) -> Dict[str, Any]:
        """
        Comprehensive transcript analysis with enhanced psychological profiling
        """
        transcript_id = os.path.basename(transcript_path)
        self.logger.info(f"🔍 Starting enhanced analysis for {transcript_id}")

        try:
            # Prepare transcript content
            if len(content) > 15000:
                content = content[:15000] + "... [Content truncated for analysis]"

            # Run comprehensive analysis in parallel for efficiency
            psychological_task = self.analyze_psychological_profile(content)
            sales_performance_task = self.analyze_sales_performance(content)
            emotional_journey_task = self.analyze_emotional_journey(content)
            communication_task = self.analyze_communication_patterns(content)

            # Wait for all analyses to complete
            psychological_profile = await psychological_task
            sales_performance = await sales_performance_task
            emotional_journey = await emotional_journey_task
            communication_patterns = await communication_task

            # Advanced archetype classification
            archetype_analysis = await self.classify_client_archetype(
                psychological_profile, sales_performance, emotional_journey
            )

            # Generate personalized coaching recommendations
            coaching_recommendations = await self.generate_coaching_recommendations(
                psychological_profile, sales_performance, archetype_analysis
            )

            # Calculate success probability
            success_probability = self.calculate_success_probability(
                sales_performance, psychological_profile, archetype_analysis
            )

            # Compile comprehensive results
            analysis_result = {
                'transcript_id': transcript_id,
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'success',

                # Core Analysis
                'psychological_profile': psychological_profile,
                'sales_performance': sales_performance,
                'emotional_journey': emotional_journey,
                'communication_patterns': communication_patterns,

                # Classification & Insights
                'archetype_analysis': archetype_analysis,
                'coaching_recommendations': coaching_recommendations,
                'success_probability': success_probability,

                # Metadata
                'word_count': len(content.split()),
                'estimated_duration': self.estimate_call_duration(content),
                'analysis_confidence': self.calculate_analysis_confidence(
                    psychological_profile, sales_performance
                )
            }

            # Save to database
            await self.save_analysis_to_database(transcript_path, analysis_result)

            self.logger.info(f"✅ Enhanced analysis completed for {transcript_id}")
            return analysis_result

        except Exception as e:
            self.logger.error(f"❌ Analysis failed for {transcript_id}: {str(e)}")
            return {
                'transcript_id': transcript_id,
                'status': 'failed',
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }

    async def analyze_psychological_profile(self, content: str) -> Dict[str, Any]:
        """Advanced Big Five personality analysis with coaching insights"""

        prompt = f"""
        Conduct a comprehensive psychological analysis of this client based on their conversation patterns and responses.

        CONVERSATION TRANSCRIPT:
        {content}

        Analyze and provide detailed psychological insights in JSON format:
        {{
          "big_five_personality": {{
            "openness": {{
              "score": 1-100,
              "confidence": 1-100,
              "evidence": ["specific quotes or behaviors"],
              "coaching_implications": "detailed implications for approach",
              "adaptation_strategies": ["how to adapt communication"]
            }},
            "conscientiousness": {{
              "score": 1-100,
              "confidence": 1-100,
              "evidence": ["specific examples"],
              "coaching_implications": "follow-through and structure needs",
              "adaptation_strategies": ["specific coaching adaptations"]
            }},
            "extraversion": {{
              "score": 1-100,
              "confidence": 1-100,
              "evidence": ["conversation patterns"],
              "coaching_implications": "social interaction preferences",
              "adaptation_strategies": ["communication style adjustments"]
            }},
            "agreeableness": {{
              "score": 1-100,
              "confidence": 1-100,
              "evidence": ["cooperation indicators"],
              "coaching_implications": "conflict and cooperation handling",
              "adaptation_strategies": ["relationship building approaches"]
            }},
            "neuroticism": {{
              "score": 1-100,
              "confidence": 1-100,
              "evidence": ["stress and emotional indicators"],
              "coaching_implications": "emotional stability and stress response",
              "adaptation_strategies": ["emotional support strategies"]
            }}
          }},
          "emotional_intelligence": {{
            "self_awareness": {{ "score": 1-10, "evidence": ["examples"] }},
            "self_regulation": {{ "score": 1-10, "evidence": ["examples"] }},
            "motivation": {{ "score": 1-10, "evidence": ["examples"] }},
            "empathy": {{ "score": 1-10, "evidence": ["examples"] }},
            "social_skills": {{ "score": 1-10, "evidence": ["examples"] }}
          }},
          "decision_making_profile": {{
            "primary_style": "analytical|intuitive|emotional|consensus",
            "secondary_style": "analytical|intuitive|emotional|consensus",
            "information_processing": "detail_oriented|big_picture|balanced",
            "risk_tolerance": {{ "score": 1-10, "rationale": "explanation" }},
            "time_preference": "immediate|days|weeks|months",
            "influence_factors": ["what influences their decisions"]
          }},
          "stress_and_motivation": {{
            "current_stress_level": {{ "score": 1-10, "indicators": ["signs"] }},
            "primary_stressors": ["main sources of stress"],
            "motivation_drivers": ["key motivating factors"],
            "energy_level": {{ "score": 1-10, "indicators": ["signs"] }}
          }},
          "relationship_dynamics": {{
            "attachment_style": "secure|anxious|avoidant|disorganized",
            "conflict_style": "accommodating|competing|avoiding|collaborating|compromising",
            "trust_building": {{ "score": 1-10, "patterns": ["trust indicators"] }}
          }}
        }}

        Focus on actionable insights for marriage coaching sales. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            self.logger.error(f"Psychological analysis error: {str(e)}")
            return self.get_default_psychological_profile()

    async def analyze_sales_performance(self, content: str) -> Dict[str, Any]:
        """Comprehensive sales conversation performance analysis"""

        prompt = f"""
        Analyze this marriage coaching sales conversation for detailed performance metrics and improvement opportunities.

        SALES CONVERSATION:
        {content}

        Provide comprehensive sales analysis in JSON format:
        {{
          "overall_assessment": {{
            "performance_score": 1-100,
            "grade": "A+|A|A-|B+|B|B-|C+|C|C-|D|F",
            "conversion_likelihood": 1-100,
            "key_strengths": ["top 3 strengths"],
            "critical_improvements": ["top 3 areas needing work"]
          }},
          "sales_skills_breakdown": {{
            "opening_and_rapport": {{ "score": 1-10, "feedback": "specific feedback" }},
            "discovery_and_questioning": {{ "score": 1-10, "feedback": "quality of questions asked" }},
            "active_listening": {{ "score": 1-10, "feedback": "listening effectiveness" }},
            "presentation_skills": {{ "score": 1-10, "feedback": "how well solutions were presented" }},
            "objection_handling": {{ "score": 1-10, "feedback": "response to concerns" }},
            "closing_techniques": {{ "score": 1-10, "feedback": "asking for commitment" }},
            "follow_up_planning": {{ "score": 1-10, "feedback": "next steps clarity" }}
          }},
          "conversation_dynamics": {{
            "talk_time_ratio": "rep_percentage:client_percentage",
            "question_to_statement_ratio": "questions:statements",
            "emotional_connection": {{ "score": 1-10, "evidence": ["examples"] }},
            "trust_building": {{ "score": 1-10, "evidence": ["examples"] }},
            "urgency_creation": {{ "score": 1-10, "evidence": ["examples"] }}
          }},
          "client_engagement_signals": {{
            "positive_signals": ["buying signals observed"],
            "negative_signals": ["resistance indicators"],
            "engagement_level": {{ "score": 1-10, "indicators": ["signs"] }},
            "objections_and_concerns": ["specific objections raised"]
          }},
          "missed_opportunities": {{
            "discovery_gaps": ["questions that should have been asked"],
            "presentation_gaps": ["benefits not highlighted"],
            "closing_gaps": ["closing opportunities missed"],
            "emotional_gaps": ["emotional needs not addressed"]
          }},
          "coaching_priorities": {{
            "immediate_improvements": ["changes for next call"],
            "skill_development_areas": ["longer-term skill building"],
            "technique_adjustments": ["specific technique changes"]
          }}
        }}

        Focus on actionable sales coaching insights. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            self.logger.error(f"Sales analysis error: {str(e)}")
            return self.get_default_sales_analysis()

    async def analyze_emotional_journey(self, content: str) -> Dict[str, Any]:
        """Map the client's emotional journey throughout the conversation"""

        prompt = f"""
        Map the emotional journey and psychological state changes throughout this conversation.

        CONVERSATION:
        {content}

        Provide emotional journey analysis in JSON format:
        {{
          "emotional_timeline": [
            {{
              "phase": "opening|discovery|presentation|objection_handling|closing",
              "emotional_state": "specific emotion",
              "intensity": 1-10,
              "triggers": ["what caused this emotion"],
              "duration": "brief|moderate|extended"
            }}
          ],
          "overall_emotional_profile": {{
            "dominant_emotions": ["top 3 emotions shown"],
            "emotional_stability": {{ "score": 1-10, "patterns": ["stability indicators"] }},
            "stress_indicators": ["signs of stress or pressure"],
            "positive_moments": ["when client felt good/hopeful"],
            "challenging_moments": ["when client felt resistant/negative"]
          }},
          "psychological_barriers": {{
            "fear_factors": ["what they're afraid of"],
            "trust_concerns": ["trust-related hesitations"],
            "financial_anxiety": {{ "level": 1-10, "indicators": ["signs"] }},
            "skepticism_areas": ["what they're skeptical about"],
            "past_hurt_indicators": ["signs of previous relationship damage"]
          }},
          "motivation_and_hope": {{
            "hope_level": {{ "score": 1-10, "evidence": ["hopeful statements"] }},
            "motivation_strength": {{ "score": 1-10, "indicators": ["motivation signs"] }},
            "vision_clarity": {{ "score": 1-10, "evidence": ["clear vision statements"] }},
            "commitment_readiness": {{ "score": 1-10, "indicators": ["readiness signs"] }}
          }},
          "emotional_coaching_needs": {{
            "primary_emotional_need": "hope|validation|security|control|connection",
            "secondary_needs": ["other emotional needs"],
            "emotional_triggers_to_avoid": ["what not to do"],
            "emotional_bridges_to_build": ["how to connect emotionally"]
          }}
        }}

        Focus on emotional insights that inform coaching approach. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            self.logger.error(f"Emotional analysis error: {str(e)}")
            return self.get_default_emotional_analysis()

    async def analyze_communication_patterns(self, content: str) -> Dict[str, Any]:
        """Analyze communication style and preferences"""

        prompt = f"""
        Analyze the communication patterns, style, and preferences shown in this conversation.

        CONVERSATION:
        {content}

        Provide communication analysis in JSON format:
        {{
          "communication_style": {{
            "directness_level": {{ "score": 1-10, "examples": ["direct statements"] }},
            "formality_preference": "very_formal|formal|mixed|casual|very_casual",
            "detail_orientation": {{ "score": 1-10, "evidence": ["detail requests"] }},
            "pace_preference": "fast|moderate|slow",
            "processing_style": "verbal|visual|kinesthetic|mixed"
          }},
          "language_patterns": {{
            "vocabulary_level": "basic|intermediate|advanced",
            "technical_comfort": {{ "score": 1-10, "indicators": ["tech usage"] }},
            "metaphor_usage": ["metaphors or analogies they used"],
            "question_patterns": ["how they ask questions"],
            "concern_expression": ["how they express worries"]
          }},
          "interaction_preferences": {{
            "interruption_comfort": {{ "score": 1-10, "evidence": ["interruption behavior"] }},
            "silence_tolerance": {{ "score": 1-10, "evidence": ["silence handling"] }},
            "validation_needs": {{ "score": 1-10, "evidence": ["validation seeking"] }},
            "control_preference": {{ "score": 1-10, "evidence": ["control indicators"] }}
          }},
          "optimal_communication_approach": {{
            "recommended_pace": "match their preference",
            "recommended_detail_level": "high|medium|low",
            "recommended_tone": "formal|professional|warm|casual",
            "key_phrases_to_use": ["phrases that resonate with them"],
            "phrases_to_avoid": ["communication patterns to avoid"],
            "optimal_follow_up_style": "detailed email|brief text|phone call|video call"
          }}
        }}

        Focus on actionable communication insights. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            self.logger.error(f"Communication analysis error: {str(e)}")
            return self.get_default_communication_analysis()

    async def classify_client_archetype(self, psychological_profile: Dict, sales_performance: Dict, emotional_journey: Dict) -> Dict[str, Any]:
        """Enhanced 5-archetype classification with confidence scoring"""

        # Define the 5 client archetypes
        archetypes = {
            "analytical_researcher": {
                "name": "Analytical Researcher",
                "description": "Data-driven, needs facts and logical arguments",
                "communication_style": "detailed, evidence-based",
                "decision_timeline": "extended research phase",
                "key_motivators": ["proof", "statistics", "logical arguments"]
            },
            "desperate_saver": {
                "name": "Desperate Saver",
                "description": "High urgency, emotional, facing relationship crisis",
                "communication_style": "emotional, urgent",
                "decision_timeline": "quick decision needed",
                "key_motivators": ["immediate relief", "crisis resolution", "hope"]
            },
            "hopeful_builder": {
                "name": "Hopeful Builder",
                "description": "Optimistic, growth-focused, future-oriented",
                "communication_style": "positive, vision-focused",
                "decision_timeline": "reasonable consideration period",
                "key_motivators": ["growth potential", "future vision", "improvement"]
            },
            "skeptical_evaluator": {
                "name": "Skeptical Evaluator",
                "description": "Cautious, needs proof and guarantees",
                "communication_style": "questioning, cautious",
                "decision_timeline": "careful evaluation phase",
                "key_motivators": ["guarantees", "testimonials", "risk mitigation"]
            },
            "consensus_seeker": {
                "name": "Consensus Seeker",
                "description": "Involves others, needs group approval",
                "communication_style": "collaborative, consultative",
                "decision_timeline": "involves partner/family",
                "key_motivators": ["partner buy-in", "external validation", "shared decision"]
            }
        }

        # Classify based on analysis data
        archetype_scores = {}

        try:
            # Extract key indicators for classification
            big_five = psychological_profile.get('big_five_personality', {})
            decision_style = psychological_profile.get('decision_making_profile', {})
            emotional_state = emotional_journey.get('overall_emotional_profile', {})

            # Score each archetype based on psychological indicators
            # Analytical Researcher
            analytical_score = (
                big_five.get('openness', {}).get('score', 50) * 0.3 +
                big_five.get('conscientiousness', {}).get('score', 50) * 0.4 +
                (100 - big_five.get('neuroticism', {}).get('score', 50)) * 0.3
            )

            # Desperate Saver
            desperate_score = (
                big_five.get('neuroticism', {}).get('score', 50) * 0.5 +
                emotional_journey.get('emotional_timeline', [{}])[0].get('intensity', 5) * 10 * 0.3 +
                (10 - psychological_profile.get('stress_and_motivation', {}).get('current_stress_level', {}).get('score', 5)) * 10 * 0.2
            )

            # Hopeful Builder
            hopeful_score = (
                big_five.get('extraversion', {}).get('score', 50) * 0.3 +
                big_five.get('openness', {}).get('score', 50) * 0.3 +
                emotional_journey.get('motivation_and_hope', {}).get('hope_level', {}).get('score', 5) * 10 * 0.4
            )

            # Skeptical Evaluator
            skeptical_score = (
                big_five.get('conscientiousness', {}).get('score', 50) * 0.4 +
                (100 - big_five.get('agreeableness', {}).get('score', 50)) * 0.3 +
                len(emotional_journey.get('psychological_barriers', {}).get('skepticism_areas', [])) * 20 * 0.3
            )

            # Consensus Seeker
            consensus_score = (
                big_five.get('agreeableness', {}).get('score', 50) * 0.4 +
                (100 - big_five.get('extraversion', {}).get('score', 50)) * 0.3 +
                (10 if decision_style.get('primary_style') == 'consensus' else 0) * 0.3
            )

            archetype_scores = {
                'analytical_researcher': min(analytical_score, 100),
                'desperate_saver': min(desperate_score, 100),
                'hopeful_builder': min(hopeful_score, 100),
                'skeptical_evaluator': min(skeptical_score, 100),
                'consensus_seeker': min(consensus_score, 100)
            }

            # Determine primary archetype
            primary_archetype_key = max(archetype_scores.keys(), key=lambda k: archetype_scores[k])
            primary_score = archetype_scores[primary_archetype_key]

            # Determine secondary archetype
            remaining_scores = {k: v for k, v in archetype_scores.items() if k != primary_archetype_key}
            secondary_archetype_key = max(remaining_scores.keys(), key=lambda k: remaining_scores[k])

            return {
                'primary_archetype': archetypes[primary_archetype_key]['name'],
                'primary_archetype_key': primary_archetype_key,
                'confidence_score': primary_score / 100,
                'secondary_archetype': archetypes[secondary_archetype_key]['name'],
                'archetype_scores': archetype_scores,
                'archetype_details': archetypes[primary_archetype_key],
                'classification_reasoning': f"Primary: {archetypes[primary_archetype_key]['description']}"
            }

        except Exception as e:
            self.logger.error(f"Archetype classification error: {str(e)}")
            return {
                'primary_archetype': 'Mixed Profile',
                'confidence_score': 0.5,
                'secondary_archetype': 'Hopeful Builder',
                'error': str(e)
            }

    async def generate_coaching_recommendations(self, psychological_profile: Dict, sales_performance: Dict, archetype_analysis: Dict) -> Dict[str, Any]:
        """Generate personalized coaching recommendations"""

        archetype = archetype_analysis.get('primary_archetype', 'Mixed Profile')
        sales_score = sales_performance.get('overall_assessment', {}).get('performance_score', 50)

        prompt = f"""
        Generate specific, actionable coaching recommendations based on this client's psychological profile and sales interaction.

        CLIENT ARCHETYPE: {archetype}
        SALES PERFORMANCE SCORE: {sales_score}/100

        PSYCHOLOGICAL PROFILE: {json.dumps(psychological_profile, indent=2)}
        SALES PERFORMANCE: {json.dumps(sales_performance, indent=2)}
        ARCHETYPE DETAILS: {json.dumps(archetype_analysis, indent=2)}

        Provide comprehensive coaching recommendations in JSON format:
        {{
          "immediate_action_plan": {{
            "top_3_priorities": ["specific actions for next interaction"],
            "follow_up_timing": "1-2 days|3-5 days|1 week|2+ weeks",
            "follow_up_method": "email|phone|text|video_call",
            "key_message_focus": "main theme for follow-up"
          }},
          "communication_strategy": {{
            "tone_adjustments": "specific tone recommendations",
            "pace_modifications": "faster|slower|match_their_pace",
            "detail_level": "high_detail|moderate|high_level",
            "emotional_approach": "logical|empathetic|motivational|reassuring",
            "language_adaptations": ["specific phrases to use"],
            "topics_to_emphasize": ["key points to highlight"],
            "topics_to_avoid": ["sensitive areas to avoid"]
          }},
          "objection_handling_strategy": {{
            "likely_objections": ["expected concerns they'll raise"],
            "preparation_responses": ["how to address each objection"],
            "psychological_approaches": ["psychological techniques to use"],
            "evidence_to_gather": ["proof points to collect"]
          }},
          "relationship_building": {{
            "trust_building_actions": ["specific trust-building steps"],
            "rapport_enhancement": ["ways to deepen connection"],
            "value_demonstration": ["how to show value"],
            "credibility_boosters": ["ways to increase credibility"]
          }},
          "closing_strategy": {{
            "optimal_closing_approach": "soft_close|direct_ask|assumption|alternative_choice",
            "timing_recommendations": "when to ask for commitment",
            "commitment_steps": ["progressive commitment stages"],
            "risk_mitigation": ["ways to reduce perceived risk"]
          }},
          "long_term_nurturing": {{
            "nurture_sequence": ["follow-up sequence over time"],
            "content_recommendations": ["types of content to share"],
            "touchpoint_frequency": "weekly|bi_weekly|monthly",
            "relationship_maintenance": ["ongoing relationship activities"]
          }}
        }}

        Focus on actionable, psychology-based coaching recommendations. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            self.logger.error(f"Coaching recommendations error: {str(e)}")
            return self.get_default_coaching_recommendations()

    def calculate_success_probability(self, sales_performance: Dict, psychological_profile: Dict, archetype_analysis: Dict) -> float:
        """Calculate conversion probability based on multiple factors"""

        try:
            # Base score from sales performance
            base_score = sales_performance.get('overall_assessment', {}).get('performance_score', 50) / 100

            # Psychological readiness indicators
            stress_level = psychological_profile.get('stress_and_motivation', {}).get('current_stress_level', {}).get('score', 5)
            motivation_level = psychological_profile.get('stress_and_motivation', {}).get('motivation_strength', {}).get('score', 5)

            psychological_factor = (motivation_level - stress_level + 10) / 20  # Normalize to 0-1

            # Archetype confidence factor
            archetype_confidence = archetype_analysis.get('confidence_score', 0.5)

            # Weighted calculation
            success_probability = (
                base_score * 0.5 +
                psychological_factor * 0.3 +
                archetype_confidence * 0.2
            )

            return min(max(success_probability, 0.1), 0.95)  # Keep between 10% and 95%

        except Exception as e:
            self.logger.error(f"Success probability calculation error: {str(e)}")
            return 0.5

    async def save_analysis_to_database(self, transcript_path: str, analysis_result: Dict):
        """Save comprehensive analysis to enhanced database"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                filename = os.path.basename(transcript_path)

                # Extract key data points
                psychological = analysis_result.get('psychological_profile', {})
                sales_perf = analysis_result.get('sales_performance', {})
                archetype = analysis_result.get('archetype_analysis', {})
                coaching = analysis_result.get('coaching_recommendations', {})

                cursor.execute('''
                    INSERT OR REPLACE INTO enhanced_clients
                    (filename, word_count, big_five_personality, emotional_intelligence,
                     decision_making_style, communication_preferences, primary_archetype,
                     archetype_confidence, overall_sales_score, coaching_recommendations,
                     success_probability, complete_analysis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    filename,
                    analysis_result.get('word_count', 0),
                    json.dumps(psychological.get('big_five_personality', {})),
                    json.dumps(psychological.get('emotional_intelligence', {})),
                    json.dumps(psychological.get('decision_making_profile', {})),
                    json.dumps(analysis_result.get('communication_patterns', {})),
                    archetype.get('primary_archetype', 'Unknown'),
                    archetype.get('confidence_score', 0.5),
                    sales_perf.get('overall_assessment', {}).get('performance_score', 0),
                    json.dumps(coaching),
                    analysis_result.get('success_probability', 0.5),
                    json.dumps(analysis_result)
                ))

                conn.commit()
                self.logger.info(f"✅ Analysis saved to database for {filename}")

        except Exception as e:
            self.logger.error(f"Database save error: {str(e)}")

    def estimate_call_duration(self, content: str) -> int:
        """Estimate call duration based on content length"""
        word_count = len(content.split())
        # Rough estimate: 150 words per minute average speaking rate
        estimated_minutes = max(word_count // 150, 5)  # Minimum 5 minutes
        return estimated_minutes

    def calculate_analysis_confidence(self, psychological_profile: Dict, sales_performance: Dict) -> float:
        """Calculate confidence in analysis based on data completeness"""

        confidence_factors = []

        # Check psychological profile completeness
        big_five = psychological_profile.get('big_five_personality', {})
        if len(big_five) == 5:  # All Big Five traits present
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.6)

        # Check sales performance completeness
        sales_breakdown = sales_performance.get('sales_skills_breakdown', {})
        if len(sales_breakdown) >= 5:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.7)

        return sum(confidence_factors) / len(confidence_factors)

    # Default fallback methods
    def get_default_psychological_profile(self) -> Dict:
        return {
            "big_five_personality": {
                "openness": {"score": 50, "confidence": 50, "evidence": [], "coaching_implications": "moderate openness"},
                "conscientiousness": {"score": 50, "confidence": 50, "evidence": [], "coaching_implications": "moderate structure needs"},
                "extraversion": {"score": 50, "confidence": 50, "evidence": [], "coaching_implications": "balanced social preferences"},
                "agreeableness": {"score": 50, "confidence": 50, "evidence": [], "coaching_implications": "moderate cooperation"},
                "neuroticism": {"score": 50, "confidence": 50, "evidence": [], "coaching_implications": "moderate emotional stability"}
            },
            "emotional_intelligence": {
                "self_awareness": {"score": 5, "evidence": []},
                "self_regulation": {"score": 5, "evidence": []},
                "motivation": {"score": 5, "evidence": []},
                "empathy": {"score": 5, "evidence": []},
                "social_skills": {"score": 5, "evidence": []}
            },
            "decision_making_profile": {
                "primary_style": "mixed",
                "information_processing": "balanced",
                "risk_tolerance": {"score": 5, "rationale": "insufficient data"},
                "time_preference": "moderate"
            }
        }

    def get_default_sales_analysis(self) -> Dict:
        return {
            "overall_assessment": {
                "performance_score": 50,
                "grade": "C",
                "conversion_likelihood": 50,
                "key_strengths": ["analysis incomplete"],
                "critical_improvements": ["insufficient data"]
            },
            "sales_skills_breakdown": {
                "opening_and_rapport": {"score": 5, "feedback": "unable to analyze"},
                "discovery_and_questioning": {"score": 5, "feedback": "unable to analyze"},
                "active_listening": {"score": 5, "feedback": "unable to analyze"},
                "presentation_skills": {"score": 5, "feedback": "unable to analyze"},
                "objection_handling": {"score": 5, "feedback": "unable to analyze"},
                "closing_techniques": {"score": 5, "feedback": "unable to analyze"}
            }
        }

    def get_default_emotional_analysis(self) -> Dict:
        return {
            "emotional_timeline": [],
            "overall_emotional_profile": {
                "dominant_emotions": ["neutral"],
                "emotional_stability": {"score": 5, "patterns": []},
                "stress_indicators": [],
                "positive_moments": [],
                "challenging_moments": []
            }
        }

    def get_default_communication_analysis(self) -> Dict:
        return {
            "communication_style": {
                "directness_level": {"score": 5, "examples": []},
                "formality_preference": "mixed",
                "detail_orientation": {"score": 5, "evidence": []},
                "pace_preference": "moderate"
            }
        }

    def get_default_coaching_recommendations(self) -> Dict:
        return {
            "immediate_action_plan": {
                "top_3_priorities": ["follow up within 48 hours", "address main concerns", "provide additional information"],
                "follow_up_timing": "2-3 days",
                "follow_up_method": "email",
                "key_message_focus": "value demonstration"
            }
        }

# Utility functions for batch processing
async def process_transcript_batch(analyzer: EnhancedSalesAnalyzer, transcript_files: List[str], batch_size: int = 10):
    """Process transcripts in batches for efficiency"""

    results = []

    for i in range(0, len(transcript_files), batch_size):
        batch = transcript_files[i:i+batch_size]
        batch_tasks = []

        for transcript_path in batch:
            try:
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                batch_tasks.append(analyzer.analyze_transcript(transcript_path, content))
            except Exception as e:
                analyzer.logger.error(f"Error reading {transcript_path}: {str(e)}")

        # Process batch in parallel
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        results.extend([r for r in batch_results if not isinstance(r, Exception)])

        # Brief pause between batches to avoid rate limits
        await asyncio.sleep(2)

    return results

# Export results to CSV/JSON
def export_analysis_results(db_path: str, output_format: str = 'both'):
    """Export analysis results to CSV and JSON formats"""

    os.makedirs('exports', exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        # Export to CSV
        if output_format in ['csv', 'both']:
            df = pd.read_sql_query('SELECT * FROM enhanced_clients', conn)
            csv_path = f'exports/enhanced_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(csv_path, index=False)
            print(f"✅ CSV export saved: {csv_path}")

        # Export to JSON
        if output_format in ['json', 'both']:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM enhanced_clients')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            json_data = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                # Parse JSON fields
                for field in ['big_five_personality', 'emotional_intelligence', 'coaching_recommendations', 'complete_analysis']:
                    if row_dict.get(field):
                        try:
                            row_dict[field] = json.loads(row_dict[field])
                        except:
                            pass
                json_data.append(row_dict)

            json_path = f'exports/enhanced_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON export saved: {json_path}")

if __name__ == "__main__":
    print("Enhanced Sales Call Analyzer - Ready for implementation")
    print("Use this module to analyze marriage coaching sales transcripts with advanced psychological profiling.")