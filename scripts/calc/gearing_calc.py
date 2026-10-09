import math

def calculate_rc_requirements():
    print("="*75)
    print(" Carten T410R Speed & Gearing Calculator v3.0 ")
    print("="*75)
    
    try:
        motor_size = input("Motor Size (3650 or 3660): ").strip()
        
        # Dynamic zone limits based on motor size
        if motor_size == "3660":
            limit_green, limit_yellow, limit_red = 22.0, 25.0, 28.0
        else:
            limit_green, limit_yellow, limit_red = 19.0, 22.0, 25.0
            motor_size = "3650 (Standard)"

        diameter_input = input("Please enter tire diameter in mm (e.g. 64): ")
        diameter_mm = float(eval(diameter_input))
        
        target_speed_kmh = float(input("Please enter desired target speed in km/h (e.g. 100): "))
    except Exception as e:
        print(f"Invalid input or formula error: {e}")
        return

    spur_gear = 68
    internal_ratio = 2.47
    pinions = range(21, 45)

    circumference_m = (diameter_mm * math.pi) / 1000.0
    speed_m_per_min = (target_speed_kmh * 1000.0) / 60.0
    axle_rpm = speed_m_per_min / circumference_m

    print("\n" + "="*75)
    print(" RESULTS AXLE ")
    print("="*75)
    print(f"Target Speed:          {target_speed_kmh} km/h")
    print(f"Motor Profile:         {motor_size}")
    print(f"Required Axle RPM:     {axle_rpm:,.0f} RPM".replace(',', '.'))
    
    print("\n" + "="*75)
    print(f" MOTOR REQUIREMENTS PER PINION (Spur: {spur_gear}T) ")
    print("="*75)
    print(f"{'Pinion':<8} | {'Ratio':<6} | {'Motor RPM':<14} | {'Wheel Load':<10} | {'Load Zone'}")
    print("-" * 75)

    for pinion in pinions:
        gear_ratio = (spur_gear / pinion) * internal_ratio
        motor_rpm = axle_rpm * gear_ratio
        load_pct = (1 / gear_ratio) * 100

        # Dynamic zone assignment
        if load_pct < limit_green:
            zone = "Safe (Track & Bashing)"
        elif load_pct < limit_yellow:
            zone = "Sweet Spot (Top-Speed)"
        elif load_pct <= limit_red:
            zone = "Danger Zone (Extreme!)"
        else:
            zone = "Heat Death (Overload!)"

        rpm_str = f"{motor_rpm:,.0f}".replace(',', '.')
        if motor_rpm > 50000:
            rpm_str += " (WARNING)"

        print(f"{pinion:<2} Teeth  | {gear_ratio:<6.2f} | {rpm_str:<14} | {load_pct:>5.1f} %     | {zone}")

if __name__ == '__main__':
    calculate_rc_requirements()
