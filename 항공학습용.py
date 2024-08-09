from auto_xfoil import automation
import matplotlib.pyplot as plt


auto1 = automation(airfoil_name='naca4412',
                  alpha=[-10,20,0.5],
                  flap_deflection=0,
                  x=0.75,
                  y=0.0328,
                  Re=1e6,
                  n_iter=100)
auto1.airfoil_txt()
y1=auto1.txt_to_excell()

auto2 = automation(airfoil_name='naca0012',
                  alpha=[-10,20,0.5],
                  flap_deflection=0,
                  x=0.75,
                  y=0.0328,
                  Re=1e6,
                  n_iter=100)
auto2.airfoil_txt()
auto2.txt_to_excell()

