"""
Enhanced Marriage Coaching Sales Call Analyzer
Surgical analysis for marriage coaching sales with empathetic confrontation tracking
"""

import json
import os
import asyncio
from datetime import datetime
import logging
from http.server import BaseHTTPRequestHandler

try:
    from anthropic import AsyncAnthropic
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarriageCoachingAnalyzer:
    """Surgical marriage coaching sales analyzer with framework from proven systems"""

    def __init__(self, api_key):
        self.client = AsyncAnthropic(api_key=api_key)

    async def analyze_marriage_coaching_call(self, content, filename="transcript.txt"):
        """Complete marriage coaching sales analysis"""

        try:
            if len(content) > 12000:
                content = content[:12000] + "... [Content truncated for analysis]"

            # Run comprehensive analysis
            sales_framework_analysis = await self.analyze_sales_framework(content)
            psychological_analysis = await self.analyze_psychological_profile(content)
            marriage_specific_analysis = await self.analyze_marriage_coaching_specifics(content)
            emotional_journey = await self.analyze_emotional_journey(content)
            archetype_classification = await self.classify_marriage_archetype(content)
            talk_track_improvements = await self.analyze_talk_track_improvements(content, sales_framework_analysis, marriage_specific_analysis)

            return {
                'transcript_id': filename,
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'success',
                'word_count': len(content.split()),

                # Core analyses
                'sales_framework_analysis': sales_framework_analysis,
                'psychological_profile': psychological_analysis,
                'marriage_coaching_analysis': marriage_specific_analysis,
                'emotional_journey': emotional_journey,
                'archetype_analysis': archetype_classification,
                'talk_track_improvements': talk_track_improvements,

                # Calculated metrics
                'success_probability': self.calculate_marriage_success_probability(
                    sales_framework_analysis, marriage_specific_analysis, archetype_classification
                )
            }

        except Exception as e:
            logger.error(f"Marriage coaching analysis failed: {str(e)}")
            return {
                'transcript_id': filename,
                'status': 'error',
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }

    async def analyze_sales_framework(self, content):
        """Apply the proven 6-category sales framework"""

        prompt = f"""
        You are a savage Sales Manager analyzing this marriage coaching sales call using the proven 6-category framework.

        TRANSCRIPT:
        {content}

        Analyze using the Marriage Coaching Sales Framework with surgical precision:

        {{
          "framework_scores": {{
            "call_control": {{
              "score": 1-10,
              "analysis": "How well did rep maintain control and guide the conversation?",
              "what_worked": ["specific examples with quotes"],
              "what_needed_improvement": ["specific areas with quotes"],
              "coaching_fix": "Specific script/technique for improvement"
            }},
            "discovery_depth": {{
              "score": 1-10,
              "analysis": "Quality of information gathering about marriage problems",
              "what_worked": ["good discovery questions asked"],
              "what_needed_improvement": ["missing discovery areas"],
              "coaching_fix": "Specific questions to ask next time"
            }},
            "empathetic_confrontation": {{
              "score": 1-10,
              "analysis": "Balance of empathy while showing prospect his role in problems",
              "what_worked": ["moments of effective confrontation"],
              "what_needed_improvement": ["missed confrontation opportunities"],
              "coaching_fix": "Scripts for empathetic confrontation"
            }},
            "objection_handling": {{
              "score": 1-10,
              "analysis": "Effectiveness handling money and relationship objections",
              "objections_encountered": [{{ "objection": "quote", "response": "rep response", "effectiveness": 1-10 }}],
              "what_worked": ["effective responses"],
              "what_needed_improvement": ["poor responses"],
              "coaching_fix": "Better objection handling scripts"
            }},
            "value_positioning": {{
              "score": 1-10,
              "analysis": "How well positioned marriage value vs program cost",
              "marriage_vs_cost_effectiveness": {{
                "marriage_value_examples": ["quotes showing marriage positioned as valuable"],
                "cost_justification_examples": ["quotes showing cost as investment not expense"],
                "tesla_analogy_usage": {{ "used": true/false, "effectiveness": 1-10, "quote": "actual usage" }},
                "beg_borrow_steal_positioning": {{ "used": true/false, "effectiveness": 1-10, "quote": "actual usage" }},
                "divorce_cost_comparison": {{ "mentioned": true/false, "effectiveness": 1-10 }},
                "future_happiness_value": {{ "positioned": true/false, "effectiveness": 1-10 }}
              }},
              "price_objection_handling": {{
                "objections_encountered": [{{ "objection": "specific price concern", "response": "rep response", "effectiveness": 1-10 }}],
                "missed_reframes": ["opportunities to reframe price as investment"]
              }},
              "what_worked": ["effective value positioning moments"],
              "what_needed_improvement": ["missed value opportunities with specific quotes"],
              "coaching_fix": "Specific value positioning scripts and reframes"
            }},
            "closing_strength": {{
              "score": 1-10,
              "analysis": "Effectiveness of asking for commitment",
              "what_worked": ["strong closing moments"],
              "what_needed_improvement": ["weak closing attempts"],
              "coaching_fix": "Better closing techniques"
            }}
          }},
          "total_score": "sum of all 6 scores out of 60",
          "overall_grade": "A|B|C|D|F based on total score"
        }}

        Be surgical and specific. Include exact quotes when possible. Focus on marriage coaching sales specifics.

        Respond with ONLY the JSON object.
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
            logger.error(f"Sales framework analysis error: {str(e)}")
            return self.get_fallback_sales_framework()

    async def analyze_psychological_profile(self, content):
        """Big Five personality analysis for marriage coaching prospects"""

        prompt = f"""
        Analyze this marriage coaching prospect's psychological profile using Big Five personality traits.

        TRANSCRIPT:
        {content}

        Provide Big Five personality analysis in JSON format:
        {{
          "big_five_personality": {{
            "openness": {{
              "score": 1-100,
              "confidence": 80,
              "implications": "How this affects their receptiveness to marriage coaching approach"
            }},
            "conscientiousness": {{
              "score": 1-100,
              "confidence": 85,
              "implications": "Follow-through likelihood and structure needs for marriage work"
            }},
            "extraversion": {{
              "score": 1-100,
              "confidence": 75,
              "implications": "Communication style and social approach to marriage issues"
            }},
            "agreeableness": {{
              "score": 1-100,
              "confidence": 85,
              "implications": "Cooperation level and conflict handling in marriage context"
            }},
            "neuroticism": {{
              "score": 1-100,
              "confidence": 80,
              "implications": "Emotional stability and stress management in marriage crisis"
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

        Focus on marriage-specific psychological insights that will help position coaching effectively.

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

    async def analyze_marriage_coaching_specifics(self, content):
        """Marriage coaching specific analysis"""

        prompt = f"""
        Analyze this marriage coaching sales call for marriage-specific elements and coaching effectiveness.

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
            logger.error(f"Marriage coaching analysis error: {str(e)}")
            return self.get_fallback_marriage_analysis()

    async def analyze_emotional_journey(self, content):
        """Track emotional journey throughout the call"""

        prompt = f"""
        Map the emotional journey of this prospect throughout the marriage coaching sales call.

        TRANSCRIPT:
        {content}

        Analyze the emotional journey:

        {{
          "emotional_journey_phases": [
            {{
              "phase": "opening|discovery|problem_identification|value_building|objection_handling|closing",
              "emotional_state": "hopeful|desperate|defensive|angry|resigned|motivated|skeptical|curious",
              "intensity": 1-10,
              "trigger_moment": "specific quote or moment that caused this emotion",
              "rep_response_to_emotion": "how rep handled this emotional state",
              "rep_response_effectiveness": 1-10,
              "coaching_note": "how rep should have handled this emotion better"
            }}
          ],
          "emotional_patterns": {{
            "dominant_emotion": "primary emotion throughout call",
            "emotional_shifts": ["key moments where emotion changed"],
            "emotional_resistance_points": ["moments of highest resistance"],
            "emotional_connection_points": ["moments of highest connection"],
            "missed_emotional_opportunities": ["emotions rep failed to address"]
          }},
          "emotional_coaching_strategy": {{
            "next_call_emotional_approach": "how to approach emotions in next interaction",
            "emotional_triggers_to_avoid": ["things that caused negative emotions"],
            "emotional_bridges_to_build": ["ways to create positive emotional connection"],
            "emotional_closing_strategy": "how to use emotions for closing"
          }}
        }}

        Focus on marriage-specific emotions: desperation about relationship, hope for saving marriage, fear of divorce, anger at situation.

        Respond with ONLY the JSON object.
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
            logger.error(f"Emotional journey analysis error: {str(e)}")
            return self.get_fallback_emotional_journey()

    async def classify_marriage_archetype(self, content):
        """Classify into marriage coaching specific archetypes"""

        prompt = f"""
        Classify this prospect into one of the 5 marriage coaching archetypes based on the conversation.

        TRANSCRIPT:
        {content}

        Marriage Coaching Archetypes:
        1. ANALYTICAL RESEARCHER - Data-driven, needs facts about success rates and methodology
        2. DESPERATE SAVER - High urgency, emotional, facing imminent divorce or separation
        3. HOPEFUL BUILDER - Optimistic, growth-focused, believes marriage can be better
        4. SKEPTICAL EVALUATOR - Cautious, needs proof programs work, worried about scams
        5. CONSENSUS SEEKER - Needs wife's buy-in, involves others in decision-making

        Provide archetype analysis:

        {{
          "primary_archetype": "exact archetype name from list above",
          "confidence_score": 0.0-1.0,
          "secondary_archetype": "second most likely archetype",
          "archetype_evidence": {{
            "supporting_quotes": ["specific quotes supporting this classification"],
            "behavioral_indicators": ["behaviors that indicate this archetype"],
            "decision_making_style": "how they approach decisions based on conversation"
          }},
          "archetype_coaching_strategy": {{
            "optimal_approach": "best sales approach for this archetype",
            "key_motivators": ["what drives this archetype to buy"],
            "objection_patterns": ["typical objections this archetype raises"],
            "closing_strategy": "most effective closing approach",
            "follow_up_approach": "how to follow up with this archetype"
          }},
          "pre_call_validation": {{
            "recommended_questions": [
              "What would you need to see to know this program could save your marriage?",
              "On a scale of 1-10, how urgent is getting help for your marriage right now?",
              "How does your wife feel about getting outside help for the relationship?",
              "What's the biggest challenge in your marriage that you're hoping to solve?",
              "Have you tried marriage counseling before? What was that experience like?",
              "If money wasn't an issue, would you do whatever it takes to save your marriage?",
              "What happens if nothing changes in your relationship over the next 6 months?",
              "Who else would be involved in making this decision besides you?",
              "What's your biggest concern about programs like this?",
              "How much research have you done on marriage coaching programs so far?"
            ],
            "archetype_accuracy_prediction": 1-10,
            "pre_call_archetype_identification": {{
              "analytical_researcher_indicators": ["asks for success rates", "wants detailed methodology", "mentions research"],
              "desperate_saver_indicators": ["high urgency score (8-10)", "mentions separation/divorce timeline", "emotional language"],
              "hopeful_builder_indicators": ["growth-focused language", "optimistic about future", "mentions building together"],
              "skeptical_evaluator_indicators": ["mentions scams", "wants guarantees", "previous bad experiences"],
              "consensus_seeker_indicators": ["mentions wife's opinion", "involves others", "needs approval"]
            }}
          }},
          "archetype_specific_scripts": {{
            "opening_script": "tailored opening for this archetype",
            "discovery_questions": ["archetype-specific discovery questions"],
            "value_positioning": "how to position value for this archetype",
            "objection_responses": ["responses to this archetype's typical objections"],
            "closing_script": "closing approach for this archetype"
          }}
        }}

        Be specific about marriage coaching archetype identification and pre-call question recommendations.

        Respond with ONLY the JSON object.
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
            logger.error(f"Archetype classification error: {str(e)}")
            return self.get_fallback_archetype()

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
            logger.error(f"Talk track analysis error: {str(e)}")
            return self.get_fallback_talk_track()

    def calculate_marriage_success_probability(self, sales_framework, marriage_analysis, archetype):
        """Calculate close probability based on marriage coaching factors"""

        try:
            # Base score from sales framework (out of 60)
            framework_score = sales_framework.get('framework_scores', {})
            total_framework_score = 0

            for category in ['call_control', 'discovery_depth', 'empathetic_confrontation',
                           'objection_handling', 'value_positioning', 'closing_strength']:
                total_framework_score += framework_score.get(category, {}).get('score', 5)

            base_score = total_framework_score / 60  # Normalize to 0-1

            # Marriage-specific factors
            marriage_factors = marriage_analysis.get('marriage_situation_assessment', {})
            urgency_level = marriage_factors.get('urgency_level', 5) / 10
            emotional_readiness = 0.7  # Default

            if marriage_factors.get('emotional_state') == 'desperate':
                emotional_readiness = 0.9
            elif marriage_factors.get('emotional_state') == 'hopeful':
                emotional_readiness = 0.8
            elif marriage_factors.get('emotional_state') == 'angry':
                emotional_readiness = 0.4

            # Archetype confidence factor
            archetype_confidence = archetype.get('confidence_score', 0.5)

            # Weighted calculation for marriage coaching
            success_probability = (
                base_score * 0.5 +           # Sales framework performance
                urgency_level * 0.2 +        # Urgency of marriage situation
                emotional_readiness * 0.2 +  # Emotional state
                archetype_confidence * 0.1   # Archetype match confidence
            )

            return min(max(success_probability, 0.05), 0.95)

        except Exception as e:
            logger.error(f"Success probability calculation error: {str(e)}")
            return 0.5

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

            analyzer = MarriageCoachingAnalyzer(api_key)
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