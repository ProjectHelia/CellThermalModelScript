#Here i test the thermal model class
from cell_thermal_model import CellLumpedThermalModel

if __name__ == "__main__":
    # Create a cell with realistic properties
    
    #I chatgpted some example data and then messed around with it
    #Will obvioudly need correction here 
    cell = CellLumpedThermalModel(
        spec_heat_cap=4180,   # J/kg·K, water-like
        mass=1e-6,            # 1 mg
        abs_IR_A=0.08,
        abs_IR_B=0.07,
        abs_IR_C=0.06,
        heat_loss_coef=100.0,
        dt=0.1,
        cell_name="Test Cell"
    )

    # setup some simulation parameters
    simulation_time = 60 #in seconds 
    steps = int(simulation_time / cell.dt)

    # store the output temperature
    temps = []
    IR_absorbed = []

    # Just a test signal of where IR_A is constant 
    cell.input_new_IR_power(IR_A_power=0.0)

    print("Time\tTemp (°C)\tIR absorbed (J)")
    for i in range(steps):
        
        # Here i am keeping temperature constant 
        if i % 10 == 0:
            new_ambient = 37.0
            cell.input_ambient_temperature(new_ambient)

        # Step simulation to update calculations
        cell.step()

        # Store outputs
        temps.append(cell.output_temperature())
        IR_absorbed.append(cell.output_cell_IR_power())

        # Print current status
        print(f"{i*cell.dt:.1f}\t{cell.output_temperature():.4f}\t{cell.output_cell_IR_power():.6f}")
