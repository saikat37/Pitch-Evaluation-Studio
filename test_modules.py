"""Quick module test to verify all imports and basic functionality."""
import sys

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing module imports...")
    
    try:
        import audio
        print("✅ audio.py")
    except Exception as e:
        print(f"❌ audio.py: {e}")
        return False
    
    try:
        import transcribe
        print("✅ transcribe.py")
    except Exception as e:
        print(f"❌ transcribe.py: {e}")
        return False
    
    try:
        import tone
        print("✅ tone.py")
    except Exception as e:
        print(f"❌ tone.py: {e}")
        return False
    
    try:
        import parsers
        print("✅ parsers.py")
    except Exception as e:
        print(f"❌ parsers.py: {e}")
        return False
    
    try:
        import prompts
        print("✅ prompts.py")
    except Exception as e:
        print(f"❌ prompts.py: {e}")
        return False
    
    try:
        import main
        print("✅ main.py")
    except Exception as e:
        print(f"❌ main.py: {e}")
        return False
    
    try:
        import agents
        print("✅ agents.py")
    except Exception as e:
        print(f"❌ agents.py: {e}")
        return False
    
    try:
        import pipeline
        print("✅ pipeline.py")
    except Exception as e:
        print(f"❌ pipeline.py: {e}")
        return False
    
    return True


def test_env():
    """Test that environment is properly configured."""
    print("\n🔧 Testing environment configuration...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and len(api_key) > 10:
        print("✅ GROQ_API_KEY is set")
        return True
    else:
        print("❌ GROQ_API_KEY not found or invalid in .env")
        return False


def test_models():
    """Test that core models are accessible."""
    print("\n🤖 Testing model schemas...")
    
    try:
        from parsers import ScoreReason, PitchStructureResult, BusinessViabilityResult
        
        # Test instantiation
        score = ScoreReason(score=85, reason="Test reason")
        print(f"✅ ScoreReason: {score.score}/100")
        
        structure = PitchStructureResult(
            hook_present=True,
            problem_present=True,
            solution_present=True,
            ask_present=True,
            detected_order=["hook", "problem", "solution", "ask"],
            structure_quality_score=90,
            structure_comment="Test"
        )
        print(f"✅ PitchStructureResult: {structure.structure_quality_score}/100")
        
        viability = BusinessViabilityResult(
            score=75,
            risk_level="medium",
            summary_comment="Test",
            key_strengths=["Strong problem"],
            key_risks=["Unclear revenue"]
        )
        print(f"✅ BusinessViabilityResult: {viability.score}/100, Risk: {viability.risk_level}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Pitch Evaluation - Module Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test environment
    results.append(("Environment", test_env()))
    
    # Test models
    results.append(("Models", test_models()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! You're ready to run the app.")
        print("\nRun: streamlit run app.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
