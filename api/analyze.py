"""
Vercel Serverless Function for Real AI Sales Call Analysis
Provides actual Anthropic Claude AI analysis for marriage coaching transcripts
"""

import json
import os
import asyncio
from datetime import datetime
import logging

try:
    from anthropic import AsyncAnthropic
except ImportError:
    # Fallback for deployment
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerlessAnalyzer:
    """Serverless version of Enhanced Sales Analyzer for web deployment"""

    def __init__(self, api_key):
        self.client = AsyncAnthropic(api_key=api_key)

    async def analyze_transcript_content(self, content, filename="transcript.txt"):
        """Main analysis function optimized for serverless deployment"""

        try:
            # Limit content length for API efficiency
            if len(content) > 12000:
                content = content[:12000] + "... [Content truncated for analysis]"

            # Run comprehensive analysis
            psychological_analysis = await self.analyze_psychological_profile(content)
            sales_analysis = await self.analyze_sales_performance(content)
            archetype_classification = await self.classify_archetype(psychological_analysis, sales_analysis)
            coaching_recommendations = await self.generate_coaching_recommendations(
                psychological_analysis, sales_analysis, archetype_classification
            )

            # Calculate success probability
            success_probability = self.calculate_success_probability(
                sales_analysis, psychological_analysis, archetype_classification
            )

            return {
                'transcript_id': filename,
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'success',
                'word_count': len(content.split()),
                'psychological_profile': psychological_analysis,
                'sales_performance': sales_analysis,
                'archetype_analysis': archetype_classification,
                'coaching_recommendations': coaching_recommendations,
                'success_probability': success_probability
            }

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                'transcript_id': filename,
                'status': 'error',
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }

    async def analyze_psychological_profile(self, content):
        """Big Five personality analysis with coaching insights"""

        prompt = f"""
        Analyze this marriage coaching sales conversation for deep psychological insights.

        CONVERSATION:
        {content}

        Provide Big Five personality analysis in JSON format:
        {{
          "big_five_personality": {{
            "openness": {{
              "score": 1-100,
              "confidence": 80,
              "implications": "detailed coaching implications"
            }},
            "conscientiousness": {{
              "score": 1-100,
              "confidence": 85,
              "implications": "follow-through and structure needs"
            }},
            "extraversion": {{
              "score": 1-100,
              "confidence": 75,
              "implications": "communication and social interaction style"
            }},
            "agreeableness": {{
              "score": 1-100,
              "confidence": 85,
              "implications": "cooperation and conflict handling approach"
            }},
            "neuroticism": {{
              "score": 1-100,
              "confidence": 80,
              "implications": "emotional stability and stress management"
            }}
          }},
          "decision_making_style": {{
            "primary_style": "analytical|emotional|intuitive|consensus",
            "confidence": 85,
            "time_preference": "immediate|days|weeks|months",
            "information_needs": "minimal|moderate|extensive"
          }},
          "emotional_state": {{
            "primary_emotion": "hopeful|anxious|skeptical|desperate|calm",
            "intensity": 1-10,
            "stability": 1-10
          }},
          "communication_preferences": {{
            "directness": 1-10,
            "detail_level": "high|medium|low",
            "pace": "fast|moderate|slow"
          }}
        }}

        Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Psychological analysis error: {str(e)}")
            return self.get_fallback_psychological_analysis()

    async def analyze_sales_performance(self, content):
        """Sales conversation performance analysis"""

        prompt = f"""
        Analyze this marriage coaching sales conversation for performance metrics.

        SALES CONVERSATION:
        {content}

        Provide sales performance analysis in JSON format:
        {{
          "overall_assessment": {{
            "performance_score": 1-100,
            "grade": "A|B|C|D|F",
            "conversion_likelihood": 1-100,
            "key_strengths": ["top 3 strengths"],
            "improvement_areas": ["top 3 areas needing work"]
          }},
          "skills_breakdown": {{
            "rapport_building": {{ "score": 1-10, "feedback": "specific feedback" }},
            "discovery_quality": {{ "score": 1-10, "feedback": "question effectiveness" }},
            "presentation": {{ "score": 1-10, "feedback": "solution presentation quality" }},
            "objection_handling": {{ "score": 1-10, "feedback": "concern management" }},
            "closing": {{ "score": 1-10, "feedback": "asking for commitment" }}
          }},
          "conversation_metrics": {{
            "talk_ratio": "rep_percentage:client_percentage",
            "emotional_connection": 1-10,
            "trust_building": 1-10
          }},
          "client_signals": {{
            "buying_signals": ["positive indicators"],
            "objections": ["concerns raised"],
            "engagement_level": 1-10
          }}
        }}

        Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Sales analysis error: {str(e)}")
            return self.get_fallback_sales_analysis()

    async def classify_archetype(self, psychological_profile, sales_performance):
        """Classify client into one of 5 archetypes using AI analysis"""

        prompt = f"""
        Based on this psychological and sales analysis, classify the client into one of these 5 archetypes:

        1. ANALYTICAL RESEARCHER - Data-driven, needs facts and logical arguments
        2. DESPERATE SAVER - High urgency, emotional, facing relationship crisis
        3. HOPEFUL BUILDER - Optimistic, growth-focused, future-oriented
        4. SKEPTICAL EVALUATOR - Cautious, needs proof and guarantees
        5. CONSENSUS SEEKER - Involves others, needs group approval

        PSYCHOLOGICAL PROFILE:
        {json.dumps(psychological_profile, indent=2)}

        SALES PERFORMANCE:
        {json.dumps(sales_performance, indent=2)}

        Respond with JSON:
        {{
          "primary_archetype": "exact archetype name from list above",
          "confidence_score": 0.0-1.0,
          "secondary_archetype": "second most likely archetype",
          "reasoning": "brief explanation of classification",
          "key_characteristics": ["3 key traits that led to this classification"]
        }}

        Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Archetype classification error: {str(e)}")
            return self.get_fallback_archetype()

    async def generate_coaching_recommendations(self, psychological_profile, sales_performance, archetype):
        """Generate actionable coaching recommendations"""

        archetype_name = archetype.get('primary_archetype', 'Mixed Profile')
        sales_score = sales_performance.get('overall_assessment', {}).get('performance_score', 50)

        prompt = f"""
        Generate specific coaching recommendations for this sales conversation.

        CLIENT ARCHETYPE: {archetype_name}
        SALES PERFORMANCE SCORE: {sales_score}/100

        Based on the analysis, provide actionable coaching in JSON format:
        {{
          "immediate_action_plan": {{
            "top_3_priorities": ["specific action items for next interaction"],
            "follow_up_timing": "1-2 days|3-5 days|1 week|2+ weeks",
            "follow_up_method": "email|phone|text|video",
            "key_message_focus": "primary theme for follow-up"
          }},
          "communication_strategy": {{
            "tone_adjustments": "specific tone recommendations",
            "language_style": "formal|conversational|empathetic|direct",
            "key_phrases_to_use": ["effective phrases for this archetype"],
            "topics_to_emphasize": ["important points to highlight"],
            "topics_to_avoid": ["sensitive areas to avoid"]
          }},
          "sales_technique_improvements": {{
            "discovery_improvements": ["better questions to ask"],
            "presentation_adjustments": ["how to present solutions"],
            "closing_recommendations": ["effective closing approaches"],
            "objection_handling": ["how to address likely concerns"]
          }}
        }}

        Focus on actionable, psychology-based recommendations. Respond with ONLY the JSON object.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()

            return json.loads(response_text)

        except Exception as e:
            logger.error(f"Coaching recommendations error: {str(e)}")
            return self.get_fallback_coaching()

    def calculate_success_probability(self, sales_performance, psychological_profile, archetype):
        """Calculate conversion probability based on analysis"""

        try:
            # Base score from sales performance
            base_score = sales_performance.get('overall_assessment', {}).get('performance_score', 50) / 100

            # Archetype confidence factor
            archetype_confidence = archetype.get('confidence_score', 0.5)

            # Emotional state factor
            emotional_state = psychological_profile.get('emotional_state', {})
            emotional_intensity = emotional_state.get('intensity', 5)
            emotional_factor = min(emotional_intensity / 10, 1.0)

            # Weighted calculation
            success_probability = (
                base_score * 0.6 +
                archetype_confidence * 0.2 +
                emotional_factor * 0.2
            )

            return min(max(success_probability, 0.1), 0.95)  # Keep between 10% and 95%

        except Exception as e:
            logger.error(f"Success probability calculation error: {str(e)}")
            return 0.5

    # Fallback methods for error handling
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
            "emotional_state": {"primary_emotion": "neutral", "intensity": 5, "stability": 5}
        }

    def get_fallback_sales_analysis(self):
        return {
            "overall_assessment": {
                "performance_score": 50,
                "grade": "C",
                "conversion_likelihood": 50,
                "key_strengths": ["analysis unavailable"],
                "improvement_areas": ["analysis unavailable"]
            },
            "skills_breakdown": {
                "rapport_building": {"score": 5, "feedback": "analysis unavailable"},
                "discovery_quality": {"score": 5, "feedback": "analysis unavailable"},
                "presentation": {"score": 5, "feedback": "analysis unavailable"},
                "objection_handling": {"score": 5, "feedback": "analysis unavailable"},
                "closing": {"score": 5, "feedback": "analysis unavailable"}
            }
        }

    def get_fallback_archetype(self):
        return {
            "primary_archetype": "Mixed Profile",
            "confidence_score": 0.5,
            "secondary_archetype": "Hopeful Builder",
            "reasoning": "analysis unavailable"
        }

    def get_fallback_coaching(self):
        return {
            "immediate_action_plan": {
                "top_3_priorities": ["follow up within 48 hours", "address main concerns", "provide additional value"],
                "follow_up_timing": "2-3 days",
                "follow_up_method": "email"
            }
        }

# Vercel serverless function handler
def handler(request):
    """Main Vercel serverless function entry point"""

    # Handle CORS for browser requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }

    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Method not allowed'})
        }

    try:
        # Get API key from environment
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'error': 'API key not configured',
                    'message': 'Please set ANTHROPIC_API_KEY environment variable'
                })
            }

        # Parse request body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Invalid JSON in request body'})
            }

        # Validate required fields
        if 'content' not in body:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing required field: content'})
            }

        content = body['content']
        filename = body.get('filename', 'transcript.txt')

        # Validate content
        if not content or len(content.strip()) < 100:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Content too short. Please provide at least 100 characters of transcript content.'})
            }

        # Initialize analyzer
        analyzer = ServerlessAnalyzer(api_key)

        # Run analysis
        result = asyncio.run(analyzer.analyze_transcript_content(content, filename))

        # Return results
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(result)
        }

    except Exception as e:
        logger.error(f"Serverless function error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    print("Enhanced Sales Analyzer - Serverless API endpoint")
    print("Deploy to Vercel for production use")