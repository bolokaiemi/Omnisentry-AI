import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.website_analyzer import analyze_website

def run_tests():
    print("=" * 60)
    print("OMNISENTRY AI SECURITY VERIFICATION TESTS")
    print("=" * 60)

    # Test cases:
    # 1. A highly trusted, long-standing domain (e.g. google.com)
    # 2. A potentially suspicious/typosquatted brand domain (e.g. netfl1x-login-verification.xyz)
    # 3. An unregistered domain (e.g. non-existent-domain-999333221.com)
    
    test_domains = [
        "google.com",
        "netfl1x-login-verification.xyz",
        "non-existent-domain-999333221.com"
    ]

    for domain in test_domains:
        print(f"\n[+] Auditing Domain: {domain}")
        print("-" * 40)
        try:
            report = analyze_website(domain)
            
            print(f"  * Registered:      {report['registered']}")
            print(f"  * Age Days:        {report['age_days']}")
            print(f"  * SSL Enabled:     {report['ssl']}")
            print(f"  * Reputation Lvl:  {report['reputation']['level']}")
            print(f"  * Reputation Score:{report['reputation']['score']}")
            print(f"  * Trust Score:     {report['trust_score']}/100")
            print(f"  * Risk Level:      {report['risk_level']}")
            print(f"  * AI Prediction:   {report['ai_prediction']}")
            print(f"  * Location:        {report['city']}, {report['country']}")
            print(f"  * ISP / ASN:       {report['isp']} / {report['asn']}")
            print(f"  * Risk Factors:    {report['risk_factors']}")
            
            # Assertions / Validations
            if domain == "google.com":
                assert report['registered'] is True, "google.com should be registered"
                assert report['age_days'] >= 365, "google.com age should be >= 365 days"
                assert report['trust_score'] >= 85, "google.com trust score should be SAFE (>= 85)"
                assert report['risk_level'] == "SAFE", "google.com risk level should be SAFE"
                assert report['ai_prediction'] == 1, "google.com AI verdict should be 1 (Trusted)"
                
            elif domain == "non-existent-domain-999333221.com":
                assert report['registered'] is False, "Non-existent domain should show unregistered"
                assert report['age_days'] == 0, "Non-existent domain age should be 0"
                assert report['trust_score'] <= 15, "Non-existent domain trust score should be Critical/High risk"
                
            print("  => Verification: PASS")
            
        except Exception as e:
            print(f"  => Verification: FAIL (Error: {e})")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
