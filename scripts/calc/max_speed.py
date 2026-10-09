import math

def calculate_max_speed():
    print("="*75)
    print(" Carten T410R Real-World Top-Speed Calculator v3.0 ")
    print("="*75)
    
    try:
        kv = float(input("Motor kV (e.g. 4000 or 3700): "))
        cells = int(input("LiPo Cells (e.g. 3 for 3S): "))
        diameter_mm = float(eval(input("Tire diameter in mm (e.g. 64): ")))
        
        motor_size = input("Motor Size (3650 or 3660): ").strip()
        if motor_size == "3660":
            max_load = 25.0  # Increased limit for the larger motor
        else:
            max_load = 22.0  # Standard limit
            motor_size = "3650 (Standard)"
            
    except Exception as e:
        print(f"Input error: {e}")
        return

    print(f"\n-> Setting thermal limit for {motor_size} motor automatically to {max_load} % wheel load.")

    v_max = cells * 4.2  
    v_nom = cells * 3.7  

    spur_gear = 68
    internal_ratio = 2.47
    
    rpm_max = kv * v_max
    rpm_nom = kv * v_nom
    circumference_m = (diameter_mm * math.pi) / 1000.0

    best_safe_pinion = None
    best_safe_speed_nom = 0
    best_safe_speed_max = 0
    best_safe_ratio = 0
    best_safe_load = 0

    absolute_max_pinion = 44
    abs_ratio = (spur_gear / absolute_max_pinion) * internal_ratio
    abs_load = (1 / abs_ratio) * 100
    abs_speed_nom = ((rpm_nom / abs_ratio) * circumference_m * 60) / 1000.0
    abs_speed_max = ((rpm_max / abs_ratio) * circumference_m * 60) / 1000.0

    for pinion in range(21, 45):
        gear_ratio = (spur_gear / pinion) * internal_ratio
        load_pct = (1 / gear_ratio) * 100
        
        if load_pct <= max_load:
            speed_nom = ((rpm_nom / gear_ratio) * circumference_m * 60) / 1000.0
            speed_max = ((rpm_max / gear_ratio) * circumference_m * 60) / 1000.0
            
            if speed_nom > best_safe_speed_nom:
                best_safe_speed_nom = speed_nom
                best_safe_speed_max = speed_max
                best_safe_pinion = pinion
                best_safe_ratio = gear_ratio
                best_safe_load = load_pct

    print("\n" + "="*75)
    print(" MOTOR & BATTERY DATA ")
    print("="*75)
    print(f"Battery under load:   {v_nom:.1f} V (Realistic Voltage Sag)")
    print(f"Motor RPM (Load):     {rpm_nom:,.0f} RPM".replace(',', '.'))
    
    if best_safe_pinion:
        print("\nTHERMALLY SAFE MAXIMUM (On the road)")
        print(f"Optimal Pinion:       {best_safe_pinion} Teeth (Ratio: {best_safe_ratio:.2f})")
        print(f"Actual Load:          {best_safe_load:.1f} % (Limit was {max_load} %)")
        print(f"Real Top Speed:       {best_safe_speed_nom:.1f} km/h")
    else:
        print("\nERROR: No pinion found that stays below the specified wheel load!")

    print("\nABSOLUTE CHASSIS LIMIT (44T - Caution!)")
    print(f"Actual Load:          {abs_load:.1f} %")
    print(f"Real Top Speed:       {abs_speed_nom:.1f} km/h")
    print("="*75)

if __name__ == '__main__':
    calculate_max_speed()
