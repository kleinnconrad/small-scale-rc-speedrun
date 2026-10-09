import matplotlib.pyplot as plt
import numpy as np
import math

def plot_dashboard():
    # 1. Constants & Input data for 3660 Motor (3700KV on 3S)
    motor_kv = 3700
    akku_v = 11.1
    spur_gear = 68
    internal_ratio = 2.47
    tire_diameter_mm = 64.0

    # 2. Calculations
    pinions = np.arange(21, 45)
    fdr = (spur_gear / pinions) * internal_ratio
    radlast = (1 / fdr) * 100
    motor_rpm = motor_kv * akku_v
    achsdrehzahl = motor_rpm / fdr

    # 3. Plot Setup
    fig, ax1 = plt.subplots(figsize=(10, 7))

    # Y-Axis 1: Wheel Load (Blue)
    color1 = 'tab:blue'
    ax1.set_xlabel('Pinion Size (Teeth)', fontsize=12)
    ax1.set_ylabel('Wheel Load (%)', color=color1, fontsize=12)
    line1, = ax1.plot(pinions, radlast, color=color1, label='Wheel Load (%)', linewidth=2, marker='o')
    ax1.tick_params(axis='y', labelcolor=color1)

    # Y-Axis 2: Axle RPM (Red)
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Axle RPM at full throttle', color=color2, fontsize=12)
    line2, = ax2.plot(pinions, achsdrehzahl, color=color2, label='Axle RPM', linewidth=2, marker='x')
    ax2.tick_params(axis='y', labelcolor=color2)

    # 4. Draw multiple target lines (100, 110, 120, 130) as baseline
    circumference_m = (tire_diameter_mm * math.pi) / 1000.0
    target_speeds = [100.0, 110.0, 120.0, 130.0]
    line_colors = ['black', '#4a4a4a', '#7a7a7a', '#a3a3a3']
    target_lines = []

    for speed, color in zip(target_speeds, line_colors):
        target_rpm = (speed * 1000.0 / 60.0) / circumference_m
        # Make the 100 km/h line slightly thicker to highlight it as primary target
        lw = 2 if speed == 100.0 else 1.5
        line = ax2.axhline(target_rpm, color=color, linestyle='--', linewidth=lw, 
                           label=f'{int(speed)} km/h Target (~{int(target_rpm)} RPM)')
        target_lines.append(line)

    # 5. Thermal zones for 3660 Motor (Background colors)
    ax1.axhspan(10, 22.0, color='green', alpha=0.15)
    ax1.axhspan(22.0, 25.0, color='yellow', alpha=0.15)
    ax1.axhspan(25.0, 28.0, color='red', alpha=0.15)

    # Text labels for zones
    ax1.text(21.5, 16, 'Safe Zone (< 22%)', color='darkgreen', fontsize=11, fontweight='bold')
    ax1.text(21.5, 23.5, 'Sweet Spot (22% - 25%)', color='olive', fontsize=11, fontweight='bold')
    ax1.text(21.5, 26.5, 'Danger Zone (> 25%)', color='darkred', fontsize=11, fontweight='bold')

    # Axis limits and styling
    ax1.set_ylim(10, 28)
    ax1.set_xlim(20.5, 44.5)
    ax1.set_xticks(np.arange(21, 45, 2))

    # Merge all legends
    lines = [line1, line2] + target_lines
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower right', fontsize=9)

    plt.title('Drivetrain Dashboard: Carten T410R (Extended Speed Targets)', fontsize=14, fontweight='bold')
    fig.tight_layout()
    ax1.grid(True, linestyle=':', alpha=0.7)

    # Save image
    filename = 'antriebs_plot_multi_speed.png'
    plt.savefig(filename, dpi=300)
    print(f"SUCCESS: Dashboard successfully saved as '{filename}'.")

if __name__ == '__main__':
    plot_dashboard()
