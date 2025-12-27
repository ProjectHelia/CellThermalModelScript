##This file provides a class with the model of the cell
## Use the class to update IR measurements and ambient tempurature measurements 
## The output will be approximate cell tempurature and absorbed IR
## NOTE: that this is not going to be the most accurate cell model at the start
## NOTE: DOES NOT INCLUDE EFFECTS OF MICROWAVES YET

#by Subhaan Ahmed 

class CellLumpedThermalModel():
    """
    A simple cell thermal model that uses a lumped thermal capacitance model.
    Essentially, the entire clump of cells is treated as a UNIFORM temperature.
    Only use this if the cell clump is small (perhaps < 100um).

    This class takes inputs of the ambient temperature and the input IR energy 
    and simulates the estimated temperature of the cell. Note that it only simulates
    for the cells and not the flask

    Parameters
    ----------
    heat_capacity : float
        The specific heat capacity (J/kg·K) of the cell clump, Default = 4180 (i.e for water).
    mass : float
        Expected mass of the cell clump
    abs_IR_A : float
        Absorbivity of IR A power
    abs_IR_B : float
        Absorbivity of IR B power
    abs_IR_C : float
        Absorbivity of IR C power
    heat_loss_coefficient : float
        The convective heat loss coefficient, h. Default is 0.0001
    area : float
        the area of the cell culture. Default is 1e-5
    dt : float 
        A time step in seconds (be sensible please). Default is 0.1 seconds
    cell_name : string, optional
        Give a name for your cells (Default is "Kyane's fat cells")
        
    Attributes
    ----------
    cell_name : string
        As understood, the default is "Kyane's fat cells"
    specific_heat_capacity : float
    mass : float
    abs_IR_A : float
    abs_IR_B : float
    abs_IR_C : float
    ambient_temp : float
        The ambient temperature of the cell's surrounding, this can obviously change over time
    IR_A_power : float
    IR_B_power : float
    IR_C_power : float
    cell_area : float
    dt : float
    heat_loss_coefficient : float
    Q_IR : float
        The amount of IR (all types) absorbed by the cell
    output_cell_temp : float
        The approx output tempurature of the cell given ambient and IR tempurature   
    cell_heat_loss : float
        heat lost from cell to environment, in Watts (W)
    old_cell_temp : float
        The old cell temperature
        
    """
    def __init__(self, spec_heat_cap, mass, abs_IR_A, abs_IR_B, abs_IR_C, heat_loss_coef = 0.0001, area = 1e-5,
                                                                dt = 0.1, cell_name="Kyane's Fat Cells"):
        self.cell_name = cell_name
        self.specific_heat_capacity = spec_heat_cap
        self.mass = mass
        self.abs_IR_A = abs_IR_A
        self.abs_IR_B = abs_IR_B
        self.abs_IR_C = abs_IR_C
        self.heat_loss_coefficient = heat_loss_coef
        self.dt = dt
        self.cell_area = area
        
        #Other time dependant inputs
        self.ambient_temp = 37.0 # a default, can be changed
        self.IR_A_power = 0.0 # input IR power
        self.IR_B_power = 0.0
        self.IR_C_power = 0.0
        
        #Outputs: These outputs are outputs at a specific time
        self.Q_IR = 0.0 
        self.output_cell_temp = 37.0
        self.cell_heat_loss = 0.0
        
        #Other important simulation attributes
        self.old_cell_temp = 37.0 # start at 37 degrees
        
        
        
    def input_new_IR_power(self, IR_A_power=None, IR_B_power=None, IR_C_power=None):
        '''
        This method allows you to input a new IR power for A, B and C
        
        :param IR_A_power: float, optional
            Input a new IR_A power in Watts (W)
        :param IR_B_power: float, optional
            Input a new IR_B power in Watts (W)
        :param IR_C_power: float, optional
            Input a new IR_C power in Watts (W)
        '''
        if IR_A_power is not None: self.IR_A_power = IR_A_power
        if IR_B_power is not None: self.IR_B_power = IR_B_power
        if IR_C_power is not None: self.IR_C_power = IR_C_power
        
    def input_ambient_temperature(self, ambient_tempurature):
        '''
        This method allows you to input a new ambient tempurature
        NOTE: That this method assumes an instant increase in that ambient tempurature 
        
        :param ambient_tempurature: float
            Input a new ambient tempurature 
        '''
        self.ambient_temp = ambient_tempurature
        
    
    def output_temperature(self):
        '''
        Outputs the cell tempurature at this instance
        
        Returns
        -------
        float 
            Output tempurature of cells in degrees (C)
        '''
        
        return self.output_cell_temp
        
    def output_cell_IR_power(self):
        '''
        Outputs the emission IR power from the cells at this instance in time 
        
        Returns
        -------
        float 
            Output IR emission power in Watts (W)
        '''
        return self.Q_IR
        
        
    def step(self):
        '''
        The Step function calculates the temperature of the cells at a given time
        Currently does not implement dynamic changes in temperature to simplify the simulation
        If needed, dynamic simulation can be added
        '''
        
        #compute energy absorbed into cell due to the differnt IR powers
        IR_energy_absorbed = (self.abs_IR_A * self.IR_A_power +
                              self.abs_IR_B * self.IR_B_power +
                              self.abs_IR_C * self.IR_C_power) * self.dt
        
        #then compute energy lost from cells
        self.cell_heat_loss = self.heat_loss_coefficient * self.cell_area * (self.old_cell_temp - self.ambient_temp) * self.dt
        
        #temp change
        temp_change = (IR_energy_absorbed - self.cell_heat_loss) / (self.mass * self.specific_heat_capacity)
        
        #update the temperature
        self.output_cell_temp = self.output_cell_temp + temp_change
        
        self.old_cell_temp = self.output_cell_temp
        
        #The IR absorbtion 
        self.Q_IR = IR_energy_absorbed
        
        
        
        
        
        
        
        