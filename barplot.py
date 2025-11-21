import matplotlib.pyplot as plt


# Cases and their corresponding intervention levels
cases = ['TaskRabbit\n(US)', 'C-SPAN\n(US)', 'WPP\n(EU)', 'UK Energy Firm\n(EU)']
levels = [0, 1, 1, 0] # 0: No Intervention, 1: Reporting only

# Colors to distinguish regions (Blue for US, Orange for EU)
colors = ['#1f77b4', '#1f77b4', '#ff7f0e', '#ff7f0e']

# Create the Plot 
plt.figure(figsize=(10, 6)) 
bars = plt.bar(cases, levels, color=colors, edgecolor='black')

plt.ylim(0, 4.5) 
y_ticks = [0, 1, 2, 3, 4]
y_labels = [
    '0: No Intervention / Public inaction',
    '1: Reporting only',
    '2: Active Investigation',
    '3: Fines/Sanctions Issued',
    '4: Severe Action'
]
plt.yticks(y_ticks, y_labels)


plt.ylabel('Regulatory Intervention Level', fontsize=12)
plt.xlabel('Case Studies', fontsize=12)
plt.title('Regulatory Intervention Level: Policy vs. Practice Gap', fontsize=14, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)


for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'Level {int(height)}',
             ha='center', va='bottom', fontweight='bold')

# Add Expectation Line 
plt.axhline(y=3, color='red', linestyle=':', alpha=0.5, label='Policy Expectation')
plt.legend(loc='upper right')

# Final Layout Adjustments  
plt.tight_layout()
plt.show()