# Import all three modules
from gui import Gui
from plotter import Plotter
from data import CsvDataBase

# Initialize data module
data = CsvDataBase()

# Initialize plotter module with a reference to data
plotter = Plotter(data)

# Initialize gui module with references to both
app = Gui(data, plotter)

# Set the initial window size
app.geometry("800x600")

# Run the gui main loop
app.mainloop()
