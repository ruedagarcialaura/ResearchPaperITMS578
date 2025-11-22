import matplotlib.pyplot as plt


# Cases and their corresponding intervention levels
cases = ['TaskRabbit\n(US)', 'C-SPAN\n(US)', 'WPP\n(EU)', 'UK Energy Firm\n(EU)']
levels = [0, 1, 1, 0] # 0: No Intervention, 1: Reporting only

# Colors to distinguish regions (Blue for US, Green for EU)
colors = ['#1f77b4', '#1f77b4', "#2D954C", '#2D954C']

# Create the Plot 
plt.figure(figsize=(10, 6)) 
bars = plt.bar(cases, levels, color=colors, edgecolor='black')

plt.ylim(0, 4.5) 
y_ticks = [0, 1, 2, 3, 4]
y_labels = [
    '0: No Intervention',
    '1: Reporting only',
    '2: Active Investigation',
    '3: Fines Issued',
    '4: Severe Action'
]
plt.yticks(y_ticks, y_labels)


ax = plt.gca()
ax.set_ylabel('Regulatory Intervention Level', fontsize=12, rotation=270, labelpad=15)
ax.yaxis.set_label_position("right")

plt.xlabel('Case Studies', fontsize=12)
plt.title('Regulatory Intervention Level: Policy vs. Practice Gap', fontsize=18, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)


for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'Level {int(height)}',
             ha='center', va='bottom', fontweight='bold')

# Add Expectation Line 
plt.axhline(y=3, color='red', linestyle=':', linewidth=3, alpha=0.9, zorder=5, label='Policy Expectation')
plt.legend(loc='upper right')

# Final Layout Adjustments  
plt.tight_layout()
plt.show()