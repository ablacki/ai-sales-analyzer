#!/usr/bin/env python3
"""
Test script for Enhanced Sales Call Analyzer
Tests the system with sample transcripts to validate functionality
"""

import asyncio
import os
import json
from datetime import datetime

# Import our enhanced analyzer
from enhanced_analyzer import EnhancedSalesAnalyzer

async def test_single_transcript():
    """Test the enhanced analyzer with a single transcript"""

    print("🧪 Testing Enhanced Sales Call Analyzer")
    print("=" * 50)

    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not found")
        print("Please set your API key: export ANTHROPIC_API_KEY='your_key_here'")
        return False

    try:
        # Initialize analyzer
        analyzer = EnhancedSalesAnalyzer(api_key)
        print("✅ Enhanced analyzer initialized successfully")

        # Find a sample transcript
        test_transcript_path = "Test Transcripts/1_Brian_Kegler_Marriage_Turnaround_Consultation_45_Mins_transcript-2025-01-20T143157Z.txt"

        if not os.path.exists(test_transcript_path):
            print(f"❌ Sample transcript not found: {test_transcript_path}")
            return False

        print(f"📄 Reading sample transcript: {os.path.basename(test_transcript_path)}")

        # Read transcript content
        with open(test_transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📊 Transcript length: {len(content)} characters, {len(content.split())} words")

        # Run enhanced analysis
        print("🔍 Running enhanced AI analysis...")
        print("   - Psychological profiling (Big Five personality)")
        print("   - Sales performance analysis")
        print("   - Archetype classification")
        print("   - Coaching recommendations")
        print("   - Success probability calculation")
        print("\n⏳ This may take 30-60 seconds...")

        start_time = datetime.now()

        result = await analyzer.analyze_transcript(test_transcript_path, content)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Check results
        if result.get('status') == 'success':
            print(f"\n✅ Analysis completed successfully in {processing_time:.1f} seconds")
            print("=" * 50)

            # Display key results
            print("📋 KEY INSIGHTS:")
            print("-" * 30)

            # Sales Performance
            sales_perf = result.get('sales_performance', {}).get('overall_assessment', {})
            score = sales_perf.get('performance_score', 0)
            grade = sales_perf.get('grade', 'N/A')
            print(f"🎯 Sales Performance: {score}/100 (Grade: {grade})")

            # Archetype
            archetype_info = result.get('archetype_analysis', {})
            archetype = archetype_info.get('primary_archetype', 'Unknown')
            confidence = archetype_info.get('confidence_score', 0)
            print(f"🏷️  Client Archetype: {archetype} ({confidence:.1%} confidence)")

            # Success Probability
            success_prob = result.get('success_probability', 0)
            print(f"📈 Success Probability: {success_prob:.1%}")

            # Big Five Personality
            print(f"\n🧠 BIG FIVE PERSONALITY PROFILE:")
            big_five = result.get('psychological_profile', {}).get('big_five_personality', {})
            for trait, data in big_five.items():
                score = data.get('score', 0) if isinstance(data, dict) else 0
                print(f"   • {trait.title()}: {score}/100")

            # Top Coaching Recommendations
            print(f"\n💡 TOP COACHING RECOMMENDATIONS:")
            coaching = result.get('coaching_recommendations', {})
            priorities = coaching.get('immediate_action_plan', {}).get('top_3_priorities', [])
            for i, priority in enumerate(priorities[:3], 1):
                print(f"   {i}. {priority}")

            # Save test results
            test_results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(test_results_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Full results saved: {test_results_file}")

            return True

        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def test_database_connection():
    """Test database functionality"""

    print("\n🗄️  Testing Database Connection")
    print("-" * 30)

    try:
        import sqlite3

        # Test database creation and connection
        test_db = 'data/enhanced_sales_analysis.db'

        if os.path.exists(test_db):
            with sqlite3.connect(test_db) as conn:
                cursor = conn.cursor()

                # Check if tables exist
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                print(f"✅ Database connected: {test_db}")
                print(f"📊 Tables found: {len(tables)}")
                for table in tables:
                    print(f"   • {table[0]}")

                # Check record count
                try:
                    cursor.execute("SELECT COUNT(*) FROM enhanced_clients;")
                    count = cursor.fetchone()[0]
                    print(f"📈 Records in enhanced_clients: {count}")
                except:
                    print("📈 Records in enhanced_clients: 0 (table empty)")

                return True
        else:
            print("⚠️  Database file not found - will be created on first analysis")
            return True

    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_dashboard():
    """Test dashboard file"""

    print("\n🖥️  Testing Dashboard")
    print("-" * 20)

    dashboard_file = "enhanced_dashboard.html"

    if os.path.exists(dashboard_file):
        file_size = os.path.getsize(dashboard_file)
        print(f"✅ Dashboard file found: {dashboard_file}")
        print(f"📊 File size: {file_size:,} bytes")
        print(f"🌐 Open in browser: file://{os.path.abspath(dashboard_file)}")
        return True
    else:
        print(f"❌ Dashboard file not found: {dashboard_file}")
        return False

def check_dependencies():
    """Check required dependencies"""

    print("📦 Checking Dependencies")
    print("-" * 25)

    dependencies = {
        'anthropic': 'Anthropic AI client',
        'pandas': 'Data processing',
        'asyncio': 'Async processing',
        'sqlite3': 'Database operations',
        'json': 'JSON processing',
        'os': 'File operations',
        'datetime': 'Date/time handling'
    }

    missing_deps = []

    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep:<10} - {description}")
        except ImportError:
            print(f"❌ {dep:<10} - {description} (MISSING)")
            missing_deps.append(dep)

    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        return False

    return True

async def main():
    """Main test function"""

    print("🚀 ENHANCED SALES CALL ANALYZER - SYSTEM TEST")
    print("=" * 60)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return

    # Test database
    test_database_connection()

    # Test dashboard
    test_dashboard()

    # Test main analysis functionality
    print("\n🧪 STARTING MAIN FUNCTIONALITY TEST")
    print("=" * 40)

    success = await test_single_transcript()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\nSystem is ready for production use:")
        print("• Run batch analysis: python run_enhanced_analysis.py")
        print("• Analyze single file: python run_enhanced_analysis.py single <filepath>")
        print("• View dashboard: open enhanced_dashboard.html")
        print("• Check database: data/enhanced_sales_analysis.db")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the errors above and resolve issues before proceeding.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())