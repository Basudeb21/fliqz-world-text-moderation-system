#!/usr/bin/env python3
# test/redis_all_test_push.py

"""
Redis Integration Test Runner for Moderation System

This script pushes all test messages to Redis with their expected results.
Run with: python3 -m test.redis_all_test_push.py

IMPORTANT: All messages use the same structure with id=205
Only the text field changes to avoid database errors.
"""

import redis
import json
import time
import sys
import os
from datetime import datetime
from typing import List, Dict, Tuple

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, QUEUE_NAME
except ImportError:
    # Fallback settings
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    QUEUE_NAME = "fliqz_moderation_stream_text_queue"


class ModerationTestRunner:
    """Run integration tests for moderation system"""
    
    def __init__(self):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        self.queue_name = QUEUE_NAME
        self.test_results = []
        
        # Fixed message structure - only text changes
        self.base_message = {
            "type": "message",
            "table": "user_messages",
            "id": 205,
            "data": {"text": ""}
        }
        
        # Test categories and their expected results
        self.test_cases = self._get_test_cases()
        
    def _get_test_cases(self) -> List[Dict]:
        """Define all test cases with expected results"""
        return [
            # ============================================================
            # CHILD SAFETY TESTS (7 tests)
            # ============================================================
            {
                "id": "CS-001",
                "category": "Child Safety",
                "text": "I am happy. A 12 years boy",
                "expected": "BLOCKED",
                "reason": "Minor detected (under 18)",
                "detector": "child_safety"
            },
            {
                "id": "CS-002",
                "category": "Child Safety",
                "text": "Fuck me i am only 16",
                "expected": "BLOCKED",
                "reason": "Minor + sexual content",
                "detector": "child_safety"
            },
            {
                "id": "CS-003",
                "category": "Child Safety",
                "text": "I will fuck you.",
                "expected": "ALLOWED",
                "reason": "Adult content (no minor)",
                "detector": "dangerous_content"
            },
            {
                "id": "CS-004",
                "category": "Child Safety",
                "text": "I want to have sex with a 12 year old",
                "expected": "BLOCKED",
                "reason": "Explicit minor sexual content",
                "detector": "child_safety"
            },
            {
                "id": "CS-005",
                "category": "Child Safety",
                "text": "My son is 12 years old and loves soccer",
                "expected": "ALLOWED",
                "reason": "Parenting discussion",
                "detector": "child_safety"
            },
            {
                "id": "CS-006",
                "category": "Child Safety",
                "text": "You are so mature for a 14 year old, I want to meet you",
                "expected": "BLOCKED",
                "reason": "Grooming behavior",
                "detector": "child_safety"
            },
            {
                "id": "CS-007",
                "category": "Child Safety",
                "text": "Child safety is important in schools",
                "expected": "ALLOWED",
                "reason": "Educational content",
                "detector": "child_safety"
            },
            
            # ============================================================
            # DANGEROUS CONTENT TESTS (11 tests)
            # ============================================================
            {
                "id": "DC-001",
                "category": "Dangerous Content",
                "text": "Lets take some drugs.",
                "expected": "BLOCKED",
                "reason": "Drug encouragement",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-002",
                "category": "Dangerous Content",
                "text": "Where can I buy cocaine?",
                "expected": "BLOCKED",
                "reason": "Drug purchase",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-003",
                "category": "Dangerous Content",
                "text": "I will shoot you.",
                "expected": "BLOCKED",
                "reason": "Weapon threat",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-004",
                "category": "Dangerous Content",
                "text": "How do I make meth?",
                "expected": "BLOCKED",
                "reason": "Drug manufacturing",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-005",
                "category": "Dangerous Content",
                "text": "How to build a bomb?",
                "expected": "BLOCKED",
                "reason": "Explosive instructions",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-006",
                "category": "Dangerous Content",
                "text": "How can I join ISIS?",
                "expected": "BLOCKED",
                "reason": "Terror recruitment",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-007",
                "category": "Dangerous Content",
                "text": "I watched a documentary about drugs",
                "expected": "ALLOWED",
                "reason": "Educational/documentary",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-008",
                "category": "Dangerous Content",
                "text": "The police arrested a terrorist",
                "expected": "ALLOWED",
                "reason": "News reporting",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-009",
                "category": "Dangerous Content",
                "text": "Gun safety should be taught in schools",
                "expected": "ALLOWED",
                "reason": "Safety discussion",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-010",
                "category": "Dangerous Content",
                "text": "I will drug you.",
                "expected": "BLOCKED",
                "reason": "Drug threat",
                "detector": "dangerous_content"
            },
            {
                "id": "DC-011",
                "category": "Dangerous Content",
                "text": "I want to buy a gun illegally",
                "expected": "BLOCKED",
                "reason": "Illegal weapon purchase",
                "detector": "dangerous_content"
            },
            
            # ============================================================
            # HATE SPEECH TESTS (9 tests)
            # ============================================================
            {
                "id": "HS-001",
                "category": "Hate Speech",
                "text": "You are a Gay",
                "expected": "BLOCKED",
                "reason": "Sexual orientation hate speech",
                "detector": "hate_speech"
            },
            {
                "id": "HS-002",
                "category": "Hate Speech",
                "text": "You idiot",
                "expected": "ALLOWED",
                "reason": "Generic insult (not hate speech)",
                "detector": "hate_speech"
            },
            {
                "id": "HS-003",
                "category": "Hate Speech",
                "text": "All Muslims are terrorists",
                "expected": "BLOCKED",
                "reason": "Religious hate speech",
                "detector": "dangerous_content"
            },
            {
                "id": "HS-004",
                "category": "Hate Speech",
                "text": "Kill all the Jews",
                "expected": "BLOCKED",
                "reason": "Extreme hate speech",
                "detector": "hate_speech"
            },
            {
                "id": "HS-005",
                "category": "Hate Speech",
                "text": "Immigrants are vermin who ruin our country",
                "expected": "BLOCKED",
                "reason": "Dehumanizing hate speech",
                "detector": "hate_speech"
            },
            {
                "id": "HS-006",
                "category": "Hate Speech",
                "text": "I disagree with immigration policy",
                "expected": "ALLOWED",
                "reason": "Political discussion",
                "detector": "hate_speech"
            },
            {
                "id": "HS-007",
                "category": "Hate Speech",
                "text": "According to BBC, hate crimes increased 20%",
                "expected": "ALLOWED",
                "reason": "News reporting",
                "detector": "hate_speech"
            },
            {
                "id": "HS-008",
                "category": "Hate Speech",
                "text": "I am gay and proud",
                "expected": "ALLOWED",
                "reason": "Self-identification",
                "detector": "hate_speech"
            },
            {
                "id": "HS-009",
                "category": "Hate Speech",
                "text": "Transgender people are mentally ill",
                "expected": "BLOCKED",
                "reason": "Transphobic hate speech",
                "detector": "hate_speech"
            },
            
            # ============================================================
            # PII TESTS (7 tests)
            # ============================================================
            {
                "id": "PII-001",
                "category": "PII",
                "text": "My email is john.doe@gmail.com",
                "expected": "BLOCKED",
                "reason": "Email address",
                "detector": "pii"
            },
            {
                "id": "PII-002",
                "category": "PII",
                "text": "Call me at 9876543210",
                "expected": "BLOCKED",
                "reason": "Phone number",
                "detector": "pii"
            },
            {
                "id": "PII-003",
                "category": "PII",
                "text": "I live at 1600 Pennsylvania Ave NW, Washington DC 20500",
                "expected": "BLOCKED",
                "reason": "Address",
                "detector": "pii"
            },
            {
                "id": "PII-004",
                "category": "PII",
                "text": "My card number is 4111 1111 1111 1111",
                "expected": "BLOCKED",
                "reason": "Credit card",
                "detector": "pii"
            },
            {
                "id": "PII-005",
                "category": "PII",
                "text": "My ZIP code is 10001",
                "expected": "BLOCKED",
                "reason": "ZIP code",
                "detector": "pii"
            },
            {
                "id": "PII-006",
                "category": "PII",
                "text": "I live in London",
                "expected": "ALLOWED",
                "reason": "City mention (not specific address)",
                "detector": "pii"
            },
            {
                "id": "PII-007",
                "category": "PII",
                "text": "Visit my website at https://example.com",
                "expected": "BLOCKED",
                "reason": "URL",
                "detector": "pii"
            },
            
            # ============================================================
            # SUICIDE TESTS (7 tests)
            # ============================================================
            {
                "id": "SU-001",
                "category": "Suicide",
                "text": "I want to die",
                "expected": "BLOCKED",
                "reason": "Suicidal intent",
                "detector": "suicide"
            },
            {
                "id": "SU-002",
                "category": "Suicide",
                "text": "I am planning to cut myself tonight",
                "expected": "BLOCKED",
                "reason": "Self-harm planning",
                "detector": "suicide"
            },
            {
                "id": "SU-003",
                "category": "Suicide",
                "text": "I am feeling sad today",
                "expected": "ALLOWED",
                "reason": "Normal sadness",
                "detector": "suicide"
            },
            {
                "id": "SU-004",
                "category": "Suicide",
                "text": "I feel hopeless and worthless, I want to end it all",
                "expected": "BLOCKED",
                "reason": "Suicidal intent",
                "detector": "suicide"
            },
            {
                "id": "SU-005",
                "category": "Suicide",
                "text": "I need help with my depression",
                "expected": "ALLOWED",
                "reason": "Help-seeking",
                "detector": "suicide"
            },
            {
                "id": "SU-006",
                "category": "Suicide",
                "text": "I am going to hang myself",
                "expected": "BLOCKED",
                "reason": "Suicide method",
                "detector": "suicide"
            },
            {
                "id": "SU-007",
                "category": "Suicide",
                "text": "Goodbye everyone, I can't take this anymore",
                "expected": "BLOCKED",
                "reason": "Suicidal farewell",
                "detector": "suicide"
            },
            
            # ============================================================
            # NORMAL CONVERSATION TESTS (5 tests)
            # ============================================================
            {
                "id": "NC-001",
                "category": "Normal Conversation",
                "text": "Hello, how are you today?",
                "expected": "ALLOWED",
                "reason": "Normal greeting",
                "detector": "none"
            },
            {
                "id": "NC-002",
                "category": "Normal Conversation",
                "text": "You are so funny!",
                "expected": "ALLOWED",
                "reason": "Friendly compliment",
                "detector": "none"
            },
            {
                "id": "NC-003",
                "category": "Normal Conversation",
                "text": "You motherfucker",
                "expected": "ALLOWED",
                "reason": "Generic profanity",
                "detector": "none"
            },
            {
                "id": "NC-004",
                "category": "Normal Conversation",
                "text": "In the movie, they killed everyone",
                "expected": "ALLOWED",
                "reason": "Movie reference",
                "detector": "none"
            },
            {
                "id": "NC-005",
                "category": "Normal Conversation",
                "text": "World War II changed history",
                "expected": "ALLOWED",
                "reason": "Historical reference",
                "detector": "none"
            },
        ]
    
    def push_messages(self, delay: float = 0.3) -> int:
        """Push all test messages to Redis queue - all with same ID=205"""
        print("\n" + "="*70)
        print("📤 PUSHING TEST MESSAGES TO REDIS")
        print("="*70)
        print(f"📌 Using fixed ID: 205 for all messages")
        print(f"📌 Queue: {self.queue_name}")
        print("-"*70)
        
        count = 0
        for test in self.test_cases:
            # Create message with same structure, only text changes
            message = {
                "type": "message",
                "table": "user_messages",
                "id": 205,
                "data": {"text": test["text"]}
            }
            
            try:
                self.redis_client.lpush(
                    self.queue_name,
                    json.dumps(message)
                )
                count += 1
                
                # Show progress with emoji
                emoji = "🚫" if test["expected"] == "BLOCKED" else "✅"
                print(f"  {emoji} {test['id']}: {test['text'][:40]}... -> {test['expected']}")
                
                time.sleep(delay)
            except Exception as e:
                print(f"  ❌ Failed to push {test['id']}: {e}")
        
        print(f"\n📊 Pushed {count} messages to {self.queue_name}")
        return count
    
    def show_test_plan(self) -> None:
        """Display all test cases in a formatted table"""
        print("\n" + "="*70)
        print("🧪 MODERATION INTEGRATION TEST PLAN")
        print("="*70)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total Test Cases: {len(self.test_cases)}")
        print(f"📌 All messages use ID: 205")
        print("="*70)
        
        # Group by category
        categories = {}
        for test in self.test_cases:
            cat = test["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test)
        
        # Print by category
        for category, tests in categories.items():
            blocked = sum(1 for t in tests if t["expected"] == "BLOCKED")
            allowed = len(tests) - blocked
            
            print(f"\n📂 {category} ({len(tests)} tests | 🚫{blocked} | ✅{allowed})")
            print("-"*60)
            
            for test in tests:
                emoji = "🚫" if test["expected"] == "BLOCKED" else "✅"
                print(f"  {emoji} {test['id']}: {test['text'][:45]}...")
                print(f"     → {test['expected']} ({test['reason']})")
            print()
    
    def generate_report(self) -> str:
        """Generate a detailed test report"""
        report = []
        report.append("="*70)
        report.append("MODERATION INTEGRATION TEST REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Tests: {len(self.test_cases)}")
        report.append(f"All messages use ID: 205")
        report.append("")
        
        # Group by category
        categories = {}
        for test in self.test_cases:
            cat = test["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test)
        
        for category, tests in categories.items():
            report.append(f"\n{'='*60}")
            report.append(f"CATEGORY: {category}")
            report.append(f"{'='*60}")
            
            for test in tests:
                report.append(f"\n{test['id']}:")
                report.append(f"  Text: {test['text']}")
                report.append(f"  Expected: {test['expected']}")
                report.append(f"  Reason: {test['reason']}")
                report.append(f"  Detector: {test['detector']}")
        
        report.append("\n" + "="*70)
        report.append("END OF REPORT")
        report.append("="*70)
        
        return "\n".join(report)
    
    def save_report(self, filename: str = "test_report.txt") -> None:
        """Save test report to file"""
        report = self.generate_report()
        with open(filename, "w") as f:
            f.write(report)
        print(f"\n📄 Report saved to: {filename}")
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        total = len(self.test_cases)
        blocked = sum(1 for t in self.test_cases if t["expected"] == "BLOCKED")
        allowed = total - blocked
        
        # Count by detector
        detectors = {}
        for test in self.test_cases:
            detector = test["detector"]
            if detector not in detectors:
                detectors[detector] = {"total": 0, "blocked": 0, "allowed": 0}
            detectors[detector]["total"] += 1
            if test["expected"] == "BLOCKED":
                detectors[detector]["blocked"] += 1
            else:
                detectors[detector]["allowed"] += 1
        
        return {
            "total": total,
            "blocked": blocked,
            "allowed": allowed,
            "detectors": detectors
        }
    
    def print_summary(self) -> None:
        """Print summary statistics"""
        stats = self.get_summary_stats()
        
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"  Total Tests: {stats['total']}")
        print(f"  Expected BLOCKED: {stats['blocked']} 🚫")
        print(f"  Expected ALLOWED: {stats['allowed']} ✅")
        print("-"*70)
        print("  By Detector:")
        
        for detector, counts in stats['detectors'].items():
            if detector == "none":
                continue
            print(f"    {detector}: {counts['total']} tests (🚫{counts['blocked']} | ✅{counts['allowed']})")
        
        print("="*70)


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 REDIS MODERATION INTEGRATION TEST RUNNER")
    print("="*70)
    print(f"Redis Host: {REDIS_HOST}:{REDIS_PORT}")
    print(f"Queue Name: {QUEUE_NAME}")
    print(f"Fixed ID: 205 (all messages)")
    print("="*70)
    
    runner = ModerationTestRunner()
    
    # Show test plan
    runner.show_test_plan()
    
    # Ask for confirmation
    print("\n" + "="*70)
    response = input("🚀 Push all test messages to Redis? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Test cancelled.")
        return
    
    # Push all messages
    count = runner.push_messages(delay=0.3)
    
    if count == 0:
        print("\n❌ No messages pushed. Check Redis connection.")
        return
    
    # Show summary
    runner.print_summary()
    
    # Save report
    runner.save_report("test_report.txt")
    
    print("\n" + "="*70)
    print("✅ Test runner completed!")
    print("="*70)
    print("\n⚠️  REMEMBER: This only pushes test messages to Redis.")
    print("   To see actual moderation results, ensure the worker is running:")
    print("\n   📌 In a separate terminal:")
    print("   python3 -m app.workers.text_moderation_worker")
    print("\n   📌 Or check Redis queue:")
    print(f"   redis-cli LLEN {QUEUE_NAME}")
    print("="*70)


if __name__ == "__main__":
    main()