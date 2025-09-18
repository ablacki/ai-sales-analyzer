#!/usr/bin/env python3
"""
Enhanced Sales Call Analysis - Batch Processing Script
Processes marriage coaching sales transcripts using advanced AI psychological profiling
"""

import asyncio
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_analyzer import EnhancedSalesAnalyzer, process_transcript_batch, export_analysis_results

class AnalysisRunner:
    """Main orchestrator for running enhanced sales call analysis"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        self.analyzer = EnhancedSalesAnalyzer(self.api_key)
        self.transcript_dir = "Test Transcripts"
        self.results_dir = "enhanced_results"

        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)

    def get_transcript_files(self):
        """Get all transcript files to process"""
        transcript_path = Path(self.transcript_dir)

        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript directory '{self.transcript_dir}' not found")

        # Get all .txt files
        transcript_files = list(transcript_path.glob("*.txt"))

        if not transcript_files:
            raise FileNotFoundError(f"No .txt files found in '{self.transcript_dir}'")

        print(f"📁 Found {len(transcript_files)} transcript files to process")
        return [str(f) for f in transcript_files]

    async def run_analysis(self, max_files=None, batch_size=5):
        """Run enhanced analysis on transcript files"""

        print("🚀 Starting Enhanced Sales Call Analysis")
        print("=" * 60)

        try:
            # Get transcript files
            transcript_files = self.get_transcript_files()

            # Limit files if specified
            if max_files:
                transcript_files = transcript_files[:max_files]
                print(f"📊 Processing first {len(transcript_files)} files (limited by max_files={max_files})")

            # Process transcripts in batches
            print(f"⚙️  Processing {len(transcript_files)} transcripts in batches of {batch_size}")

            start_time = datetime.now()

            results = await process_transcript_batch(
                self.analyzer,
                transcript_files,
                batch_size=batch_size
            )

            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            # Process results
            successful_analyses = [r for r in results if r.get('status') == 'success']
            failed_analyses = [r for r in results if r.get('status') == 'failed']

            print("\n" + "=" * 60)
            print("📊 ANALYSIS COMPLETE")
            print("=" * 60)
            print(f"✅ Successfully analyzed: {len(successful_analyses)} transcripts")
            print(f"❌ Failed analyses: {len(failed_analyses)} transcripts")
            print(f"⏱️  Total processing time: {processing_time:.1f} seconds")
            print(f"📈 Average time per transcript: {processing_time/len(transcript_files):.1f} seconds")

            # Save detailed results
            await self.save_results(successful_analyses, failed_analyses)

            # Export to CSV/JSON
            print("\n📤 Exporting results...")
            export_analysis_results(self.analyzer.db_path, 'both')

            # Generate summary report
            self.generate_summary_report(successful_analyses)

            return successful_analyses

        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            self.analyzer.logger.error(f"Batch analysis failed: {str(e)}")
            raise

    async def save_results(self, successful_results, failed_results):
        """Save comprehensive results to files"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save successful analyses
        if successful_results:
            success_file = f"{self.results_dir}/successful_analyses_{timestamp}.json"
            with open(success_file, 'w', encoding='utf-8') as f:
                json.dump(successful_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Successful analyses saved: {success_file}")

        # Save failed analyses
        if failed_results:
            failed_file = f"{self.results_dir}/failed_analyses_{timestamp}.json"
            with open(failed_file, 'w', encoding='utf-8') as f:
                json.dump(failed_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"⚠️  Failed analyses saved: {failed_file}")

    def generate_summary_report(self, results):
        """Generate executive summary report"""

        if not results:
            print("⚠️  No successful results to summarize")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{self.results_dir}/executive_summary_{timestamp}.md"

        # Analyze results for summary
        total_transcripts = len(results)
        archetype_distribution = {}
        avg_sales_score = 0
        avg_success_probability = 0

        for result in results:
            # Archetype distribution
            archetype = result.get('archetype_analysis', {}).get('primary_archetype', 'Unknown')
            archetype_distribution[archetype] = archetype_distribution.get(archetype, 0) + 1

            # Average scores
            sales_score = result.get('sales_performance', {}).get('overall_assessment', {}).get('performance_score', 0)
            avg_sales_score += sales_score

            success_prob = result.get('success_probability', 0)
            avg_success_probability += success_prob

        avg_sales_score = avg_sales_score / total_transcripts if total_transcripts > 0 else 0
        avg_success_probability = avg_success_probability / total_transcripts if total_transcripts > 0 else 0

        # Generate report
        report_content = f"""# Enhanced Sales Call Analysis - Executive Summary

**Analysis Date**: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
**Total Transcripts Analyzed**: {total_transcripts}
**Analysis System**: Enhanced AI-Powered Psychological Profiling

---

## 📊 Key Performance Metrics

- **Average Sales Performance Score**: {avg_sales_score:.1f}/100
- **Average Success Probability**: {avg_success_probability:.1%}
- **Analysis Completion Rate**: {(total_transcripts / total_transcripts * 100):.1f}%

---

## 🎯 Client Archetype Distribution

"""

        for archetype, count in sorted(archetype_distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_transcripts) * 100
            report_content += f"- **{archetype}**: {count} clients ({percentage:.1f}%)\n"

        report_content += f"""

---

## 🔍 Analysis Insights

### Top Performing Sales Conversations
"""

        # Get top performers
        top_performers = sorted(results, key=lambda x: x.get('sales_performance', {}).get('overall_assessment', {}).get('performance_score', 0), reverse=True)[:3]

        for i, result in enumerate(top_performers, 1):
            transcript_id = result.get('transcript_id', 'Unknown')
            score = result.get('sales_performance', {}).get('overall_assessment', {}).get('performance_score', 0)
            archetype = result.get('archetype_analysis', {}).get('primary_archetype', 'Unknown')
            report_content += f"{i}. **{transcript_id}** - Score: {score}/100 - Archetype: {archetype}\n"

        report_content += f"""

### Areas for Improvement
Based on analysis of all {total_transcripts} conversations:

1. **Discovery Phase**: Focus on asking deeper, more insightful questions
2. **Emotional Connection**: Strengthen rapport building in opening minutes
3. **Objection Handling**: Develop archetype-specific objection responses
4. **Closing Effectiveness**: Practice assumptive and alternative choice closes

---

## 📈 Recommendations

### Immediate Actions
1. Review top-performing conversations for best practices
2. Implement archetype-specific coaching strategies
3. Focus training on lowest-scoring skill areas
4. Develop follow-up sequences based on psychological profiles

### Strategic Initiatives
1. Create archetype-based sales playbooks
2. Implement psychological profiling in CRM
3. Develop personality-matched coaching approaches
4. Build archetype-specific objection handling scripts

---

**Generated by Enhanced Sales Call Analyzer**
*AI-Powered Psychological Profiling for Marriage Coaching Sales*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📋 Executive summary report saved: {report_file}")

    async def analyze_single_transcript(self, transcript_path):
        """Analyze a single transcript file"""

        print(f"🔍 Analyzing single transcript: {transcript_path}")

        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()

            result = await self.analyzer.analyze_transcript(transcript_path, content)

            if result.get('status') == 'success':
                print("✅ Analysis completed successfully")

                # Print key insights
                archetype = result.get('archetype_analysis', {}).get('primary_archetype', 'Unknown')
                sales_score = result.get('sales_performance', {}).get('overall_assessment', {}).get('performance_score', 0)
                success_prob = result.get('success_probability', 0)

                print(f"🎯 Client Archetype: {archetype}")
                print(f"📊 Sales Performance: {sales_score}/100")
                print(f"📈 Success Probability: {success_prob:.1%}")

                # Save single result
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                result_file = f"{self.results_dir}/single_analysis_{timestamp}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                print(f"💾 Results saved: {result_file}")

                return result
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"❌ Error analyzing transcript: {str(e)}")
            return None

async def main():
    """Main entry point for enhanced analysis"""

    try:
        runner = AnalysisRunner()

        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == 'single' and len(sys.argv) > 2:
                # Analyze single file
                transcript_path = sys.argv[2]
                await runner.analyze_single_transcript(transcript_path)
            elif sys.argv[1] == 'batch':
                # Batch analysis with optional parameters
                max_files = int(sys.argv[2]) if len(sys.argv) > 2 else None
                batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 5
                await runner.run_analysis(max_files=max_files, batch_size=batch_size)
            else:
                print("Usage:")
                print("  python run_enhanced_analysis.py batch [max_files] [batch_size]")
                print("  python run_enhanced_analysis.py single <transcript_path>")
                sys.exit(1)
        else:
            # Default: run batch analysis on all files
            await runner.run_analysis()

    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Enhanced Sales Call Analyzer")
    print("AI-Powered Psychological Profiling for Marriage Coaching Sales")
    print("=" * 60)

    # Run the async main function
    asyncio.run(main())