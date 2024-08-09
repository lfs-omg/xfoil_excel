from auto_xfoil import automation
import matplotlib.pyplot as plt


auto1 = automation(airfoil_name='naca4412',
                  alpha=[-15,15,0.5],
                  flap_deflection=0,
                  x=0.75,
                  y=0.0328,
                  Re=6e6,
                  n_iter=100)
auto1.airfoil_txt()
y1=auto1.txt_to_excell()

auto2 = automation(airfoil_name='naca0012',
                  alpha=[-15,15,0.5],
                  flap_deflection=0,
                  x=0.75,
                  y=0.0328,
                  Re=6e6,
                  n_iter=100)
auto2.airfoil_txt()
y2=auto2.txt_to_excell()

plt.plot(y1['CD'],y1['CL'],label='naca4412')
plt.plot(y2['CD'],y2['CL'],label='nlf(1)-0215f')
plt.xlabel('CD')
plt.ylabel('CL')
plt.legend()
plt.grid(True)
plt.savefig('C:\\Users\\user\\PycharmProjects\\pythonProject\\xfoil\\xfoil6.99\\OUTPUT\\raw_excel_data\\figure1.png')









