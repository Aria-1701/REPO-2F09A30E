import re
# Code for Password Analyzer implemented hereimport re
import math
import argparse

def analyze_password(password):
    score = 0
    feedback = []
    pool_size = 0
    
    # 1. التحقق من طول كلمة المرور
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("[-] Password should be at least 8 characters long.")
        
    # 2. فحص الأنماط باستخدام Regular Expressions
    if re.search(r"[a-z]", password):
        score += 1
        pool_size += 26
    else:
        feedback.append("[-] Add lowercase letters.")
        
    if re.search(r"[A-Z]", password):
        score += 1
        pool_size += 26
    else:
        feedback.append("[-] Add uppercase letters.")
        
    if re.search(r"\d", password):
        score += 1
        pool_size += 10
    else:
        feedback.append("[-] Add numbers.")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
        pool_size += 32
    else:
        feedback.append("[-] Add special characters (symbols).")
        
    # 3. حساب الـ Entropy
    entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
    
    # التقييم النهائي
    if score == 5 and entropy > 60:
        strength = "Strong 🟢"
    elif score >= 3:
        strength = "Moderate 🟡"
    else:
        strength = "Weak 🔴"
        
    return strength, round(entropy, 2), feedback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Strength Analyzer Tool")
    parser.add_argument("-pwd", "--password", help="Password to analyze", required=True)
    
    args = parser.parse_args()
    
    strength, entropy, feedback = analyze_password(args.password)
    
    print("-" * 40)
    print(f"[*] Password Analysis Report")
    print("-" * 40)
    print(f"Password Strength : {strength}")
    print(f"Entropy Score     : {entropy} bits")
    if feedback:
        print("\nRecommendations to improve:")
        for tip in feedback:
            print(f"  {tip}")
    print("-" * 40)